"""review_challenge on invented Challenge-2021-shaped headers (codes/names are made up)."""

import pandas as pd
import pytest

import synthetic as syn
from stemi.review import review_challenge as rc


@pytest.fixture
def root(tmp_path):
    r = tmp_path / "georgia"
    g1 = r / "training" / "georgia" / "g1"
    recs = [("E00001", 5000, "Age: 60|Sex: Male|Dx: 111,222"),
            ("E00002", 2500, "Age: NaN|Sex: Female|Dx: 333"),
            ("E00003", 5000, "Age: 70|Sex: Male|Dx: 999")]
    for name, n, comments in recs:
        syn.write_hea(g1 / f"{name}.hea", name, 500, n, syn.LEADS_12,
                      comments=comments.split("|"))
    (g1 / "RECORDS").write_text("\n".join(r_[0] for r_ in recs) + "\n")
    maps = tmp_path / "maps"
    maps.mkdir()
    pd.DataFrame({"Dx": ["fake myocardial infarction", "fake sinus rhythm"],
                  "SNOMEDCTCode": ["111", "222"], "Abbreviation": ["MI", "SR"]}
                 ).to_csv(maps / "dx_mapping_scored.csv", index=False)
    pd.DataFrame({"Acronym Name": ["STE"], "Full Name": ["fake ST elevation"],
                  "Snomed_CT": ["333"]}).to_csv(maps / "ConditionNames_SNOMED-CT.csv", index=False)
    return r, maps


def test_dx_counts_and_mapping(root, tmp_path):
    r, maps = root
    res = rc.review("georgia", r, maps, tmp_path / "out")
    dx = res["dx"].set_index("code")
    assert dx.loc["111", "name"] == "fake myocardial infarction" and dx.loc["111", "kw_infarct"]
    assert dx.loc["333", "map_source"] == "ConditionNames_SNOMED-CT.csv" and dx.loc["333", "kw_st_elev"]
    assert dx.loc["999", "name"] == "unmapped"
    assert res["mi_records"] == 2
    assert res["basics"]["unmapped codes"] == "999"


def test_header_stats(root, tmp_path):
    r, maps = root
    b = rc.review("georgia", r, maps, tmp_path / "out")["basics"]
    assert b["headers read"] == 3 and b["records listed in g*/RECORDS"] == 3
    assert b["duration s min / median / max"] == "5 / 10 / 10"
    assert b["age non-numeric values"] == "NaN: 1"
    assert b["any patient-ID-like comment key"] == "none found"
    assert (tmp_path / "out" / "challenge_georgia_summary.md").exists()


def test_no_maps_all_unmapped(root, tmp_path):
    r, _ = root
    dx = rc.review("georgia", r, None, tmp_path / "out")["dx"]
    assert (dx["name"] == "unmapped").all()
