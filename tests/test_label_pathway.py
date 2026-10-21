"""label_pathway text table and row builder (no real data)."""

from stemi.review import label_pathway as lp


def test_every_text_has_star_and_source():
    for key, t in lp.TEXT.items():
        if "stage" in t:
            assert t["stage"].startswith("★"), key
        if "pathway" in t:
            assert "★" in t["pathway"], key
        if "source" in t:
            assert "verified_facts" in t["source"], key


def test_row_columns_and_override():
    r = lp._row("code15", "Normal ECG", "normal_ecg", lp.TEXT["code15"], 5, 4, "records",
                **lp.TEXT["code15_normal"])
    assert list(r) == lp.COLUMNS
    assert r["labeller"] == "automatic annotation system" and r["n_ecgs"] == 5


def test_ptbxl_labeller_says_subset_not_equal():
    assert "⊂" in lp.TEXT["ptb_xl"]["labeller"] and "1,070" in lp.TEXT["ptb_xl"]["labeller"]
