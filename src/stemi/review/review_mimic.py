"""MIMIC-IV-ECG 1.0 open-module review (step S4). Reads CSVs and .hea text only.

    .venv/bin/python -I src/stemi/review/review_mimic.py data/samples/mimic_iv_ecg

Machine report text is listed for review only. It is never a label source (L2, C2.6).
Years are not reported because MIMIC dates are shifted (C2.7).

Outputs (results/):
    mimic_iv_ecg_report_statements.csv  every distinct report_* statement: ECGs, subjects,
                                        keyword flags (listing only)
    mimic_iv_ecg_field_counts.csv       raw value counts of cart_id, bandwidth, filtering
    mimic_iv_ecg_headers.csv            one row per downloaded header
    mimic_iv_ecg_summary.md
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
    MI_KEYWORDS, RESULTS_DIR, keyword_flags, md_table, provenance, write_summary,
)
from stemi.review.hea_parser import header_row, parse_header

DATASET_ID = "mimic_iv_ecg"
RELEASE = "1.0"
SCRIPT = "src/stemi/review/review_mimic.py"
RAW_FIELDS = ["cart_id", "bandwidth", "filtering"]       # C2.6: raw strings, not numbers
MISSING = "<missing>"


def report_columns(cols) -> list[str]:
    return sorted([c for c in cols if re.fullmatch(r"report_\d+", c)],
                  key=lambda c: int(c.split("_")[1]))


def statement_table(mm: pd.DataFrame) -> pd.DataFrame:
    rep = report_columns(mm.columns)
    long = (mm[["subject_id", "study_id"] + rep]
            .melt(id_vars=["subject_id", "study_id"], value_name="statement")
            .dropna(subset=["statement"]))
    long["statement"] = long["statement"].astype(str).str.strip()
    long = long[long["statement"] != ""].drop_duplicates(["study_id", "statement"])
    g = long.groupby("statement")
    out = pd.DataFrame({"n_ecgs": g["study_id"].nunique(),
                        "n_subjects": g["subject_id"].nunique()})
    flags = pd.DataFrame([keyword_flags(s) for s in out.index], index=out.index)
    out = out.join(flags)
    out["any_mi_st_keyword"] = flags.any(axis=1)
    return out.reset_index().sort_values("n_ecgs", ascending=False)


def field_counts(mm: pd.DataFrame) -> pd.DataFrame:
    parts = []
    for col in RAW_FIELDS:
        if col not in mm.columns:
            parts.append(pd.DataFrame({"field": [col], "value": ["not found"], "n_ecgs": [None]}))
            continue
        vc = mm[col].astype("string").fillna(MISSING).value_counts()
        parts.append(pd.DataFrame({"field": col, "value": vc.index, "n_ecgs": vc.to_numpy()}))
    return pd.concat(parts, ignore_index=True)


def header_table(root: Path) -> pd.DataFrame:
    files = sorted((root / "files").glob("p*/p*/s*/*.hea"))
    return pd.DataFrame([{"file": p.relative_to(root).as_posix(), **header_row(parse_header(p))}
                         for p in files])


def ecgs_with(stmts: pd.DataFrame, mm: pd.DataFrame, flag: str) -> tuple[int, int]:
    """Distinct ECGs/subjects with >=1 statement carrying ``flag``."""
    hit = set(stmts.loc[stmts[flag], "statement"])
    rep = report_columns(mm.columns)
    mask = mm[rep].apply(lambda col: col.astype("string").str.strip().isin(hit)).any(axis=1)
    return int(mm.loc[mask, "study_id"].nunique()), int(mm.loc[mask, "subject_id"].nunique())


def review(root: Path, out_dir: Path = RESULTS_DIR) -> dict:
    paths = {k: root / f for k, f in [("records", "record_list.csv"),
                                      ("mm", "machine_measurements.csv"),
                                      ("dict", "machine_measurements_data_dictionary.csv"),
                                      ("notes", "waveform_note_links.csv")]}
    rec = pd.read_csv(paths["records"])
    mm = (pd.read_csv(paths["mm"], low_memory=False, dtype={c: str for c in RAW_FIELDS})
          if paths["mm"].exists() else None)
    notes = pd.read_csv(paths["notes"]) if paths["notes"].exists() else None
    ddict = pd.read_csv(paths["dict"]) if paths["dict"].exists() else None
    headers = header_table(root)

    out_dir.mkdir(parents=True, exist_ok=True)
    headers.to_csv(out_dir / "mimic_iv_ecg_headers.csv", index=False)

    per_subj = rec.groupby("subject_id").size()
    basics = {
        "rows in record_list.csv": len(rec),
        "distinct study_id (record_list)": rec["study_id"].nunique(),
        "distinct subject_id (record_list)": rec["subject_id"].nunique(),
        "ECGs per subject: min / median / max": f"{per_subj.min()} / {per_subj.median():g} / {per_subj.max()}",
        "record_list columns": ", ".join(rec.columns),
    }
    if notes is not None:
        nn = notes["note_id"].notna() if "note_id" in notes.columns else pd.Series(False, index=notes.index)
        basics["rows in waveform_note_links.csv"] = len(notes)
        basics["distinct study_id with a note_id"] = int(notes.loc[nn, "study_id"].nunique())
        basics["share of record_list ECGs with a note_id"] = (
            f"{rec['study_id'].isin(notes.loc[nn, 'study_id']).mean():.4f}")
    else:
        basics["waveform_note_links.csv"] = "not downloaded"
    stmts = fields = flag_df = None
    if mm is not None:
        stmts = statement_table(mm)
        fields = field_counts(mm)
        basics.update({
            "rows in machine_measurements.csv": len(mm),
            "report_* columns": len(report_columns(mm.columns)),
            "distinct report statements": len(stmts),
            "record_list study_id missing from machine_measurements":
                int((~rec["study_id"].isin(mm["study_id"])).sum()),
        })
        flag_counts = []
        for flag in list(MI_KEYWORDS) + ["any_mi_st_keyword"]:
            n_e, n_s = ecgs_with(stmts, mm, flag)
            flag_counts.append({"keyword_flag": flag,
                                "regex": MI_KEYWORDS.get(flag, "any of the above"),
                                "distinct_statements": int(stmts[flag].sum()), "n_ecgs": n_e,
                                "n_subjects": n_s})
        flag_df = pd.DataFrame(flag_counts)
        stmts.to_csv(out_dir / "mimic_iv_ecg_report_statements.csv", index=False)
        fields.to_csv(out_dir / "mimic_iv_ecg_field_counts.csv", index=False)
        flag_df.to_csv(out_dir / "mimic_iv_ecg_keyword_flag_counts.csv", index=False)
        mi_list = stmts[stmts["kw_infarct"] | stmts["kw_injury"] | stmts["kw_st_elev"]]
        mm_sections = [
            ("Keyword flags over machine report statements (L2: machine text, listing only)",
             md_table(flag_df)),
            ("Statements with infarct / injury / ST-elevation keywords (top 60 by ECGs)",
             md_table(mi_list[["statement", "n_ecgs", "n_subjects", "kw_acute"]], max_rows=60)),
            ("Raw device / filter fields (C2.6: cart_id is not a model; filter strings are not cutoffs)",
             md_table(fields.groupby("field").head(15))),
        ]
    else:
        mm_sections = [("Machine report statements, cart_id, filters",
                        "not downloaded (machine_measurements.csv not in the sample folder)")]
    sections = [
        ("Basic counts", md_table(pd.DataFrame(list(basics.items()), columns=["item", "value"]))),
        *mm_sections,
        ("machine_measurements_data_dictionary.csv (verbatim)",
         md_table(ddict) if ddict is not None else "not downloaded"),
        (f"Headers ({len(headers)} seeded-sample files; not a release-level fact, E2)",
         md_table(headers.drop(columns=["base_time", "base_date"], errors="ignore"))
         if len(headers) else "No headers found under files/."),
        ("Not reported", "Calendar years: dates in MIMIC are shifted (C2.7)."),
    ]
    write_summary(out_dir / "mimic_iv_ecg_summary.md",
                  "MIMIC-IV-ECG open-module review (local observation)", DATASET_ID, RELEASE,
                  SCRIPT, provenance([p for p in paths.values() if p.exists()]), sections)
    return {"statements": stmts, "fields": fields, "headers": headers, "basics": basics,
            "flags": flag_df}


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("root", type=Path, help="data/samples/mimic_iv_ecg")
    ap.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    args = ap.parse_args(argv)
    res = review(args.root, args.out_dir)
    for k, v in res["basics"].items():
        print(f"{k}: {v}")
    print(res["flags"].to_string(index=False))


if __name__ == "__main__":
    main()
