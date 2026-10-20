"""SPH (Shandong Provincial Hospital, figshare 5779802 v1) review (step S6). CSV only.

    .venv/bin/python -I src/stemi/review/review_sph.py data/samples/sph

Statements are AHA codes. A statement may carry modifiers joined with '+'
(e.g. "160+330"); several statements per ECG are separated by ';'. The split
characters are checked against the file: a summary line reports how many
fields contain each separator.

Outputs (results/):
    sph_code_counts.csv           primary AHA code: ECGs, patients, description
    sph_code_modifier_counts.csv  primary code + modifier pairs: ECGs, patients
    sph_mi_timing.csv             distinct ECGs with an MI code by Acute/Recent/Old modifier
    sph_summary.md
"""

from __future__ import annotations

if __package__ in (None, ""):          # run as a file under ``python -I``
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import argparse
import re
from pathlib import Path

import pandas as pd

from stemi.review.common import (
    RESULTS_DIR, keyword_flags, md_table, provenance, read_text_csv, write_summary,
)

DATASET_ID = "sph"
RELEASE = "figshare collection 5779802 v1"
SCRIPT = "src/stemi/review/review_sph.py"

COLUMN_PATTERNS = {"ecg": r"^ecg_?id$", "code": r"^aha_?code$", "patient": r"^patient_?id$",
                   "age": r"^age$", "sex": r"^sex$", "n": r"^n$", "date": r"^date$"}


def find_col(cols, pattern: str) -> str | None:
    hits = [c for c in cols if re.fullmatch(pattern, str(c).strip(), flags=re.IGNORECASE)]
    return hits[0] if hits else None


def explode_statements(meta: pd.DataFrame, ecg: str, code: str, patient: str | None) -> pd.DataFrame:
    """One row per (ECG, primary code, modifier or '')."""
    rows = []
    pats = meta[patient] if patient else pd.Series([None] * len(meta))
    for e, p, s in zip(meta[ecg], pats, meta[code].astype(str)):
        for stmt in [x.strip() for x in s.split(";") if x.strip()]:
            primary, *mods = [x.strip() for x in stmt.split("+")]
            rows.append((e, p, primary, ""))
            rows += [(e, p, primary, m) for m in mods]
    return pd.DataFrame(rows, columns=["ecg", "patient", "code", "modifier"])


def counts(long: pd.DataFrame, by: list[str]) -> pd.DataFrame:
    g = long.groupby(by)
    return pd.DataFrame({"n_ecgs": g["ecg"].nunique(),
                         "n_patients": g["patient"].nunique()}).reset_index()


def mi_timing_table(long: pd.DataFrame, primary: pd.DataFrame, names: pd.DataFrame) -> pd.DataFrame:
    """Distinct ECGs/patients with an MI-named code (category M in code.csv if present,
    else 'MI' in the description), by the timing modifier attached to that statement."""
    if "Category" in names.columns:
        mi = set(names.loc[names["Category"].str.strip() == "M", "code"])
    else:
        mi = set(primary.loc[primary["kw_infarct"], "code"])
    timing = {m: d for m, d in zip(names["code"], names["description"])
              if str(d).strip().lower() in ("acute", "recent", "old")}
    mi_long = long[long["code"].isin(mi)]
    stmt_mods = mi_long.groupby(["ecg", "code"])["modifier"].apply(set)
    rows = []
    def add(label, ecgs):
        sub = long[long["ecg"].isin(ecgs)]
        rows.append({"selection": label, "n_ecgs": len(ecgs),
                     "n_patients": sub["patient"].nunique()})
    add(f"any MI code {sorted(mi)}", set(mi_long["ecg"]))
    for m, d in sorted(timing.items()):
        add(f"MI code with modifier {m} ({d})",
            {e for (e, _), mods in stmt_mods.items() if m in mods})
    add("MI code with none of the timing modifiers",
        {e for (e, _), mods in stmt_mods.items() if not (mods & set(timing))})
    acute = {e for (e, _), mods in stmt_mods.items() if any(timing.get(x) == "Acute" for x in mods)}
    st_elev = set(long[(long["code"] == "145") & (long["modifier"] == "363")]["ecg"])
    add("MI code + Acute AND 145+363 (ST deviation + Elevation) on the same ECG", acute & st_elev)
    return pd.DataFrame(rows)


def load_code_names(path: Path) -> pd.DataFrame:
    """code.csv -> (code, description, category if present) with code as string."""
    c = read_text_csv(path, dtype=str)
    code_col = find_col(c.columns, r"^code$") or c.columns[0]
    desc_col = find_col(c.columns, r"^(description|statement|name)$") or c.columns[1]
    out = c.rename(columns={code_col: "code", desc_col: "description"})
    out["code"] = out["code"].str.strip()
    return out


def review(root: Path, out_dir: Path = RESULTS_DIR) -> dict:
    meta_p, code_p = root / "metadata.csv", root / "code.csv"
    meta = read_text_csv(meta_p, dtype=str)
    cols = {k: find_col(meta.columns, p) for k, p in COLUMN_PATTERNS.items()}
    if not cols["ecg"] or not cols["code"]:
        raise ValueError(f"ECG id / AHA code column not found in {list(meta.columns)}")
    names = load_code_names(code_p)
    long = explode_statements(meta, cols["ecg"], cols["code"], cols["patient"])

    primary = counts(long.drop_duplicates(["ecg", "code"]), ["code"])
    primary = primary.merge(names, on="code", how="left")
    primary = primary.join(pd.DataFrame([keyword_flags(d) for d in primary["description"]]))
    primary["in_code_csv"] = primary["code"].isin(names["code"])
    pairs = counts(long[long["modifier"] != ""], ["code", "modifier"])
    pairs = (pairs.merge(names[["code", "description"]], on="code", how="left")
             .merge(names[["code", "description"]].rename(columns={"code": "modifier",
                                                                   "description": "modifier_description"}),
                    on="modifier", how="left"))
    timing = mi_timing_table(long, primary, names)
    primary = primary.sort_values("n_ecgs", ascending=False)
    pairs = pairs.sort_values("n_ecgs", ascending=False)

    out_dir.mkdir(parents=True, exist_ok=True)
    primary.to_csv(out_dir / "sph_code_counts.csv", index=False)
    pairs.to_csv(out_dir / "sph_code_modifier_counts.csv", index=False)
    timing.to_csv(out_dir / "sph_mi_timing.csv", index=False)

    raw = meta[cols["code"]].astype(str)
    basics = {
        "metadata.csv columns": ", ".join(meta.columns),
        "column used": ", ".join(f"{k}={v or 'not found'}" for k, v in cols.items()),
        "rows (ECGs)": len(meta),
        "distinct ECG ids": meta[cols["ecg"]].nunique(),
        "distinct patients": meta[cols["patient"]].nunique() if cols["patient"] else "not found",
        "code fields containing ';' / '+'": f"{raw.str.contains(';').sum()} / {raw.str.contains(re.escape('+')).sum()}",
        "distinct primary codes": long["code"].nunique(),
        "primary codes not in code.csv": ", ".join(sorted(set(long["code"]) - set(names["code"]))) or "none",
        "distinct modifiers used": ", ".join(sorted(set(long["modifier"]) - {""})) or "none",
    }
    if cols["patient"]:
        per = meta.groupby(cols["patient"]).size()
        basics["ECGs per patient: min / median / max"] = f"{per.min()} / {per.median():g} / {per.max()}"
    if cols["n"]:
        n = pd.to_numeric(meta[cols["n"]], errors="coerce")
        basics["N (samples) min / median / max"] = f"{n.min():g} / {n.median():g} / {n.max():g}"
        basics["N / 500 s (500 Hz per [MCR p.3]) min / median / max"] = f"{n.min()/500:g} / {n.median()/500:g} / {n.max()/500:g}"
        basics["N value counts (top 5)"] = "; ".join(f"{k}: {v}" for k, v in n.value_counts().head(5).items())
    for k in ("age", "sex"):
        if cols[k]:
            v = meta[cols[k]]
            basics[f"{k}"] = (f"{pd.to_numeric(v, errors='coerce').min():g}–{pd.to_numeric(v, errors='coerce').max():g}"
                              if k == "age" else "; ".join(f"{a}: {b}" for a, b in v.value_counts().items()))
    if cols["date"]:
        d = pd.to_datetime(meta[cols["date"]], errors="coerce")
        basics["date min / max (as stored)"] = f"{d.min()} / {d.max()}"

    st_dev = primary["description"].fillna("").str.contains(r"ST deviation", case=False)
    mi_mask = primary["kw_infarct"] | primary["kw_injury"] | primary["kw_st_elev"] | st_dev
    mi_codes = set(primary.loc[mi_mask, "code"])
    mi_ecgs = long[long["code"].isin(mi_codes)]
    sections = [
        ("Basic counts", md_table(pd.DataFrame(list(basics.items()), columns=["item", "value"]))),
        ("Codes whose code.csv description mentions infarct / injury / ST elevation / "
         "ST deviation (listing only; L2)",
         f"ECGs with any: {mi_ecgs['ecg'].nunique()}; patients: {mi_ecgs['patient'].nunique()}.\n\n"
         + md_table(primary.loc[mi_mask, ["code", "description", "n_ecgs", "n_patients"]])),
        ("MI codes by timing modifier: distinct ECGs (listing only; not acute labels, L2/L3)",
         md_table(timing)),
        ("Modifiers attached to those codes",
         md_table(pairs[pairs["code"].isin(mi_codes)][["code", "description", "modifier",
                                                         "modifier_description", "n_ecgs",
                                                         "n_patients"]])),
        ("All primary codes (top 40 by ECGs; full list in sph_code_counts.csv)",
         md_table(primary[["code", "description", "n_ecgs", "n_patients"]], max_rows=40)),
    ]
    write_summary(out_dir / "sph_summary.md", "SPH metadata review (local observation)",
                  DATASET_ID, RELEASE, SCRIPT,
                  provenance([meta_p, code_p] + ([root / "rule.pdf"] if (root / "rule.pdf").exists() else [])),
                  sections)
    return {"primary": primary, "pairs": pairs, "timing": timing, "basics": basics, "mi_codes": sorted(mi_codes)}


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("root", type=Path, help="data/samples/sph")
    ap.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    args = ap.parse_args(argv)
    res = review(args.root, args.out_dir)
    for k, v in res["basics"].items():
        print(f"{k}: {v}")
    print("MI/injury/ST-elevation codes:", res["mi_codes"])


if __name__ == "__main__":
    main()
