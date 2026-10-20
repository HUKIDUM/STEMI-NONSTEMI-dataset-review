"""mimic_icd_count on invented MIMIC-shaped tables (no real data, no credentialed files)."""

import pandas as pd
import pytest

from stemi.review import mimic_icd_count as mic

SUP = mic.SUPPRESSED


def _fixture(tmp_path):
    """Invented: 12 admissions with I2101 (seq 1) + 11 with I2111 (seq 2), one ECG inside
    each stay; one admission with I214 + I213 whose ECG is outside the stay; one ICD-9 4107x."""
    adm, dx, rec = [], [], []
    hadm = 1000
    for code, n, seq in (("I2101", 12, 1), ("I2111", 11, 2)):
        for i in range(n):
            s = 100 + hadm
            adm.append((s, hadm, "2150-01-01 10:00", "2150-01-05 10:00"))
            dx.append((s, hadm, seq, code, 10))
            rec.append((s, 50000 + hadm, "2150-01-02 08:00"))
            hadm += 1
    adm.append((900, 9000, "2150-01-01 10:00", "2150-01-03 10:00"))
    dx += [(900, 9000, 1, "I214", 10), (900, 9000, 2, "I213", 10)]
    rec.append((900, 99000, "2150-02-01 08:00"))                       # outside the stay
    adm.append((901, 9001, "2150-01-01 10:00", "2150-01-03 10:00"))
    dx += [(901, 9001, 3, "41071", 9), (901, 9001, 1, "I214", 9),      # wrong version: ignored
           (901, 9001, 4, "4280", 9)]                                   # not MI: ignored
    files = {}
    for name, rows, cols in [
        ("admissions.csv.gz", adm, ["subject_id", "hadm_id", "admittime", "dischtime"]),
        ("diagnoses_icd.csv.gz", dx, ["subject_id", "hadm_id", "seq_num", "icd_code", "icd_version"]),
        ("record_list.csv", rec, ["subject_id", "study_id", "ecg_time"]),
    ]:
        p = tmp_path / name
        pd.DataFrame(rows, columns=cols).to_csv(p, index=False)
        files[name] = p
    return files


def _args(files, *extra):
    return ["--diagnoses", str(files["diagnoses_icd.csv.gz"]),
            "--admissions", str(files["admissions.csv.gz"]),
            "--records", str(files["record_list.csv"]), *extra]


def _cell(codes, group, position="any position", metric="admissions"):
    r = codes[(codes["group"] == group) & (codes["position"] == position)]
    return r.iloc[0][metric]


STEMI_B = "ICD-10 I21.0-I21.3 (I210*-I213*)"


def test_buckets_and_raw_counts(tmp_path):
    f = _fixture(tmp_path)
    res = mic.run(f["diagnoses_icd.csv.gz"], f["admissions.csv.gz"], f["record_list.csv"])
    raw = res["_raw"]
    r = raw[(raw["group"] == STEMI_B) & (raw["position"] == "any position")].iloc[0]
    assert r["admissions"] == 24 and r["ecgs_linked"] == 23     # mixed admission's ECG is outside
    assert _cell(raw, STEMI_B, "seq_num == 1") == 12
    assert _cell(raw, "I210") == 12 and _cell(raw, "I211") == 11 and _cell(raw, "I213") == 1
    assert _cell(raw, "ICD-10 I21.4 (I214*)") == 1               # the ICD-9 'I214' is not counted
    assert _cell(raw, "ICD-9 410*") == 1
    assert res["inputs"]["rows_read"].tolist() == [28, 25, 24]


def test_primary_and_secondary_suppression(tmp_path):
    f = _fixture(tmp_path)
    codes = mic.run(f["diagnoses_icd.csv.gz"], f["admissions.csv.gz"], f["record_list.csv"])["codes"]
    assert _cell(codes, STEMI_B) == "24"
    assert _cell(codes, "I213") == SUP                           # primary (<10)
    assert _cell(codes, "I211") == SUP                           # secondary: smallest visible sibling
    assert _cell(codes, "I210") == "12"
    assert _cell(codes, "ICD-10 I21.4 (I214*)") == SUP
    assert _cell(codes, mic.BOTH) == SUP


def test_suppress_family_rules():
    assert mic.suppress_family(30, [25, 5]) == ("30", [SUP, SUP])
    assert mic.suppress_family(40, [20, 15, 5]) == ("40", ["20", SUP, SUP])
    assert mic.suppress_family(40, [20, 20]) == ("40", ["20", "20"])
    assert mic.suppress_family(8, [5, 3]) == (SUP, [SUP, SUP])
    assert mic.suppress_family(9, []) == (SUP, [])


def test_ecg_context_not_back_calculable(tmp_path):
    f = _fixture(tmp_path)
    ctx = mic.run(f["diagnoses_icd.csv.gz"], f["admissions.csv.gz"],
                  f["record_list.csv"])["context"].set_index("item")["count"]
    assert ctx["ECGs total (record_list)"] == "24"
    assert ctx["ECGs not linked (outside every admit-discharge window)"] == SUP   # 1
    assert ctx["ECGs linked to any admission"] == SUP                              # secondary


def test_printed_output_has_no_ids_or_dates(tmp_path, capsys):
    f = _fixture(tmp_path)
    mic.main(_args(f, "--versions", "TEST-HOSP 9.9; TEST-ECG 1.0"))
    out = capsys.readouterr().out
    assert "TEST-HOSP 9.9; TEST-ECG 1.0" in out
    for caveat in mic.CAVEATS:
        assert caveat in out
    assert "https://physionet.org/content/mimic-iv-ecg/1.0/" in out
    assert "rows_read" in out
    for ident in ["1100", "1000", "51000", "9000", "99000", "2150"]:
        assert ident not in out


def test_out_file_new_only_and_aggregate(tmp_path):
    f = _fixture(tmp_path)
    out = tmp_path / "agg.csv"
    mic.main(_args(f, "--out", str(out)))
    text = out.read_text()
    assert text.startswith("# versions:") and all(c in text for c in mic.CAVEATS)
    assert text and "51000" not in text and "2150" not in text
    with pytest.raises(SystemExit):
        mic.main(_args(f, "--out", str(out)))


def test_chunked_read(tmp_path, monkeypatch):
    monkeypatch.setattr(mic, "CHUNK_ROWS", 3)
    f = _fixture(tmp_path)
    res = mic.run(f["diagnoses_icd.csv.gz"], f["admissions.csv.gz"], f["record_list.csv"])
    assert res["inputs"]["rows_read"].tolist() == [28, 25, 24]
    assert _cell(res["_raw"], STEMI_B) == 24


def test_bucket_of():
    assert mic.bucket_of("I2109", 10) == (STEMI_B, "I210")
    assert mic.bucket_of("I214", 10)[0] == "ICD-10 I21.4 (I214*)"
    assert mic.bucket_of("I21A1", 10) == ("ICD-10 other I21 (not I210-I214)", "I21A1")
    assert mic.bucket_of("I222", 10) == ("ICD-10 I22*", "I222")
    assert mic.bucket_of("41071", 9) == ("ICD-9 410*", "4107")
    assert mic.bucket_of("I214", 9) is None and mic.bucket_of("4280", 9) is None


def _table_for(tmp_path, dx_rows):
    adm = pd.DataFrame([(1, h, "2150-01-01", "2150-01-09") for h in range(len(dx_rows))],
                       columns=["subject_id", "hadm_id", "admittime", "dischtime"])
    dx = pd.DataFrame([(1, h, 1, c, v) for h, (c, v) in enumerate(dx_rows)],
                      columns=["subject_id", "hadm_id", "seq_num", "icd_code", "icd_version"])
    rec = pd.DataFrame([(1, 7, "2150-01-02")], columns=["subject_id", "study_id", "ecg_time"])
    for name, df in [("a.csv", adm), ("d.csv", dx), ("r.csv", rec)]:
        df.to_csv(tmp_path / name, index=False)
    return mic.run(tmp_path / "d.csv", tmp_path / "a.csv", tmp_path / "r.csv")["_raw"]


def test_unknown_i21_subcode_goes_to_other_with_breakdown(tmp_path):
    raw = _table_for(tmp_path, [("I21B9", 10), ("I21", 10), ("I219", 10), ("I210", 10)])
    other = "ICD-10 other I21 (not I210-I214)"
    assert _cell(raw, other) == 3
    subs = raw[(raw["level"] == "sub-code") & raw["group"].isin(["I21B9", "I21", "I219"])]
    assert len(subs[subs["position"] == "any position"]) == 3


def test_icd9_410_split_by_fourth_digit(tmp_path):
    raw = _table_for(tmp_path, [("41071", 9), ("41072", 9), ("41001", 9), ("4109", 9)])
    assert _cell(raw, "ICD-9 410*") == 4
    assert _cell(raw, "4107") == 2 and _cell(raw, "4100") == 1 and _cell(raw, "4109") == 1
