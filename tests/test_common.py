"""common.provenance: manifest de-duplication on local_path."""

import csv

from stemi.review import common


def test_provenance_prefers_downloaded_row(tmp_path, monkeypatch):
    monkeypatch.setattr(common, "PROJECT_ROOT", tmp_path)
    m = tmp_path / "manifest.csv"
    cols = ["dataset_id", "url", "local_path", "sha256", "download_utc", "status", "checksum_match"]
    with open(m, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerow({"local_path": "data/x.hea", "sha256": "aa", "download_utc": "T1",
                    "status": "downloaded", "checksum_match": "yes"})
        w.writerow({"local_path": "data/x.hea", "sha256": "aa", "download_utc": "T2",
                    "status": "skipped_exists", "checksum_match": "not available"})
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "x.hea").write_text("x")
    row = common.provenance([tmp_path / "data" / "x.hea"], m).iloc[0]
    assert row["download_utc"] == "T1" and row["checksum_match"] == "yes"


def test_read_text_csv_keeps_literal_na(tmp_path):
    p = tmp_path / "t.csv"
    p.write_text("a,b\nn/a,NA\n,x\n")
    df = common.read_text_csv(p)
    assert df.loc[0, "a"] == "n/a" and df.loc[0, "b"] == "NA"
    assert df["a"].isna().tolist() == [False, True]          # empty cell is still missing
