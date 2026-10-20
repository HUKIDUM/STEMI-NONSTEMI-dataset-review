"""review_sph on invented SPH-shaped CSVs (no real data; codes and texts are made up)."""

import pandas as pd
import pytest

from stemi.review import review_sph as rs


@pytest.fixture
def root(tmp_path):
    r = tmp_path / "sph"
    r.mkdir()
    pd.DataFrame({"ECG_ID": ["A1", "A2", "A3", "A4"],
                  "AHA_Code": ["1", "22;160+330", "160+332", "50"],
                  "Patient_ID": ["P1", "P1", "P2", "P3"],
                  "Age": ["50", "50", "70", "30"], "Sex": ["M", "M", "F", "F"],
                  "N": ["5000", "5000", "7500", "5000"]}).to_csv(r / "metadata.csv", index=False)
    pd.DataFrame({"Code": ["1", "22", "50", "160", "330", "332"],
                  "Description": ["Normal ECG", "Sinus tachycardia", "Fake ST change",
                                  "Fake anterior MI", "Acute", "Old"]}).to_csv(r / "code.csv", index=False)
    return r


def test_primary_and_modifier_counts(root, tmp_path):
    res = rs.review(root, tmp_path / "out")
    p = res["primary"].set_index("code")
    assert p.loc["160", "n_ecgs"] == 2 and p.loc["160", "n_patients"] == 2
    pairs = res["pairs"].set_index(["code", "modifier"])
    assert pairs.loc[("160", "330"), "n_ecgs"] == 1
    assert pairs.loc[("160", "332"), "modifier_description"] == "Old"
    assert res["mi_codes"] == ["160"]


def test_basics(root, tmp_path):
    b = rs.review(root, tmp_path / "out")["basics"]
    assert b["distinct patients"] == 3
    assert b["code fields containing ';' / '+'"] == "1 / 2"
    assert b["N / 500 s (500 Hz per [MCR p.3]) min / median / max"] == "10 / 10 / 15"
    assert b["primary codes not in code.csv"] == "none"
    assert (tmp_path / "out" / "sph_summary.md").exists()
