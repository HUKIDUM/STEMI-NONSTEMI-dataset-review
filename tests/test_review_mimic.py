"""review_mimic on an invented MIMIC-IV-ECG-shaped folder (no real data)."""

import pandas as pd
import pytest

from stemi.review import review_mimic as rm


@pytest.fixture
def root(tmp_path):
    r = tmp_path / "mimic"
    r.mkdir()
    pd.DataFrame({"subject_id": [1, 1, 2], "study_id": [11, 12, 21],
                  "path": ["files/p1000/p1/s11/11", "files/p1000/p1/s12/12", "files/p1000/p2/s21/21"]}
                 ).to_csv(r / "record_list.csv", index=False)
    pd.DataFrame({
        "subject_id": [1, 1, 2], "study_id": [11, 12, 21], "cart_id": ["6848", "6848", None],
        "bandwidth": ["0.5-150 Hz"] * 3, "filtering": ["60 Hz notch Baseline filter", None, None],
        "report_0": ["Sinus rhythm", "Sinus rhythm", "Sinus tachycardia"],
        "report_1": ["Inferior infarct - age undetermined", "*** ACUTE MI ***", None],
        "report_2": [" Sinus rhythm", "ST elevation, consider anterior injury", None],
    }).to_csv(r / "machine_measurements.csv", index=False)
    pd.DataFrame({"subject_id": [1], "study_id": [11], "note_id": ["1-RE-1"]}
                 ).to_csv(r / "waveform_note_links.csv", index=False)
    d = r / "files" / "p1000" / "p1" / "s11"
    d.mkdir(parents=True)
    (d / "11.hea").write_text("11 2 500 5000\n11.dat 16 200/mV 16 0 0 0 0 I\n11.dat 16 200/mV 16 0 0 0 0 II\n")
    return r


def test_statements_and_flags(root, tmp_path):
    res = rm.review(root, tmp_path / "out")
    s = res["statements"].set_index("statement")
    assert s.loc["Sinus rhythm", "n_ecgs"] == 2          # stripped and de-duplicated per ECG
    assert s.loc["*** ACUTE MI ***", "kw_infarct"] and s.loc["*** ACUTE MI ***", "kw_acute"]
    assert s.loc["ST elevation, consider anterior injury", "kw_st_elev"]
    f = res["flags"].set_index("keyword_flag")
    assert f.loc["kw_infarct", "n_ecgs"] == 2 and f.loc["kw_infarct", "n_subjects"] == 1
    assert f.loc["any_mi_st_keyword", "n_ecgs"] == 2


def test_basics_fields_headers(root, tmp_path):
    out = tmp_path / "out"
    res = rm.review(root, out)
    b = res["basics"]
    assert b["distinct subject_id (record_list)"] == 2
    assert b["share of record_list ECGs with a note_id"] == "0.3333"
    f = res["fields"]
    assert set(f.loc[f["field"] == "cart_id", "value"]) == {"6848", "<missing>"}   # raw strings
    assert res["headers"].iloc[0]["units"] == "mV"
    text = (out / "mimic_iv_ecg_summary.md").read_text()
    assert "shifted" in text and "L2" in text


def test_without_machine_measurements(root, tmp_path):
    (root / "machine_measurements.csv").rename(root / "mm_hidden.csv")
    out = tmp_path / "out"
    res = rm.review(root, out)
    assert res["statements"] is None
    assert res["basics"]["distinct subject_id (record_list)"] == 2
    assert "not downloaded" in (out / "mimic_iv_ecg_summary.md").read_text()
