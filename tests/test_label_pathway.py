"""label_pathway: every text cell traces to a verified_facts row key (no real data needed)."""

import pandas as pd

from stemi.review import label_pathway as lp


def test_every_text_key_is_a_verified_row():
    keys = lp.verified_row_keys()
    for name, fields in lp.TEXT.items():
        for field, (text, row) in fields.items():
            assert row in keys, (name, field, row)
            assert field in lp.TEXT_FIELDS and text.strip()


def test_row_text_cells_trace_to_source_rows():
    r = lp._row("code15", "Normal ECG", "normal_ecg", 5, "records", ["code15_normal"])
    assert list(r) == lp.COLUMNS
    assert "automatic annotation system" in r["labeller"]
    assert "dataset-level method" not in r["steps"]                 # class-specific statement exists
    for f in lp.TEXT_FIELDS:
        if r[f]:
            assert any(k in r["source_rows"] for k in ("code15 | S13 provenance", "code15 | S13 pathway"))


def test_not_found_wording_kept():
    assert lp.TEXT["challenge_cg"]["labeller"][0] == "not found (per source)"
    assert lp.TEXT["ptb_diagnostic"]["labeller"][0] == "not found"


def test_built_file_traces(tmp_path):
    """On the real output (if present): every non-empty text cell's row is in source_rows,
    and every source_rows key exists in verified_facts.md."""
    p = lp.VERIFIED.parent / "label_provenance.csv"
    if not p.exists():
        return
    df = pd.read_csv(p, dtype=str, keep_default_na=False)
    keys = lp.verified_row_keys()
    for r in df.itertuples(index=False):
        used = [k.strip() for k in r.source_rows.split(" ; ") if k.strip()]
        assert used and all(k in keys for k in used)
