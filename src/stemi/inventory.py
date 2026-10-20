"""Local data inventory from metadata and headers only (research_plan step 1).

Rules this module follows:
- Reads metadata tables, WFDB ``.hea`` text and array shapes only. It never
  loads sample arrays and never downloads or deletes anything.
- Rows are local observations (E3). Registry values are copied for comparison,
  never overwritten; disagreements go to ``conflicts`` (E2, P3).
- ``target_rate`` stays null: the input spec is unresolved (C1.3, Q9).
- Acquisition rate, released rate and filter settings stay in separate
  columns (P5).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable, NamedTuple

import numpy as np
import pandas as pd

from .registry import CHALLENGE_DATASET_IDS, get_entry

OBSERVATION_TYPE = "local_observation"  # E3
DATA_ORIGINS = ("synthetic_fixture", "local_files")
TARGET_RATE_STATUS = "unresolved (C1.3, Q9)"

# Standard 12-lead names, used only to *identify* channels. Native order is kept;
# the model lead order is not decided here (P4, P6 ASSUMPTION, Q9).
STANDARD_12_LEADS = ("I", "II", "III", "aVR", "aVL", "aVF",
                     "V1", "V2", "V3", "V4", "V5", "V6")

# research_plan step 1 bounded selection
SELECTION_POOL_ROWS = 10_000
DEFAULT_SEED = 0

INVENTORY_COLUMNS = [
    "dataset_id", "release", "record_id", "patient_key", "patient_key_field",
    "observation_type", "data_origin", "selection_rule",
    "file_path", "header_found",
    "native_rate", "native_rate_source", "acquisition_rate", "filter_raw",
    "target_rate", "target_rate_status",
    "n_samples", "original_duration_s", "stored_duration_s",
    "padding_status", "padding_mask",
    "n_channels", "channel_names", "standard12_channel_map",
    "metadata_row", "shard_row",
    "registry_hz", "registry_leads", "conflicts",
]


# --------------------------------------------------------------------------- WFDB


@dataclass
class WfdbHeader:
    record_name: str
    n_sig: int
    fs: float | None
    n_samples: int | None
    channel_names: list[str]
    comments: list[str] = field(default_factory=list)


def parse_wfdb_header(path: Path) -> WfdbHeader:
    """Parse the record line, signal lines and comments of a single-segment .hea."""
    lines = path.read_text().splitlines()
    comments = [ln[1:].strip() for ln in lines if ln.startswith("#")]
    body = [ln for ln in lines if ln.strip() and not ln.startswith("#")]
    rec = body[0].split()
    n_sig = int(rec[1])
    # fs may be "500/1000(0)" (counter frequency); keep the sampling part only
    fs = float(rec[2].split("/")[0]) if len(rec) > 2 else None
    n_samples = int(rec[3]) if len(rec) > 3 else None
    names = [ln.split()[-1] for ln in body[1:1 + n_sig]]
    return WfdbHeader(rec[0], n_sig, fs, n_samples, names, comments)


def standard12_channel_map(channel_names: list[str]) -> dict[str, int] | None:
    """Map each standard lead name to its native channel index, or None if any is
    missing (C2.3). Keeps lead identity explicit so order is never assumed (P4)."""
    lookup = {name.lower(): i for i, name in enumerate(channel_names)}
    mapping = {lead: lookup.get(lead.lower()) for lead in STANDARD_12_LEADS}
    if any(i is None for i in mapping.values()):
        return None
    return mapping


def is_duplicate_representation(dataset_id: str, rel_path: str) -> bool:
    """PTB-XL records100 duplicates records500 and is never counted (C2.1, O2)."""
    return dataset_id == "ptb_xl" and Path(rel_path).parts[:1] == ("records100",)


# --------------------------------------------------------------------------- helpers


def _check_origin(data_origin: str) -> None:
    if data_origin not in DATA_ORIGINS:
        raise ValueError(f"data_origin must be one of {DATA_ORIGINS}")


def _select(df: pd.DataFrame, limit: int | None, seed: int) -> tuple[pd.DataFrame, str]:
    if limit is None:
        return df, "all metadata rows"
    pool = df.head(SELECTION_POOL_ROWS)
    n = min(limit, len(pool))
    rule = f"random {n} of first {len(pool)} metadata rows, seed={seed} (research_plan step 1)"
    return pool.sample(n=n, random_state=seed).sort_index(), rule


def _base_row(dataset_id: str, data_origin: str, selection_rule: str) -> dict:
    entry = get_entry(dataset_id)
    row = dict.fromkeys(INVENTORY_COLUMNS)
    row.update(
        dataset_id=dataset_id,
        release=entry.release,               # V1: exact registered string
        observation_type=OBSERVATION_TYPE,   # E3
        data_origin=data_origin,
        selection_rule=selection_rule,
        target_rate=None,                    # C1.3, Q9: not fixed to 500
        target_rate_status=TARGET_RATE_STATUS,
        registry_hz=entry.publisher_hz,
        registry_leads=entry.n_leads,
        conflicts=[],
    )
    return row


def _fill_from_header(row: dict, hea: Path) -> None:
    """Copy observed header values; note conflicts with the registry, never edit it (E2)."""
    if not hea.exists():
        row["header_found"] = False      # recorded, no search for replacements [NB p.29-30]
        row["conflicts"].append("header file missing")
        return
    h = parse_wfdb_header(hea)
    row.update(
        header_found=True,
        native_rate=h.fs,
        native_rate_source="header_observed",
        n_samples=h.n_samples,
        original_duration_s=(h.n_samples / h.fs) if h.fs and h.n_samples else None,
        n_channels=h.n_sig,
        channel_names=json.dumps(h.channel_names),
    )
    if h.fs is not None and h.fs != row["registry_hz"]:
        row["conflicts"].append(
            f"header fs {h.fs:g} != registry {row['registry_hz']} (registry unchanged, E2)")
    if h.n_sig != row["registry_leads"]:
        row["conflicts"].append(
            f"header n_sig {h.n_sig} != registry {row['registry_leads']} (registry unchanged, E2)")


def _finish(rows: list[dict]) -> pd.DataFrame:
    for r in rows:
        r["conflicts"] = "; ".join(r["conflicts"]) or None
    return pd.DataFrame(rows, columns=INVENTORY_COLUMNS)


# --------------------------------------------------------------------------- sources


def inventory_ptb_xl(root: Path, *, data_origin: str, limit: int | None = None,
                     seed: int = DEFAULT_SEED) -> pd.DataFrame:
    """One row per ``ptbxl_database.csv`` row, read via ``filename_hr`` only (C2.1, O2)."""
    _check_origin(data_origin)
    root = Path(root)
    meta = pd.read_csv(root / "ptbxl_database.csv")
    meta, rule = _select(meta, limit, seed)
    rows = []
    for idx, rec in meta.iterrows():
        rel = str(rec["filename_hr"])
        if is_duplicate_representation("ptb_xl", rel) or Path(rel).parts[:1] != ("records500",):
            raise ValueError(f"filename_hr {rel!r} is not under records500 (C2.1)")
        row = _base_row("ptb_xl", data_origin, rule)
        row.update(record_id=str(rec["ecg_id"]), patient_key=str(rec["patient_id"]),
                   patient_key_field="patient_id", file_path=rel, metadata_row=int(idx))
        _fill_from_header(row, root / f"{rel}.hea")
        rows.append(row)
    return _finish(rows)


def inventory_mimic_iv_ecg(root: Path, *, data_origin: str, limit: int | None = None,
                           seed: int = DEFAULT_SEED) -> pd.DataFrame:
    """One row per ``record_list.csv`` row (``subject_id``, ``study_id``, ``path``).

    ``cart_id`` and filter strings are not read: cart_id is not a device model and
    filter strings are not numeric cutoffs (C2.6).
    """
    _check_origin(data_origin)
    root = Path(root)
    meta = pd.read_csv(root / "record_list.csv")
    meta, rule = _select(meta, limit, seed)
    rows = []
    for idx, rec in meta.iterrows():
        rel = str(rec["path"])
        row = _base_row("mimic_iv_ecg", data_origin, rule)
        row.update(record_id=str(rec["study_id"]), patient_key=str(rec["subject_id"]),
                   patient_key_field="subject_id", file_path=rel, metadata_row=int(idx))
        _fill_from_header(row, root / f"{rel}.hea")
        rows.append(row)
    return _finish(rows)


def inventory_ptb_diagnostic(root: Path, *, data_origin: str) -> pd.DataFrame:
    """One row per ``patientNNN/*.hea``. Identifies the standard 12 of 15 channels (C2.3).

    No 1000→500 Hz conversion is applied; that is a planned, undecided step.
    """
    _check_origin(data_origin)
    root = Path(root)
    rows = []
    for hea in sorted(root.glob("patient*/*.hea")):
        rel = hea.relative_to(root).with_suffix("").as_posix()
        row = _base_row("ptb_diagnostic", data_origin, "all patient*/ headers")
        row.update(record_id=rel, patient_key=hea.parent.name,
                   patient_key_field="patient_folder", file_path=rel)
        _fill_from_header(row, hea)
        idx = standard12_channel_map(json.loads(row["channel_names"]))
        row["standard12_channel_map"] = json.dumps(idx) if idx is not None else None
        if idx is None:
            row["conflicts"].append("standard 12 leads not all found (C2.3)")
        rows.append(row)
    return _finish(rows)


def inventory_challenge(dataset_id: str, root: Path, *, data_origin: str) -> pd.DataFrame:
    """One row per ``.hea`` in a Challenge 2021 source dir. Signal files are not opened.

    No patient key is given in the PDFs, so ``patient_key`` stays null (S7 is applied later).
    """
    if dataset_id not in CHALLENGE_DATASET_IDS:
        raise ValueError(f"{dataset_id!r} is not a Challenge 2021 source")
    _check_origin(data_origin)
    root = Path(root)
    rows = []
    for hea in sorted(root.glob("*.hea")):
        row = _base_row(dataset_id, data_origin, "all headers in directory")
        row.update(record_id=hea.stem, file_path=hea.with_suffix("").name)
        _fill_from_header(row, hea)
        rows.append(row)
    return _finish(rows)


class Code15Shard(NamedTuple):
    """What the inventory needs from one CODE-15% shard: never the tracing values."""
    name: str
    tracings_shape: tuple[int, ...]   # documented as N x 4096 x 12 (C2.2)
    exam_ids: np.ndarray              # join key, one per tracing row


def read_npy_shards(root: Path) -> Iterable[Code15Shard]:
    """Stand-in reader for ``<shard>_tracings.npy`` + ``<shard>_exam_id.npy`` pairs.

    Real CODE-15% shards are HDF5; reading them needs h5py, which is not approved
    for this environment, so a matching HDF5 reader is deferred. ``mmap_mode`` only
    parses the .npy header, so tracing values are not loaded.
    """
    for tr in sorted(Path(root).glob("*_tracings.npy")):
        stem = tr.name[: -len("_tracings.npy")]
        ids_path = tr.with_name(f"{stem}_exam_id.npy")
        if not ids_path.exists():
            raise ValueError(f"{stem}: no exam_id array; row-position join is forbidden (C2.2)")
        shape = np.load(tr, mmap_mode="r").shape
        yield Code15Shard(stem, shape, np.load(ids_path))


def inventory_code15(root: Path, *, data_origin: str, exams_csv: str = "exams.csv",
                     shard_reader: Callable[[Path], Iterable[Code15Shard]] = read_npy_shards,
                     ) -> pd.DataFrame:
    """One row per stored tracing, joined to ``exams.csv`` on ``exam_id`` (C2.2).

    4096 / 400 Hz = 10.24 s is the *stored* length including padding, so
    ``original_duration_s`` stays null and no padding mask is inferred.
    ``patient_key`` stays null: the PDFs give only ``exam_id`` (BG-UNCONFIRMED).
    """
    _check_origin(data_origin)
    root = Path(root)
    entry = get_entry("code15")
    exams = pd.read_csv(root / exams_csv)
    if exams["exam_id"].duplicated().any():
        raise ValueError("exams.csv has duplicate exam_id; cannot join safely (C2.2)")
    meta_row_by_exam = {int(e): int(i) for i, e in exams["exam_id"].items()}
    rows = []
    for shard in shard_reader(root):
        n, n_stored, n_leads = shard.tracings_shape
        if len(shard.exam_ids) != n:
            raise ValueError(f"{shard.name}: {len(shard.exam_ids)} exam_ids for {n} tracings")
        for i, exam_id in enumerate(shard.exam_ids):
            row = _base_row("code15", data_origin, "all stored tracings")
            meta_row = meta_row_by_exam.get(int(exam_id))
            row.update(
                record_id=str(int(exam_id)), file_path=shard.name, header_found=None,
                native_rate=entry.publisher_hz, native_rate_source="registry_documentary",
                n_samples=n_stored, stored_duration_s=n_stored / entry.publisher_hz,
                original_duration_s=None,
                padding_status="stored_padded; interpretation unresolved (C2.2)",
                n_channels=n_leads, metadata_row=meta_row, shard_row=i,
            )
            if meta_row is None:
                row["conflicts"].append("exam_id not found in exams.csv")
            if n_leads != entry.n_leads:
                row["conflicts"].append(f"tracings leads {n_leads} != registry {entry.n_leads}")
            rows.append(row)
    return _finish(rows)


def write_inventory(df: pd.DataFrame, path: Path) -> None:
    """Write a CSV; refuses to overwrite an existing artifact (P3, V5 ASSUMPTION)."""
    path = Path(path)
    if path.exists():
        raise FileExistsError(f"{path} exists; write a new versioned file instead (V5)")
    df.to_csv(path, index=False)
