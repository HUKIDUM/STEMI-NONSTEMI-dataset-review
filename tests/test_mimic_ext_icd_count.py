"""mimic_ext_icd_count on invented rows shaped like the documented columns (no real data)."""

import pandas as pd
import pytest

from stemi.review import mimic_ext_icd_count as mx


def _write(tmp_path, rows):
    p = tmp_path / "records_w_diag_icd10.csv"
    pd.DataFrame(rows).to_csv(p, index=False)
    return p


def _row(sid, ed="[]", hosp="[]", alld=None, in_ed=False, in_hosp=False):
    _row.n = getattr(_row, "n", 0) + 1
    return {"subject_id": sid, "study_id": 90000000 + _row.n, "ed_diag_ed": ed, "ed_diag_hosp": "[]", "hosp_diag_hosp": hosp,
            "all_diag_hosp": hosp, "all_diag_all": alld if alld is not None else hosp,
            "ecg_taken_in_ed": in_ed, "ecg_taken_in_hosp": in_hosp,
            "ecg_taken_in_ed_or_hosp": in_ed or in_hosp}


def _fixture(tmp_path):
    rows = [_row(1000 + i, ed="['I10']", hosp="['I214', 'I10']", in_ed=True, in_hosp=True)
            for i in range(12)]                                    # ED no MI, hosp NSTEMI
    rows += [_row(2000 + i, hosp="['I2101']", in_hosp=True) for i in range(11)]   # hosp STEMI
    rows += [_row(3000, ed="['I214']", hosp="['I2109']", in_ed=True, in_hosp=True)]
    rows += [_row(4000, alld="['I252']")]                          # outpatient old MI
    rows += [_row(5000, hosp="not a list {")]                      # unparseable
    return _write(tmp_path, rows)


def _cell(df, **kv):
    m = pd.Series(True, index=df.index)
    for k, v in kv.items():
        m &= df[k] == v
    return df[m].iloc[0]


def test_parse_codes():
    assert mx.parse_codes("['I21.4', 'i10']") == (["I214", "I10"], True)
    assert mx.parse_codes("[]") == ([], True)
    assert mx.parse_codes("not a list {")[1] is False


def test_counts_and_suppression(tmp_path):
    res = mx.run(_fixture(tmp_path))
    bc = res["by_column"]
    assert _cell(bc, group=mx.GROUPS[1][0], diagnosis_column="hosp_diag_hosp")["ecgs"] == "12"
    assert _cell(bc, group=mx.GROUPS[0][0], diagnosis_column="hosp_diag_hosp")["ecgs"] == "12"
    assert _cell(bc, group="old MI (I25.2)", diagnosis_column="all_diag_all")["ecgs"] == "<10"
    assert _cell(bc, group=mx.GROUPS[1][0], diagnosis_column="ed_diag_ed")["ecgs"] == "<10"
    ident = res["identity"].set_index("item")["value"]
    assert ident["rows"] == 26 and ident["unparseable cells in hosp_diag_hosp"] == "<10"
    assert ident["disagreement pair used"] == "ed_diag_ed vs ed_diag_hosp"
    assert len(ident["file sha256"]) == 64


def test_setting_split_secondary_suppression(tmp_path):
    bs = mx.run(_fixture(tmp_path))["by_setting"]
    r = _cell(bs, group=mx.GROUPS[0][0], unit="ecgs")            # STEMI: 11 hosp-only + 1 both
    assert r["total"] == "12" and r["ED and hospital"] == "<10"
    assert r["hospital only"] == "<10"                           # hidden too: 12 - 1 would reveal it


def test_disagreement(tmp_path):
    d = mx.run(_fixture(tmp_path), hosp_col="hosp_diag_hosp")["disagreement"].set_index("comparison")
    assert d.loc["ed_diag_ed no I21/I22, hosp_diag_hosp NSTEMI", "in_both"] == "12"
    assert d.loc["ed_diag_ed NSTEMI and hosp_diag_hosp STEMI", "in_both"] == "<10"


def test_missing_column_prints_names_only(tmp_path, capsys):
    p = _write(tmp_path, [{"subject_id": 1, "secret_col": "I214 patient 42"}])
    with pytest.raises(SystemExit):
        mx.run(p)
    out = capsys.readouterr().out
    assert "secret_col" in out and "patient 42" not in out and "I214" not in out


def test_output_has_no_ids_or_cell_text(tmp_path, capsys):
    mx.main(["--table", str(_fixture(tmp_path))])
    out = capsys.readouterr().out
    for s in ("1000", "2005", "3000", "4000", "5000", "9000000", "not a list", "I10", "I2109"):
        assert s not in out
    assert "billing codes" in out and "ASSUMPTION" in out


def test_out_never_overwrites(tmp_path):
    p, out = _fixture(tmp_path), tmp_path / "agg.csv"
    mx.main(["--table", str(p), "--out", str(out)])
    assert out.read_text().startswith("# Diagnoses")
    with pytest.raises(SystemExit):
        mx.main(["--table", str(p), "--out", str(out)])


def test_suppress_parts():
    assert mx.suppress_parts(12, [0, 11, 1, 0]) == ("12", ["0", "<10", "<10", "0"])
    assert mx.suppress_parts(30, [15, 15, 0]) == ("30", ["15", "15", "0"])
    assert mx.suppress_parts(5, [5, 0]) == ("<10", ["<10", "0"])


def test_flag_parsing_and_unparseable():
    v, bad = mx._flag(pd.Series(["True", "false", "1", "0", "T", "f", "yes", "maybe"]))
    assert v.tolist() == [True, False, True, False, True, False, False, False] and bad == 2


def test_default_pair_is_ed_journey(tmp_path):
    rows = [_row(7000 + i, ed="['I10']", hosp="[]", in_ed=True) for i in range(12)]
    for r in rows:
        r["ed_diag_hosp"] = "['I214']"                              # admission after the ED stay
    d = mx.run(_write(tmp_path, rows))["disagreement"].set_index("comparison")
    assert d.loc["ed_diag_ed no I21/I22, ed_diag_hosp NSTEMI", "in_both"] == "12"


def test_study_id_fallback_is_announced(tmp_path):
    rows = [_row(8000 + i) for i in range(3)]
    for r in rows:
        r.pop("study_id")
    ident = mx.run(_write(tmp_path, rows))["identity"].set_index("item")["value"]
    assert any("MISSING" in k for k in ident.index)


def test_elapsed_and_pair_printed(tmp_path, capsys):
    mx.main(["--table", str(_fixture(tmp_path))])
    out = capsys.readouterr().out
    assert "Elapsed:" in out and "Disagreement pair used: ed_diag_ed vs ed_diag_hosp" in out
    assert "Cell format assumed" in out and "Flag format assumed" in out
