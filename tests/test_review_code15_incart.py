"""review_code15 / review_incart on invented files (no real data)."""

import pandas as pd

import synthetic as syn
from stemi.review import review_code15 as rc15
from stemi.review import review_incart as ri


def test_code15_label_sums(tmp_path):
    r = tmp_path / "code15"
    r.mkdir()
    pd.DataFrame({"exam_id": [1, 2, 3], "age": [50, 60, 70], "is_male": [True, False, True],
                  "1dAVb": [True, False, False], "AF": [False, False, True],
                  "normal_ecg": [False, True, False], "death": [False, None, True],
                  "patient_id": [9, 9, 8], "trace_file": ["exams_part0.hdf5"] * 3}
                 ).to_csv(r / "exams.csv", index=False)
    res = rc15.review(r, tmp_path / "out")
    lab = res["labels"].set_index("column")
    assert lab.loc["AF", "n_true"] == 1 and lab.loc["1dAVb", "n_patients_true"] == 1
    assert lab.loc["death", "n_missing"] == 1
    assert "age" not in lab.index and "patient_id" not in lab.index
    b = res["basics"]
    assert b["distinct patient_id"] == 2
    assert b["column names matching MI regex"] == "none"


def test_incart_headers_and_text(tmp_path):
    r = tmp_path / "incart"
    syn.write_hea(r / "I01.hea", "I01", 257, 462600, syn.LEADS_12,
                  comments=["<age>: 65 <sex>: F <diagnoses> fake coronary artery disease"])
    (r / "RECORDS").write_text("I01\nI02\n")
    (r / "files-patients-diagnoses.txt").write_text("Patient 1: fake acute MI\nPatient 2: none\n")
    res = ri.review(r, tmp_path / "out")
    assert res["basics"]["headers read"] == 1
    assert res["basics"]["duration s min / max"] == "1800 / 1800"
    assert res["infarct_lines"] == ["files-patients-diagnoses.txt: Patient 1: fake acute MI"]
    assert "not downloaded" in (tmp_path / "out" / "incart_summary.md").read_text()
