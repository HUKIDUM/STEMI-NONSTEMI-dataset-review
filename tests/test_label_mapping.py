"""T2: label mapping M0–M12 on synthetic records (no real labels or codes)."""

import json

import pandas as pd
import pytest

import stemi.label_mapping as lm
from stemi.label_mapping import (
    LABEL_COLUMNS, InvalidReviewError, InvariantError, MappingConfig, ReviewDecision,
    map_record, map_records, pretraining_rows, reviews_from_frame, supervised_rows,
    validate_label_table,
)

# Invented codes; they stand for nothing real.
FAKE_MI = {"ptb_xl": frozenset({"FAKE_MI_A"}), "sph": frozenset({"FAKE_MI_B"})}
FAKE_ST = {"ptb_xl": frozenset({"FAKE_ST_A"})}


def within_24h(ecg_time, event_time):
    return abs(pd.Timestamp(ecg_time) - pd.Timestamp(event_time)) <= pd.Timedelta(hours=24)


TEST_CONFIG = MappingConfig(mi_codes=FAKE_MI, st_codes=FAKE_ST, acute_window=within_24h)


def rec(**kw):
    base = {"dataset_id": "ptb_xl", "record_id": "1", "patient_key": "p1",
            "label_source": "scp_statement", "original_label": "{'FAKE_X': 100.0}",
            "codes": ["FAKE_X"]}
    base.update(kw)
    return base


def review(**kw):
    base = {"status": "confirmed", "reviewer": "rev_a", "review_date": "2026-10-19",
            "final_class": "STEMI"}
    base.update(kw)
    return ReviewDecision(**base)


def mixed_records():
    """A spread of synthetic records hitting every rule under TEST_CONFIG."""
    return [
        rec(record_id="r0", label_source="none", codes=[], original_label=None),        # M4
        rec(record_id="r1", label_source="machine_text", original_label="ACUTE MI ?",
            codes=["txt"]),                                                             # M5
        rec(dataset_id="code15", record_id="r2", label_source="rhythm_label",
            codes=["FAKE_RHYTHM"], patient_key=None),                                   # M6
        rec(dataset_id="incart", record_id="r3", label_source="beat_annotation",
            codes=["N"], patient_key=None),                                             # M6
        rec(record_id="r4", codes=["FAKE_ST_A"]),                                       # M7
        rec(record_id="r5", codes=["FAKE_MI_A"]),                                       # M8
        rec(record_id="r6", codes=["FAKE_ST_A", "FAKE_MI_A"]),                          # M7 (table order)
        rec(dataset_id="mimic_iv_ecg", record_id="r7", label_source="linked_clinical",
            linked_diagnoses=["STEMI"], ecg_time="2026-01-01 10:00",
            event_time="2026-01-01 12:00", codes=[]),                                   # M9
        rec(dataset_id="mimic_iv_ecg", record_id="r8", label_source="linked_clinical",
            linked_diagnoses=["no_acute_mi"], ecg_time="2026-01-01 10:00",
            event_time="2026-01-01 11:00", codes=[]),                                   # M10
        rec(dataset_id="mimic_iv_ecg", record_id="r9", label_source="linked_clinical",
            linked_diagnoses=["STEMI", "no_acute_mi"], ecg_time="2026-01-01 10:00",
            event_time="2026-01-01 11:00"),                                             # M11
        rec(record_id="r10", codes=["FAKE_X"]),                                         # M4 fallthrough
        rec(record_id="r11", file_path="records100/00000/00011_lr"),                    # M3 drop
        rec(record_id="r12"),                                                           # M2 via table
        rec(record_id="r13", codes=["FAKE_MI_A"]),                                      # M1 via review
    ]


def mixed_table(config=TEST_CONFIG, **kw):
    return map_records(
        mixed_records(),
        reviews={("ptb_xl", "r13"): review(final_class="NSTEMI")},
        technical_exclusions={("ptb_xl", "r12"): "non_reducible_lead_set"},
        config=config, **kw)


# --------------------------------------------------------------------------- schema / config


def test_output_columns_match_schema():
    df = mixed_table()
    assert list(df.columns) == LABEL_COLUMNS
    assert df["rule_id"].notna().all()
    assert (df["contract_version"] == "0.1.0-draft").all()
    assert (df["mapping_version"] == lm.MAPPING_VERSION).all()


def test_rule_coverage_on_mixed_records():
    got = dict(zip(mixed_table()["record_id"], mixed_table()["rule_id"]))
    assert got == {"r0": "M4", "r1": "M5", "r2": "M6", "r3": "M6", "r4": "M7", "r5": "M8",
                   "r6": "M7", "r7": "M9", "r8": "M10", "r9": "M11", "r10": "M4",
                   "r12": "M2", "r13": "M1"}


def test_production_config_is_empty():
    assert dict(lm.APPROVED_MI_STATEMENT_CODES) == {}
    assert dict(lm.APPROVED_ST_INJURY_CODES) == {}
    assert lm.ACUTE_WINDOW is None
    assert lm.NO_TARGET_LABEL_SOURCE == frozenset()
    with pytest.raises(TypeError):
        lm.APPROVED_MI_STATEMENT_CODES["ptb_xl"] = frozenset({"X"})


def test_production_config_yields_zero_candidates():
    df = mixed_table(config=lm.PRODUCTION_CONFIG)
    assert (df["status"] != "candidate").all()
    assert set(df["status"]) <= {"unresolved", "excluded", "confirmed"}
    assert not df["rule_id"].isin(["M7", "M8", "M9", "M10"]).any()
    assert (df.loc[df["status"] == "confirmed", "rule_id"] == "M1").all()


def test_injected_config_does_not_mutate_module_constants():
    mixed_table()
    assert dict(lm.APPROVED_MI_STATEMENT_CODES) == {} and lm.ACUTE_WINDOW is None
    assert lm.PRODUCTION_CONFIG.acute_window is None


# --------------------------------------------------------------------------- invariants


def test_invariant1_final_class_iff_confirmed_via_m1_with_reviewer():
    df = mixed_table()
    confirmed = df["status"] == "confirmed"
    assert (df["final_class"].notna() == confirmed).all()
    assert (df.loc[confirmed, "rule_id"] == "M1").all()
    assert df.loc[confirmed, "reviewer"].notna().all()
    bad = df.copy()
    bad.loc[bad["record_id"] == "r5", "final_class"] = "STEMI"
    with pytest.raises(InvariantError, match="invariant 1"):
        validate_label_table(bad)
    bad = df.copy()
    bad.loc[confirmed, "reviewer"] = None
    with pytest.raises(InvariantError, match="invariant 1"):
        validate_label_table(bad)


def test_invariant2_non_mi_only_via_m1():
    df = mixed_table()
    assert not ((df["final_class"] == "non-MI") & (df["rule_id"] != "M1")).any()
    m10 = df[df["rule_id"] == "M10"].iloc[0]
    assert m10["status"] == "candidate" and pd.isna(m10["final_class"])
    bad = df.copy()
    i = bad.index[bad["record_id"] == "r0"][0]
    bad.loc[i, ["status", "final_class", "rule_id", "reviewer"]] = ["confirmed", "non-MI", "M4", "x"]
    with pytest.raises(InvariantError):
        validate_label_table(bad)


def test_invariant2_absent_code_never_non_mi():  # L1
    for r in (rec(label_source="none", codes=[]), rec(codes=[]), rec(codes=["UNLISTED"])):
        row = map_record(r, config=TEST_CONFIG)
        assert row["status"] == "unresolved" and row["rule_id"] == "M4"
        assert row["proposed_class"] is None and row["final_class"] is None


def test_invariant3_m5_to_m8_never_propose_stemi_nstemi():
    df = mixed_table()
    sub = df[df["rule_id"].isin(["M5", "M6", "M7", "M8"])]
    assert set(sub["rule_id"]) == {"M5", "M6", "M7", "M8"}
    assert not sub["proposed_class"].isin(["STEMI", "NSTEMI"]).any()
    assert set(sub.loc[sub["status"] == "candidate", "proposed_class"]) == {"MI_unspecified"}
    bad = df.copy()
    bad.loc[bad["rule_id"] == "M8", "proposed_class"] = "STEMI"
    with pytest.raises(InvariantError, match="invariant 3"):
        validate_label_table(bad)


def test_invariant4_original_label_byte_identical():
    weird = "  {'FAKE_MI_A': 100.0, 'NORM': 0.0}\t— ünïcode \n"
    r = rec(original_label=weird, codes=["FAKE_MI_A"])
    df = map_records([r], config=TEST_CONFIG)
    assert df.loc[0, "original_label"].encode() == weird.encode()
    assert r["original_label"] is weird  # input untouched
    row = map_record(rec(label_source="none", codes=[], original_label=None), config=TEST_CONFIG)
    assert row["original_label"] is None  # not coerced to "None"


def test_invariant5_loaders():
    df = mixed_table(pretraining_eligible={"code15": True})
    sup = supervised_rows(df)
    assert (sup["status"] == "confirmed").all() and len(sup) == 1
    pre = pretraining_rows(df)
    assert set(pre["dataset_id"]) == {"code15"} and len(pre) == 1
    assert pre["status"].iloc[0] == "unresolved"  # any status allowed for pretraining


def test_invariant6_excluded_rows_have_reason():
    df = mixed_table()
    ex = df[df["status"] == "excluded"]
    assert len(ex) == 1 and ex["exclusion_reason"].iloc[0] == "non_reducible_lead_set"
    with pytest.raises(ValueError, match="invariant 6"):
        map_record(rec(), technical_exclusion="  ")
    bad = df.copy()
    bad.loc[bad["status"] == "excluded", "exclusion_reason"] = None
    with pytest.raises(InvariantError, match="invariant 6"):
        validate_label_table(bad)


# --------------------------------------------------------------------------- specific rules


def test_m1_only_path_to_confirmed_and_overrides_codes():
    row = map_record(rec(codes=["FAKE_MI_A"]), review(final_class="non-MI"), config=TEST_CONFIG)
    assert (row["status"], row["final_class"], row["rule_id"]) == ("confirmed", "non-MI", "M1")
    assert row["reviewer"] == "rev_a" and row["review_date"] == "2026-10-19"


@pytest.mark.parametrize("kw, msg", [
    ({"reviewer": ""}, "reviewer"),
    ({"reviewer": None}, "reviewer"),
    ({"review_date": None}, "review_date"),
    ({"status": "unresolved"}, "iff"),                      # final_class without confirmed
    ({"final_class": None}, "iff"),                         # confirmed without final_class
    ({"final_class": "MI_unspecified"}, "final_class"),
    ({"status": "candidate", "final_class": None}, "status"),
    ({"status": "excluded", "final_class": None}, "exclusion_reason"),
])
def test_m1_rejects_invalid_reviews(kw, msg):
    with pytest.raises(InvalidReviewError, match=msg):
        review(**kw)


def test_m1_rejects_unvalidated_review_object():
    with pytest.raises(InvalidReviewError):
        map_record(rec(), review={"status": "confirmed", "final_class": "STEMI"})


def test_reviews_from_frame():
    frame = pd.DataFrame([
        {"dataset_id": "ptb_xl", "record_id": 5, "status": "confirmed", "final_class": "STEMI",
         "reviewer": "rev_a", "review_date": "2026-10-19", "exclusion_reason": None},
        {"dataset_id": "ptb_xl", "record_id": 6, "status": "excluded", "final_class": None,
         "reviewer": "rev_a", "review_date": "2026-10-19", "exclusion_reason": "reviewer_rejected"},
    ])
    reviews = reviews_from_frame(frame)
    assert reviews[("ptb_xl", "5")].final_class == "STEMI"
    with pytest.raises(InvalidReviewError):
        reviews_from_frame(frame.assign(reviewer=[None, "rev_a"]))
    with pytest.raises(InvalidReviewError, match="more than one"):
        reviews_from_frame(pd.concat([frame, frame]))


def test_m2_takes_reason_and_no_hardcoded_incart_exclusion():
    r = rec(dataset_id="incart", label_source="beat_annotation", codes=["N"], patient_key=None)
    assert map_record(r)["status"] == "unresolved"            # Q8 open: not auto-excluded
    row = map_record(r, technical_exclusion="holter_context")
    assert (row["status"], row["exclusion_reason"], row["rule_id"]) == (
        "excluded", "holter_context", "M2")


def test_m3_drops_records100_rows_entirely():  # O2
    records = [rec(record_id="1", file_path="records500/00000/00001_hr"),
               rec(record_id="1", file_path="records100/00000/00001_lr")]
    df = map_records(records, config=TEST_CONFIG)
    assert len(df) == 1 and (df["status"] != "excluded").all()
    assert map_record(records[1]) is None
    # even a review cannot resurrect a duplicate representation
    assert map_record(records[1], review()) is None


def test_m4_m5_m6_unresolved():
    df = mixed_table()
    for rid in ("r0", "r1", "r2", "r3", "r10"):
        row = df[df["record_id"] == rid].iloc[0]
        assert row["status"] == "unresolved" and pd.isna(row["proposed_class"])
    assert df[df["record_id"] == "r1"]["original_label"].iloc[0] == "ACUTE MI ?"


def test_m7_m8_fire_only_with_injected_lists():
    for codes, rule in ((["FAKE_ST_A"], "M7"), (["FAKE_MI_A"], "M8")):
        row = map_record(rec(codes=codes), config=TEST_CONFIG)
        assert (row["status"], row["proposed_class"], row["rule_id"]) == (
            "candidate", "MI_unspecified", rule)
        prod = map_record(rec(codes=codes))
        assert (prod["status"], prod["rule_id"]) == ("unresolved", "M4")
    # code lists are per dataset: a ptb_xl code does not match in sph
    row = map_record(rec(dataset_id="sph", label_source="aha_statement", codes=["FAKE_MI_A"]),
                     config=TEST_CONFIG)
    assert row["rule_id"] == "M4"


def test_m9_m10_need_window_and_timing():
    stemi = rec(dataset_id="mimic_iv_ecg", label_source="linked_clinical", codes=[],
                linked_diagnoses=["NSTEMI"], ecg_time="2026-01-01 10:00",
                event_time="2026-01-01 12:00")
    assert map_record(stemi, config=TEST_CONFIG)["proposed_class"] == "NSTEMI"
    prod = map_record(stemi)                                  # ACUTE_WINDOW None (Q2)
    assert prod["status"] == "unresolved" and "Q2" in prod["supporting_evidence"]
    late = {**stemi, "event_time": "2026-01-05 12:00"}
    assert map_record(late, config=TEST_CONFIG)["status"] == "unresolved"
    untimed = {**stemi, "ecg_time": None}
    assert map_record(untimed, config=TEST_CONFIG)["status"] == "unresolved"
    empty = {**stemi, "linked_diagnoses": []}
    assert map_record(empty, config=TEST_CONFIG)["rule_id"] == "M4"


def test_m11_conflicts_unresolved_with_evidence():
    cases = [
        ["STEMI", "NSTEMI"],
        ["STEMI", "no_acute_mi"],
    ]
    for dx in cases:
        r = rec(dataset_id="mimic_iv_ecg", label_source="linked_clinical", codes=[],
                linked_diagnoses=dx, ecg_time="2026-01-01 10:00", event_time="2026-01-01 11:00")
        row = map_record(r, config=TEST_CONFIG)
        assert (row["status"], row["rule_id"]) == ("unresolved", "M11")
        assert "conflict" in json.loads(row["supporting_evidence"])
    # MI statement code plus a contradicting linked negative diagnosis
    cfg = MappingConfig(mi_codes={"mimic_iv_ecg": frozenset({"FAKE_MI_C"})},
                        acute_window=within_24h)
    r = rec(dataset_id="mimic_iv_ecg", label_source="linked_clinical", codes=["FAKE_MI_C"],
            linked_diagnoses=["no_acute_mi"], ecg_time="2026-01-01 10:00",
            event_time="2026-01-01 11:00")
    row = map_record(r, config=cfg)
    assert row["rule_id"] == "M11" and "FAKE_MI_C" in row["supporting_evidence"]
    # conflicts are detected even in production config (no window)
    assert map_record({**r, "linked_diagnoses": ["STEMI", "NSTEMI"]})["rule_id"] == "M11"


def test_m12_configurable_and_off_by_default():
    r = rec(dataset_id="code15", label_source="header_comment", codes=["FAKE"], patient_key=None)
    assert map_record(r)["rule_id"] == "M4"
    cfg = MappingConfig(no_target_label_source=frozenset({"code15"}))
    row = map_record(r, config=cfg)
    assert (row["status"], row["rule_id"]) == ("unresolved", "M12")


def test_pretraining_eligible_defaults_false():  # L11
    df = mixed_table()
    assert df["pretraining_eligible"].dtype == bool and not df["pretraining_eligible"].any()
    assert pretraining_rows(df).empty


def test_s7_record_proxy_and_o11_overlap_groups():
    df = mixed_table()
    code = df[df["record_id"] == "r2"].iloc[0]
    assert (code["patient_key"], code["patient_key_quality"]) == ("r2", "record_proxy")
    ptb = df[df["record_id"] == "r5"].iloc[0]
    assert (ptb["patient_key"], ptb["patient_key_quality"]) == ("p1", "native")
    groups = lm.OVERLAP_GROUPS
    assert {groups[d] for d in ("ningbo", "chapman_shaoxing", "georgia",
                                "cpsc_2018", "cpsc_extra")} == {"challenge_2021"}
    assert groups["ptb_xl"] == "ptb_xl" and groups["incart"] == "incart"
    assert set(groups) == set(lm.DATASET_IDS)


def test_release_and_label_source_validated():
    with pytest.raises(ValueError):
        map_record(rec(release="1.0.3"))                      # V1: exact release string
    with pytest.raises(ValueError):
        map_record(rec(label_source="icd10"))
    assert map_record(rec())["release"] == "1.0.3, records500"
