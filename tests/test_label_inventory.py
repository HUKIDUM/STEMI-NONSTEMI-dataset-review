"""label_inventory on invented files (no real data)."""

import pandas as pd

import synthetic as syn
from stemi.review import label_inventory as li


def test_code15_rows(tmp_path):
    (tmp_path / "code15").mkdir()
    pd.DataFrame({"exam_id": [1, 2, 3], "patient_id": [5, 5, 6],
                  **{c: [True, False, True] for c in li.CODE15_LABELS}}).to_csv(
        tmp_path / "code15" / "exams.csv", index=False)
    raw = li.inv_code15(tmp_path)
    assert list(raw.columns) == li.INV_COLUMNS
    df = raw.set_index("code")
    assert df.loc["ST", "count"] == 2 and df.loc["ST", "n_patients"] == 2
    assert "NOT ST elevation" in df.loc["ST", "extra"]


def test_incart_parsing_with_crlf(tmp_path):
    d = tmp_path / "incart"
    d.mkdir()
    (d / "files-patients-diagnoses.txt").write_text(
        "patient 1\r\nI01 I02\r\nAcute MI\r\npatient 2\r\nI03\r\n\r\npatient 3\r\nI04\r\nCAD, hypertension\r\n")
    (d / "record-descriptions.txt").write_text("I01\r\nPVCs, ST elevation\r\nI02\r\nPVCs\r\n")
    df = li.inv_incart(tmp_path)
    raw = df[df["label_kind"] == "patient diagnosis (raw text)"].set_index("label_as_written")
    assert raw.loc["Acute MI", "count"] == 2 and raw.loc["(no diagnosis text)", "n_patients"] == 1
    terms = df[df["label_kind"] == "record description term"].set_index("label_as_written")["count"]
    assert terms["PVCs"] == 2 and terms["ST elevation"] == 1
    split = df[df["label_kind"].str.startswith("patient diagnosis term")]["label_as_written"].tolist()
    assert split == ["CAD", "hypertension"]


def test_ptbdb_keeps_literal_text(tmp_path):
    r = tmp_path / "ptb_diagnostic"
    syn.write_hea(r / "patient001" / "s0001_re.hea", "s0001_re", 1000, 1000, syn.PTB_DIAG_15,
                  comments=["Reason for admission: n/a"])
    syn.write_hea(r / "patient002" / "s0002_re.hea", "s0002_re", 1000, 1000, syn.PTB_DIAG_15,
                  comments=["Reason for admission: Myocardial infarction",
                            "Former infarction (localization): no"])
    (r / "RECORDS").write_text("patient001/s0001_re\npatient002/s0002_re\n")
    df = li.inv_ptb_diagnostic(tmp_path)
    reasons = df[df["label_kind"] == "header comment: Reason for admission"]["label_as_written"].tolist()
    assert "n/a" in reasons
    former = df[df["label_kind"] == "header comment: Former infarction (localization)"]
    assert set(former["label_as_written"]) == {"no", li.KEY_MISSING}
