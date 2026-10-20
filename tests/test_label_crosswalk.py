"""label_crosswalk cell rules on a small invented Sources object (no real data)."""

from types import SimpleNamespace

import pandas as pd

from stemi.review import label_crosswalk as lc


def _src():
    return SimpleNamespace(
        ptbxl_long=pd.DataFrame({"ecg_id": [1, 1, 2, 3], "code": ["IMI", "AMI", "AMI", "NORM"]}),
        ptbxl_codes={"IMI", "AMI", "NORM", "LNGQT"},
        sph_long=pd.DataFrame({"ecg": ["a", "a", "b", "c"], "code": ["145", "145", "160", "145"],
                               "modifier": ["", "363", "332", "362"]}),
        sph_codes={"145", "160", "332", "362", "363", "148"},
        code15=pd.DataFrame({"AF": [True, False, False], "SB": [False, True, False]}),
        dm=pd.DataFrame({"SNOMEDCTCode": ["1", "2", "3"], "Georgia": [5, 7, 0]}),
        g1={"georgia": pd.DataFrame({"record_name": ["r1", "r1", "r2"], "code": ["1", "2", "2"]})},
    )


def test_ptbxl_union_and_listed_zero():
    s = _src()
    assert lc.cell_ptb_xl(s, ["IMI", "AMI"]) == 2            # union, not 3
    assert lc.cell_ptb_xl(s, ["LNGQT"]) == lc.LISTED_ZERO
    assert lc.cell_ptb_xl(s, []) == lc.NOT_PRESENT


def test_sph_pairs():
    s = _src()
    assert lc.cell_sph(s, ["145+363"]) == 1
    assert lc.cell_sph(s, ["145"]) == 2
    assert lc.cell_sph(s, ["148"]) == lc.LISTED_ZERO


def test_code15_union():
    assert lc.cell_code15(_src(), ["AF", "SB"]) == 2


def test_challenge_sum_and_g1_union():
    s = _src()
    pub, g1 = lc.cell_challenge(s, "georgia", ["1", "2"])
    assert pub == 12 and g1 == 2                             # 5+7 summed; g1 r1,r2 union
    assert lc.cell_challenge(s, "georgia", ["3"]) == (lc.LISTED_ZERO, lc.LISTED_ZERO)
    assert lc.cell_challenge(s, "georgia", ["9"]) == (lc.NOT_PRESENT, lc.NOT_PRESENT)


def test_every_mapping_row_has_a_note_entry():
    for label, m in lc.MAPPING.items():
        note = lc._note(label, m)
        assert note.startswith("ptb_xl:") and "incart:" in note
