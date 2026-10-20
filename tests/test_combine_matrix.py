from stemi.review import combine_matrix as cm


def test_incart_rule_first():
    v, reasons, _ = cm.verdict("ptb_xl", "incart")
    assert v == "No (supervised MI)" and "Holter" in reasons[0]


def test_reasons_listed_in_order():
    v, reasons, _ = cm.verdict("ptb_diagnostic", "code15")
    assert v == "After checks"
    assert [r[0] for r in reasons] == ["a", "b", "c", "d", "f"]
    assert "code15 has no MI labels" in reasons[-1]


def test_no_patient_id_and_overlap():
    v, reasons, rows = cm.verdict("chapman_shaoxing", "ningbo")
    assert [r[0] for r in reasons] == ["e", "g"]
    assert any("count match" in r for r in rows)


def test_yes_only_when_nothing_applies():
    a = cm.Attr(500, True, "10 s", False, "", 1000.0, True, "X", "r")
    assert cm.verdict("p", "q", {"p": a, "q": a})[0] == "Yes (technical)"


def test_build_55_pairs(tmp_path):
    df = cm.build(tmp_path)
    assert len(df) == 55 and df[["ds_a", "ds_b"]].apply(frozenset, axis=1).nunique() == 55
    assert (tmp_path / "combine_matrix_summary.md").exists()
