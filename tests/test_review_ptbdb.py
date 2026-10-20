"""review_ptbdb on invented PTB-Diagnostic-shaped headers (no real data)."""

import pytest

import synthetic as syn
from stemi.review import review_ptbdb as rp


@pytest.fixture
def root(tmp_path):
    r = tmp_path / "ptbdb"
    r.mkdir()
    syn.write_hea(r / "patient001" / "s0010_re.hea", "s0010_re", 1000, 38400, syn.PTB_DIAG_15,
                  comments=["age: 81", "sex: female", "ECG date: 01/10/1990",
                            "Reason for admission: Myocardial infarction",
                            "Acute infarction (localization): infero-latera",
                            "Former infarction (localization): no",
                            "Infarction date (acute): 29-Sep-90"])
    syn.write_hea(r / "patient001" / "s0014lre.hea", "s0014lre", 1000, 115200, syn.PTB_DIAG_15,
                  comments=["ECG date: 15/10/1990", "Reason for admission: Myocardial infarction",
                            "Infarction date (acute): 29-Sep-90"])
    syn.write_hea(r / "patient104" / "s0306lre.hea", "s0306lre", 1000, 115200, syn.PTB_DIAG_15,
                  comments=["ECG date: n/a", "Reason for admission: Healthy control"])
    (r / "RECORDS").write_text("patient001/s0010_re\npatient001/s0014lre\npatient104/s0306lre\n"
                               "patient999/s9999_re\n")
    (r / "CONTROLS").write_text("patient104/s0306lre\n")
    return r


def test_records_and_keys(root, tmp_path):
    res = rp.review(root, tmp_path / "out")
    b = res["basics"]
    assert b["records in RECORDS"] == 4 and b["headers found"] == 3
    assert b["distinct patient folders (RECORDS)"] == 3
    assert b["records with all standard 12 leads by name"] == 3
    assert res["keys"]["reason"] == "Reason for admission"
    assert res["keys"]["infarct_date"] == "Infarction date (acute)"


def test_reason_counts_by_patient(root, tmp_path):
    c = rp.review(root, tmp_path / "out")["counts"]
    r = c[(c["key"] == "Reason for admission") & (c["value"] == "Myocardial infarction")].iloc[0]
    assert (r["n_records"], r["n_patients"]) == (2, 1)


def test_mi_timing_days(root, tmp_path):
    t = rp.review(root, tmp_path / "out")["timing"]
    assert sorted(t["days_ecg_minus_infarction"].tolist()) == [2, 16]
    assert (tmp_path / "out" / "ptb_diagnostic_summary.md").exists()


def test_parse_date_formats():
    assert rp.parse_date("29-Sep-90").year == 1990
    assert rp.parse_date("01/10/1990").month == 10
    assert rp.parse_date("n/a") is None
