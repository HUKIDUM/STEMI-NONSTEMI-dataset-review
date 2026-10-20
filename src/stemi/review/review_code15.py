"""CODE-15% (Zenodo 4916206) exams.csv review (step S8). CSV only, no HDF5.

    .venv/bin/python -I src/stemi/review/review_code15.py data/samples/code15

Outputs (results/):
    code15_label_counts.csv  every boolean (True/False) column: True count, exams, patients
    code15_summary.md        exams, patients, exams per patient, trace_file spread, and
                             whether any column name or label mentions MI / infarct
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

from stemi.review.common import RESULTS_DIR, md_table, provenance, write_summary

DATASET_ID = "code15"
RELEASE = "Zenodo 4916206"
SCRIPT = "src/stemi/review/review_code15.py"
MI_NAME = r"infarct|\bmi\b|stemi|ischem|isquem|injury|st[_ ]?elev"


def boolean_columns(df: pd.DataFrame) -> list[str]:
    out = []
    for c in df.columns:
        vals = set(df[c].dropna().astype(str).str.strip().str.lower().unique())
        if vals and vals <= {"true", "false", "0", "1"} and c != "exam_id":
            out.append(c)
    return out


def as_bool(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.lower().isin({"true", "1"})


def review(root: Path, out_dir: Path = RESULTS_DIR) -> dict:
    path = root / "exams.csv"
    df = pd.read_csv(path)
    bools = boolean_columns(df)
    pid = "patient_id" if "patient_id" in df.columns else None
    rows = []
    for c in bools:
        m = as_bool(df[c])
        rows.append({"column": c, "n_true": int(m.sum()), "n_missing": int(df[c].isna().sum()),
                     "n_patients_true": int(df.loc[m, pid].nunique()) if pid else None,
                     "name_matches_mi_regex": bool(re.search(MI_NAME, c, re.I))})
    labels = pd.DataFrame(rows)
    out_dir.mkdir(parents=True, exist_ok=True)
    labels.to_csv(out_dir / "code15_label_counts.csv", index=False)

    basics = {
        "columns": ", ".join(df.columns),
        "rows": len(df),
        "distinct exam_id": df["exam_id"].nunique() if "exam_id" in df.columns else "not found",
        "distinct patient_id": df[pid].nunique() if pid else "not found",
        "boolean columns": ", ".join(bools) or "none",
        "column names matching MI regex": ", ".join(c for c in df.columns
                                                    if re.search(MI_NAME, c, re.I)) or "none",
    }
    if pid:
        per = df.groupby(pid).size()
        basics["exams per patient: min / median / max"] = f"{per.min()} / {per.median():g} / {per.max()}"
        basics["patients with >1 exam"] = int((per > 1).sum())
    if "trace_file" in df.columns:
        tf = df["trace_file"].value_counts()
        basics["distinct trace_file"] = len(tf)
        basics["exams per trace_file min / max"] = f"{tf.min()} / {tf.max()}"
    if bools:
        lab_cols = [c for c in bools if c not in ("is_male", "death")]
        none = ~df[lab_cols].apply(as_bool).any(axis=1)
        basics[f"exams with none of {lab_cols} True"] = int(none.sum())
    sections = [
        ("Basic counts", md_table(pd.DataFrame(list(basics.items()), columns=["item", "value"]))),
        ("Boolean columns (labels and other flags)", md_table(labels)),
    ]
    write_summary(out_dir / "code15_summary.md", "CODE-15% exams.csv review (local observation)",
                  DATASET_ID, RELEASE, SCRIPT, provenance([path]), sections)
    return {"labels": labels, "basics": basics}


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("root", type=Path, help="data/samples/code15")
    ap.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    args = ap.parse_args(argv)
    res = review(args.root, args.out_dir)
    for k, v in res["basics"].items():
        print(f"{k}: {v}")
    print(res["labels"].to_string(index=False))


if __name__ == "__main__":
    main()
