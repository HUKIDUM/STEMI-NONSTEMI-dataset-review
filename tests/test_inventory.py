import json

import numpy as np
import pandas as pd
import pytest

import synthetic as syn
from stemi.inventory import (
    INVENTORY_COLUMNS, OBSERVATION_TYPE, Code15Shard, inventory_challenge, inventory_code15,
    inventory_mimic_iv_ecg, inventory_ptb_diagnostic, inventory_ptb_xl,
    is_duplicate_representation, standard12_channel_map, write_inventory,
)
from stemi.registry import REGISTRY

ORIGIN = "synthetic_fixture"


def _common_checks(df, ds):
    assert list(df.columns) == INVENTORY_COLUMNS
    assert (df["dataset_id"] == ds).all()
    assert (df["release"] == REGISTRY[ds].release).all()          # V1
    assert (df["observation_type"] == OBSERVATION_TYPE).all()     # E3
    assert (df["data_origin"] == ORIGIN).all()
    assert df["target_rate"].isna().all()                         # C1.3, Q9
    assert df["acquisition_rate"].isna().all()                    # P5: not inferred
    assert df["filter_raw"].isna().all()


# ---------------------------------------------------------------- PTB-XL

def test_ptb_xl_uses_records500_only(tmp_path):  # C2.1, O2
    meta = syn.make_ptb_xl(tmp_path, n=4)
    assert (tmp_path / "records100").is_dir()
    df = inventory_ptb_xl(tmp_path, data_origin=ORIGIN)
    _common_checks(df, "ptb_xl")
    assert len(df) == len(meta) == 4
    assert df["file_path"].str.startswith("records500/").all()
    assert not df["file_path"].str.contains("records100").any()
    assert df["record_id"].is_unique
    assert (df["native_rate"] == 500).all() and (df["original_duration_s"] == 10).all()
    assert df["patient_key"].tolist() == ["100", "100", "101", "101"]
    assert df["conflicts"].isna().all()


def test_ptb_xl_rejects_records100_path(tmp_path):
    meta = syn.make_ptb_xl(tmp_path, n=2)
    meta.loc[0, "filename_hr"] = meta.loc[0, "filename_lr"]
    meta.to_csv(tmp_path / "ptbxl_database.csv", index=False)
    with pytest.raises(ValueError, match="records500"):
        inventory_ptb_xl(tmp_path, data_origin=ORIGIN)


def test_duplicate_representation_guard():
    assert is_duplicate_representation("ptb_xl", "records100/00000/00001_lr")
    assert not is_duplicate_representation("ptb_xl", "records500/00000/00001_hr")


def test_header_conflict_never_updates_registry(tmp_path):  # E2, E3, P3
    syn.make_ptb_xl(tmp_path, n=2, fs_hr=250)
    df = inventory_ptb_xl(tmp_path, data_origin=ORIGIN)
    assert (df["native_rate"] == 250).all()
    assert df["conflicts"].str.contains("registry unchanged").all()
    assert (df["registry_hz"] == 500).all()
    assert REGISTRY["ptb_xl"].publisher_hz == 500


def test_missing_header_recorded_not_replaced(tmp_path):
    syn.make_ptb_xl(tmp_path, n=2)
    (tmp_path / "records500/00000/00002_hr.hea").unlink()
    df = inventory_ptb_xl(tmp_path, data_origin=ORIGIN)
    assert df["header_found"].tolist() == [True, False]
    assert pd.isna(df.loc[1, "native_rate"])
    assert "missing" in df.loc[1, "conflicts"]


def test_bounded_selection_is_seeded(tmp_path):
    syn.make_ptb_xl(tmp_path, n=10)
    a = inventory_ptb_xl(tmp_path, data_origin=ORIGIN, limit=3, seed=7)
    b = inventory_ptb_xl(tmp_path, data_origin=ORIGIN, limit=3, seed=7)
    assert len(a) == 3 and a["record_id"].tolist() == b["record_id"].tolist()
    assert "seed=7" in a.loc[0, "selection_rule"]


def test_data_origin_required_and_validated(tmp_path):
    syn.make_ptb_xl(tmp_path, n=1)
    with pytest.raises(ValueError):
        inventory_ptb_xl(tmp_path, data_origin="real")


# ---------------------------------------------------------------- MIMIC

def test_mimic_keys_and_layout(tmp_path):
    meta = syn.make_mimic(tmp_path, n=3)
    df = inventory_mimic_iv_ecg(tmp_path, data_origin=ORIGIN)
    _common_checks(df, "mimic_iv_ecg")
    assert df["record_id"].tolist() == meta["study_id"].astype(str).tolist()
    assert df["patient_key"].tolist() == meta["subject_id"].astype(str).tolist()
    assert (df["patient_key_field"] == "subject_id").all()
    assert df["file_path"].str.match(r"files/p\d{4}/p\d+/s\d+/\d+$").all()
    assert "cart_id" not in df.columns and "device_model" not in df.columns  # C2.6


# ---------------------------------------------------------------- CODE-15%

def test_code15_joins_on_exam_id_not_row_order(tmp_path):  # C2.2
    exams = syn.make_code15(tmp_path)
    h5_ids = np.load(tmp_path / "exams_part0_exam_id.npy")
    assert exams["exam_id"].tolist() != list(h5_ids)  # fixture really is out of order

    df = inventory_code15(tmp_path, data_origin=ORIGIN)
    _common_checks(df, "code15")
    assert len(df) == 4
    for _, r in df.iterrows():
        assert exams.loc[r["metadata_row"], "exam_id"] == h5_ids[r["shard_row"]] == int(r["record_id"])
    assert df["patient_key"].isna().all()  # only exam_id given in PDFs


def test_code15_stored_length_not_observed_duration(tmp_path):  # C2.2
    syn.make_code15(tmp_path)
    df = inventory_code15(tmp_path, data_origin=ORIGIN)
    assert df["stored_duration_s"].tolist() == pytest.approx([10.24] * 4)
    assert df["original_duration_s"].isna().all()   # padding interpretation unresolved
    assert df["padding_mask"].isna().all()
    assert df["padding_status"].str.contains("unresolved").all()
    assert (df["native_rate_source"] == "registry_documentary").all()
    assert (df["n_samples"] == 4096).all() and (df["n_channels"] == 12).all()


def test_code15_custom_shard_reader(tmp_path):
    exams = syn.make_code15(tmp_path)

    def reader(_root):
        yield Code15Shard("fake", (2, 4096, 12), np.array([303, 999]))

    df = inventory_code15(tmp_path, data_origin=ORIGIN, shard_reader=reader)
    assert exams.loc[df.loc[0, "metadata_row"], "exam_id"] == 303
    assert "not found" in df.loc[1, "conflicts"]


def test_code15_unmatched_exam_flagged(tmp_path):
    syn.make_code15(tmp_path)
    exams = pd.read_csv(tmp_path / "exams.csv")
    exams[exams["exam_id"] != 302].to_csv(tmp_path / "exams.csv", index=False)
    df = inventory_code15(tmp_path, data_origin=ORIGIN)
    bad = df[df["record_id"] == "302"].iloc[0]
    assert pd.isna(bad["metadata_row"]) and "not found" in bad["conflicts"]


def test_code15_without_exam_id_refuses_positional_join(tmp_path):
    np.save(tmp_path / "x_tracings.npy", np.zeros((2, 4096, 12), dtype=np.float32))
    pd.DataFrame({"exam_id": [1, 2]}).to_csv(tmp_path / "exams.csv", index=False)
    with pytest.raises(ValueError, match="row-position"):
        inventory_code15(tmp_path, data_origin=ORIGIN)


# ---------------------------------------------------------------- PTB Diagnostic

def test_ptb_diagnostic_15_channels_standard12_identified(tmp_path):  # C2.3
    recs = syn.make_ptb_diagnostic(tmp_path)
    df = inventory_ptb_diagnostic(tmp_path, data_origin=ORIGIN)
    _common_checks(df, "ptb_diagnostic")
    assert df["record_id"].tolist() == recs
    assert df["patient_key"].tolist() == ["patient001", "patient002"]
    assert (df["n_channels"] == 15).all()
    assert (df["native_rate"] == 1000).all()          # no 1000→500 conversion applied
    for v in df["standard12_channel_map"]:
        assert json.loads(v) == dict(zip(syn.LEADS_12, range(12)))
    assert df["conflicts"].isna().all()


def test_standard12_identification_keeps_native_order():
    assert standard12_channel_map(syn.PTB_DIAG_15) == dict(zip(syn.LEADS_12, range(12)))
    shuffled = ["vx"] + syn.LEADS_12[::-1]
    m = standard12_channel_map(shuffled)
    assert m["I"] == 12 and m["V6"] == 1          # lead identity survives a reordered file (P4)
    assert standard12_channel_map(syn.LEADS_12[:11]) is None


# ---------------------------------------------------------------- Challenge (optional)

def test_challenge_headers_only(tmp_path):
    syn.make_challenge(tmp_path / "ningbo")
    df = inventory_challenge("ningbo", tmp_path / "ningbo", data_origin=ORIGIN)
    val = np.load(tmp_path / "ningbo" / "JS00001_val.npy", mmap_mode="r")
    assert val.shape == (df.loc[0, "n_channels"], df.loc[0, "n_samples"])  # C2.4 leads x samples
    _common_checks(df, "ningbo")
    assert df["record_id"].tolist() == ["JS00001", "JS00002"]
    assert df["patient_key"].isna().all()
    assert (df["n_channels"] == 12).all() and (df["native_rate"] == 500).all()
    with pytest.raises(ValueError):
        inventory_challenge("ptb_xl", tmp_path, data_origin=ORIGIN)


# ---------------------------------------------------------------- output

def test_write_inventory_refuses_overwrite(tmp_path):  # P3, V5
    syn.make_mimic(tmp_path / "m", n=1)
    df = inventory_mimic_iv_ecg(tmp_path / "m", data_origin=ORIGIN)
    out = tmp_path / "inventory.csv"
    write_inventory(df, out)
    with pytest.raises(FileExistsError):
        write_inventory(df, out)
