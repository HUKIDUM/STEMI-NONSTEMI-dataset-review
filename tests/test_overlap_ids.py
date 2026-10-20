"""overlap_ids on invented RECORDS lists (no real data)."""

import pandas as pd

from stemi.review import overlap_ids as ov


def test_ptbxl_number_overlap(tmp_path):
    s = tmp_path
    (s / "ptb_xl").mkdir()
    pd.DataFrame({"ecg_id": [1, 2, 4]}).to_csv(s / "ptb_xl" / "ptbxl_database.csv", index=False)
    g = s / "ptb_xl" / "challenge-2021" / "training" / "ptb-xl" / "g1"
    g.mkdir(parents=True)
    (g / "RECORDS").write_text("HR00001\nHR00002\nHR00003\n")
    rows = {r["check"]: r["result"] for r in ov.ptbxl_check(s)}
    assert rows["ptb_xl: numbers in both (IF HRn = ecg_id n; ASSUMPTION)"] == 2
    assert rows["ptb_xl: challenge-only numbers (first 40)"] == "3"
    assert rows["ptb_xl: native ecg_id not in challenge"] == 1
    assert rows["ptb_xl: challenge name prefixes"] == "HR"


def test_missing_inputs_reported(tmp_path):
    out = ov.review(tmp_path, tmp_path / "out")
    assert out["result"].astype(str).str.contains("not run").any()
    assert (tmp_path / "out" / "overlap_ids_summary.md").exists()


def test_ptbdb_counts_only(tmp_path):
    (tmp_path / "ptb_diagnostic").mkdir()
    (tmp_path / "ptb_diagnostic" / "RECORDS").write_text("patient001/s0010_re\npatient002/s0015lre\n")
    g = tmp_path / "ptb_diagnostic" / "challenge-2021" / "training" / "ptb" / "g1"
    g.mkdir(parents=True)
    (g / "RECORDS").write_text("S0001\nS0002\n")
    rows = {r["check"]: r["result"] for r in ov.ptbdb_check(tmp_path)}
    assert rows["ptb_diagnostic: challenge names equal to a native record stem"] == 0
    assert rows["ptb_diagnostic: record-level mapping"].startswith("not possible")
