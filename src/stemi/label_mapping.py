"""Code-level label mapping M0–M12 (research_plan §2; data_contract §3).

Produces only ``candidate`` / ``unresolved`` / ``excluded`` rows from source
annotations. ``confirmed`` comes only from a review decision (M1, L13).

Input record keys (dict): ``dataset_id``, ``record_id``, ``label_source``,
``original_label``, and optionally ``patient_key``, ``release``, ``codes``,
``ecg_time``, ``event_time``, ``linked_diagnoses``, ``file_path``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Callable, Iterable, Mapping

import pandas as pd

from . import CONTRACT_VERSION
from .inventory import is_duplicate_representation
from .registry import CHALLENGE_DATASET_IDS, DATASET_IDS, get_entry

MAPPING_VERSION = "0.1.0"

# BG-UNCONFIRMED: filled only from a reviewer-approved file (L4, L7). Empty until
# clinical sign-off, so M7/M8 cannot fire in production.
APPROVED_MI_STATEMENT_CODES: Mapping[str, frozenset[str]] = MappingProxyType({})
APPROVED_ST_INJURY_CODES: Mapping[str, frozenset[str]] = MappingProxyType({})
# Q2: the acute window is undefined, so M9/M10 cannot fire in production.
ACUTE_WINDOW: Callable[[Any, Any], bool] | None = None

# O11 ASSUMPTION: sources from the same challenge distribution share a group
# (also covers O4 Ningbo/Chapman and O5 CPSC exports). Every other source is its
# own group; O10 overlaps are BG-UNCONFIRMED and not encoded.
OVERLAP_GROUPS: Mapping[str, str] = MappingProxyType({
    **{ds: ds for ds in DATASET_IDS},
    **{ds: "challenge_2021" for ds in CHALLENGE_DATASET_IDS},
})

# M12: datasets known to have no target-label source. Empty because which
# sources qualify (e.g. code15) is BG-UNCONFIRMED.
NO_TARGET_LABEL_SOURCE: frozenset[str] = frozenset()

LABEL_SOURCES = ("scp_statement", "machine_text", "snomed", "aha_statement", "rhythm_label",
                 "beat_annotation", "linked_clinical", "header_comment", "none")
STATUSES = ("confirmed", "candidate", "unresolved", "excluded")
PROPOSED_CLASSES = ("STEMI", "NSTEMI", "non-MI", "MI_unspecified")
FINAL_CLASSES = ("STEMI", "NSTEMI", "non-MI")
PATIENT_KEY_QUALITIES = ("native", "record_proxy")
# Values allowed in a linked_clinical record's ``linked_diagnoses`` (ASSUMPTION names)
LINKED_DIAGNOSES = ("STEMI", "NSTEMI", "no_acute_mi")

LABEL_COLUMNS = [
    "dataset_id", "release", "record_id", "patient_key", "patient_key_quality",
    "overlap_group", "original_label", "label_source", "ecg_time", "supporting_evidence",
    "status", "proposed_class", "final_class", "exclusion_reason", "pretraining_eligible",
    "rule_id", "reviewer", "review_date", "contract_version", "mapping_version",
]


@dataclass(frozen=True)
class MappingConfig:
    """Production defaults come from the module constants; tests build their own."""
    mi_codes: Mapping[str, frozenset[str]] = APPROVED_MI_STATEMENT_CODES
    st_codes: Mapping[str, frozenset[str]] = APPROVED_ST_INJURY_CODES
    acute_window: Callable[[Any, Any], bool] | None = ACUTE_WINDOW
    overlap_groups: Mapping[str, str] = OVERLAP_GROUPS
    no_target_label_source: frozenset[str] = NO_TARGET_LABEL_SOURCE


PRODUCTION_CONFIG = MappingConfig()


class InvalidReviewError(ValueError):
    pass


@dataclass(frozen=True)
class ReviewDecision:
    """One reviewer decision (L5, L7). The only route to ``confirmed`` (M1)."""
    status: str
    reviewer: str
    review_date: str
    final_class: str | None = None
    exclusion_reason: str | None = None
    notes: str | None = None

    def __post_init__(self):
        if not self.reviewer or not str(self.reviewer).strip():
            raise InvalidReviewError("review has no reviewer (invariant 1, E1)")
        if not self.review_date or not str(self.review_date).strip():
            raise InvalidReviewError("review has no review_date (E1)")
        # L13: a reviewer resolves a record; leaving it 'candidate' is not a decision
        if self.status not in ("confirmed", "unresolved", "excluded"):
            raise InvalidReviewError(f"review status {self.status!r} not allowed")
        if (self.final_class is not None) != (self.status == "confirmed"):
            raise InvalidReviewError("final_class must be set iff status == confirmed (invariant 1)")
        if self.final_class is not None and self.final_class not in FINAL_CLASSES:
            raise InvalidReviewError(f"final_class {self.final_class!r} not in {FINAL_CLASSES}")
        if self.status == "excluded" and not self.exclusion_reason:
            raise InvalidReviewError("excluded review needs exclusion_reason (invariant 6, E4)")


def reviews_from_frame(df: pd.DataFrame) -> dict[tuple[str, str], ReviewDecision]:
    """Build the review lookup from a ``review_decisions.csv``-shaped frame."""
    out = {}
    for rec in df.to_dict("records"):
        key = (rec["dataset_id"], str(rec["record_id"]))
        if key in out:
            raise InvalidReviewError(f"more than one review for {key}")
        clean = {k: (None if pd.isna(v) else v) for k, v in rec.items()}
        out[key] = ReviewDecision(
            status=clean["status"], reviewer=clean.get("reviewer"),
            review_date=clean.get("review_date"), final_class=clean.get("final_class"),
            exclusion_reason=clean.get("exclusion_reason"), notes=clean.get("notes"))
    return out


# --------------------------------------------------------------------------- mapping


def _base_row(rec: Mapping, config: MappingConfig, pretraining_eligible: bool) -> dict:
    ds = rec["dataset_id"]
    entry = get_entry(ds, rec.get("release"))  # V1: exact release or error
    src = rec["label_source"]
    if src not in LABEL_SOURCES:
        raise ValueError(f"label_source {src!r} not in {LABEL_SOURCES}")
    record_id = str(rec["record_id"])
    patient_key = rec.get("patient_key")
    if patient_key is None or (isinstance(patient_key, float) and pd.isna(patient_key)):
        patient_key, quality = record_id, "record_proxy"   # S7 (ASSUMPTION)
    else:
        patient_key, quality = str(patient_key), "native"
    return {
        "dataset_id": ds,
        "release": entry.release,
        "record_id": record_id,
        "patient_key": patient_key,
        "patient_key_quality": quality,
        "overlap_group": config.overlap_groups[ds],          # O11 (ASSUMPTION)
        "original_label": rec.get("original_label"),         # L5/P3: passed through untouched
        "label_source": src,
        "ecg_time": rec.get("ecg_time"),
        "supporting_evidence": None,
        "status": "unresolved",                              # M0
        "proposed_class": None,
        "final_class": None,
        "exclusion_reason": None,
        "pretraining_eligible": bool(pretraining_eligible),  # L11: False unless reviewed
        "rule_id": "M0",
        "reviewer": None,
        "review_date": None,
        "contract_version": CONTRACT_VERSION,
        "mapping_version": MAPPING_VERSION,
    }


def _evidence(**kv) -> str:
    return json.dumps(kv, sort_keys=True, default=str)


def _code_hits(ds: str, codes: set[str], config: MappingConfig) -> tuple[set[str], set[str]]:
    return (codes & set(config.mi_codes.get(ds, ())),
            codes & set(config.st_codes.get(ds, ())))


def map_linked_clinical(row: dict, rec: Mapping, config: MappingConfig) -> dict:
    """M9 / M10 / M11 for ``label_source == linked_clinical``.

    Conflict check (M11) runs first so a conflicting record can never reach a
    candidate class. While the acute window is None (Q2) nothing else fires.
    """
    dx = set(rec.get("linked_diagnoses") or ())
    unknown = dx - set(LINKED_DIAGNOSES)
    if unknown:
        raise ValueError(f"unknown linked_diagnoses {sorted(unknown)}")
    mi_hit, st_hit = _code_hits(row["dataset_id"], set(map(str, rec.get("codes") or ())), config)
    conflict = None
    if len(dx) > 1:
        conflict = f"multiple linked diagnoses {sorted(dx)}"
    elif "no_acute_mi" in dx and (mi_hit or st_hit):
        conflict = f"no_acute_mi contradicts codes {sorted(mi_hit | st_hit)}"
    if conflict:                                                             # M11 (L6)
        return {**row, "rule_id": "M11", "supporting_evidence": _evidence(conflict=conflict)}
    if not dx:                                                               # M4
        return {**row, "rule_id": "M4"}
    if config.acute_window is None:                                          # Q2
        return {**row, "supporting_evidence": _evidence(
            linked_diagnoses=sorted(dx), note="acute window undefined (Q2)")}
    ecg_time, event_time = rec.get("ecg_time"), rec.get("event_time")
    if ecg_time is None or event_time is None or not config.acute_window(ecg_time, event_time):
        return {**row, "supporting_evidence": _evidence(
            linked_diagnoses=sorted(dx), note="timing missing or outside acute window")}
    (d,) = dx
    evidence = _evidence(linked_diagnoses=[d], event_time=event_time)
    if d in ("STEMI", "NSTEMI"):                                             # M9
        return {**row, "status": "candidate", "proposed_class": d, "rule_id": "M9",
                "supporting_evidence": evidence}
    return {**row, "status": "candidate", "proposed_class": "non-MI",        # M10 (L14, Q4)
            "rule_id": "M10", "supporting_evidence": evidence}


def map_record(rec: Mapping, review: ReviewDecision | None = None,
               technical_exclusion: str | None = None, *,
               pretraining_eligible: bool = False,
               config: MappingConfig = PRODUCTION_CONFIG) -> dict | None:
    """Apply M0–M12, first match wins. Returns None when M3 drops the row."""
    # M3 runs as a pre-filter: a duplicate representation is not a record, so it
    # must not be confirmed or excluded by the later rules (O2).
    if rec.get("file_path") and is_duplicate_representation(rec["dataset_id"], rec["file_path"]):
        return None
    row = _base_row(rec, config, pretraining_eligible)                       # M0
    if review is not None:                                                   # M1
        if not isinstance(review, ReviewDecision):
            raise InvalidReviewError("review must be a validated ReviewDecision")
        return {**row, "status": review.status, "final_class": review.final_class,
                "exclusion_reason": review.exclusion_reason, "reviewer": review.reviewer,
                "review_date": review.review_date, "rule_id": "M1",
                "supporting_evidence": _evidence(review_notes=review.notes) if review.notes else None}
    if technical_exclusion is not None:                                      # M2 (E4)
        if not str(technical_exclusion).strip():
            raise ValueError("technical_exclusion needs a non-empty reason (invariant 6)")
        return {**row, "status": "excluded", "exclusion_reason": str(technical_exclusion),
                "rule_id": "M2"}
    src = row["label_source"]
    codes = set(map(str, rec.get("codes") or ()))
    if src == "linked_clinical":                                             # M9/M10/M11
        return map_linked_clinical(row, rec, config)
    if src == "none" or not codes:                                           # M4: never non-MI (L1)
        return {**row, "rule_id": "M4"}
    if src == "machine_text":                                                # M5 (L2)
        return {**row, "rule_id": "M5"}
    if src in ("rhythm_label", "beat_annotation"):                           # M6 (L2)
        return {**row, "rule_id": "M6"}
    mi_hit, st_hit = _code_hits(row["dataset_id"], codes, config)
    # Table order: M7 before M8, so a record hitting both lists gets M7. (The §2.3
    # sketch prefers M8; status and proposed_class are identical either way.)
    hits = _evidence(st_injury_codes=sorted(st_hit), mi_statement_codes=sorted(mi_hit))
    if st_hit:                                                               # M7 (L2: not STEMI)
        return {**row, "status": "candidate", "proposed_class": "MI_unspecified",
                "rule_id": "M7", "supporting_evidence": hits}
    if mi_hit:                                                               # M8 (L2, L3)
        return {**row, "status": "candidate", "proposed_class": "MI_unspecified",
                "rule_id": "M8", "supporting_evidence": hits}
    if row["dataset_id"] in config.no_target_label_source:                   # M12 (L11)
        return {**row, "rule_id": "M12"}
    return {**row, "rule_id": "M4"}                                          # no MI code: L1


def map_records(records: Iterable[Mapping],
                reviews: Mapping[tuple[str, str], ReviewDecision] | None = None,
                technical_exclusions: Mapping[tuple[str, str], str] | None = None, *,
                pretraining_eligible: Mapping[str, bool] | None = None,
                config: MappingConfig = PRODUCTION_CONFIG) -> pd.DataFrame:
    """Map many records into a §2.1 label table and check the invariants.

    ``reviews`` / ``technical_exclusions`` are keyed by ``(dataset_id, record_id)``.
    ``pretraining_eligible`` is per dataset and defaults to False (L11).
    """
    reviews = reviews or {}
    technical_exclusions = technical_exclusions or {}
    pretraining_eligible = pretraining_eligible or {}
    rows = []
    for rec in records:
        key = (rec["dataset_id"], str(rec["record_id"]))
        row = map_record(rec, reviews.get(key), technical_exclusions.get(key),
                         pretraining_eligible=pretraining_eligible.get(rec["dataset_id"], False),
                         config=config)
        if row is not None:
            rows.append(row)
    df = pd.DataFrame(rows, columns=LABEL_COLUMNS).astype({"pretraining_eligible": bool})
    validate_label_table(df)
    return df


# --------------------------------------------------------------------------- invariants


class InvariantError(AssertionError):
    pass


def _nonempty(v) -> bool:
    return v is not None and not (isinstance(v, float) and pd.isna(v)) and str(v).strip() != ""


def validate_label_table(df: pd.DataFrame) -> None:
    """Enforce research_plan §2.2 invariants 1, 2, 3 and 6 plus enum/column checks."""
    if list(df.columns) != LABEL_COLUMNS:
        raise InvariantError("columns do not match research_plan §2.1")
    for col, allowed in (("status", STATUSES), ("label_source", LABEL_SOURCES),
                         ("patient_key_quality", PATIENT_KEY_QUALITIES)):
        bad = ~df[col].isin(allowed)
        if bad.any():
            raise InvariantError(f"{col} has values outside {allowed}")
    for col, allowed in (("proposed_class", PROPOSED_CLASSES), ("final_class", FINAL_CLASSES)):
        bad = df[col].notna() & ~df[col].isin(allowed)
        if bad.any():
            raise InvariantError(f"{col} has values outside {allowed}")
    confirmed = df["status"] == "confirmed"
    if (df["final_class"].notna() != confirmed).any():
        raise InvariantError("invariant 1: final_class non-null iff status == confirmed")
    if confirmed.any() and ((df.loc[confirmed, "rule_id"] != "M1").any()
                            or not df.loc[confirmed, "reviewer"].map(_nonempty).all()):
        raise InvariantError("invariant 1: confirmed rows need rule_id M1 and a reviewer")
    if ((df["final_class"] == "non-MI") & (df["rule_id"] != "M1")).any():
        raise InvariantError("invariant 2: non-MI final_class only via M1")
    if (df["rule_id"].isin(["M5", "M6", "M7", "M8"])
            & df["proposed_class"].isin(["STEMI", "NSTEMI"])).any():
        raise InvariantError("invariant 3: M5–M8 rows cannot propose STEMI/NSTEMI")
    if (df["proposed_class"].notna() & (df["status"] != "candidate")).any():
        raise InvariantError("proposed_class is set for candidate rows only")
    excluded = df["status"] == "excluded"
    if excluded.any() and not df.loc[excluded, "exclusion_reason"].map(_nonempty).all():
        raise InvariantError("invariant 6: excluded rows need exclusion_reason")


# --------------------------------------------------------------------------- loaders


def supervised_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Invariant 5: only confirmed rows may reach supervised train/val/test loaders."""
    validate_label_table(df)
    return df[df["status"] == "confirmed"].copy()


def pretraining_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Invariant 5 / L11: any status, but only where pretraining_eligible is True."""
    validate_label_table(df)
    return df[df["pretraining_eligible"].astype(bool)].copy()
