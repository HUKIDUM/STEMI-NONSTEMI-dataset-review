"""Aggregate MI ICD-10 counts in MIMIC-IV-ECG-Ext-ICD 1.0.1, for the USER to run on their own
credentialed copy of records_w_diag_icd10.csv (rule U1).

The team never runs this and never sees the file.
- Read-only. The path comes only from the command line. No network; stdlib + pandas only.
- Prints aggregate counts only. No subject IDs, dates, cell text or codes outside the listed
  groups.
- Every count 1–9 prints as "<10". Additive families (a total plus its exclusive parts) get
  secondary suppression, so a hidden cell cannot be back-calculated.
- If a required column is missing, only the column NAMES are printed.

    python -I src/stemi/review/mimic_ext_icd_count.py --table /path/to/records_w_diag_icd10.csv \\
        [--out counts.csv]

Column names follow https://physionet.org/content/mimic-iv-ecg-ext-icd-labels/1.0.1/
(planner-supplied). ASSUMPTIONS, to be confirmed against that page:
- one row per ECG (if a `study_id` column exists, ECGs are counted as distinct study_id);
- diag cells are list-like strings of ICD-10-CM codes, e.g. "['I214', 'I10']";
- the ED-vs-hospital comparison uses --ed-col (default ed_diag_ed) and --hosp-col
  (default hosp_diag_hosp), only on ECGs where both cells hold at least one code.
Group labels (STEMI / NSTEMI / …) are an ASSUMPTION for clinical-supervisor review; the
diagnoses are discharge billing codes and do not show whether the MI was acute at ECG time.
"""

from __future__ import annotations

if __package__ in (None, ""):          # run as a file under ``python -I``
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import argparse
import ast
import hashlib
import re
import sys
from pathlib import Path

import pandas as pd

from stemi.review.mimic_icd_count import SUPPRESSED

DIAG_COLUMNS = ["ed_diag_ed", "ed_diag_hosp", "hosp_diag_hosp", "all_diag_hosp", "all_diag_all"]
FLAG_COLUMNS = ["ecg_taken_in_ed", "ecg_taken_in_hosp", "ecg_taken_in_ed_or_hosp"]
REQUIRED = ["subject_id", *DIAG_COLUMNS, *FLAG_COLUMNS]
GROUPS = [
    ("STEMI (I21.0-I21.3; ASSUMPTION)", r"I21[0-3]\w*"),
    ("NSTEMI (I21.4; ASSUMPTION)", r"I214\w*"),
    ("unspecified/other MI (I21.9, I21.A*)", r"I21(9|A)\w*"),
    ("subsequent MI (I22*)", r"I22\w*"),
    ("old MI (I25.2)", r"I252\w*"),
    ("any I21/I22", r"I2[12]\w*"),
]
ANY = "any I21/I22"
CHUNK_ROWS = 200_000
CAVEATS = [
    "Diagnoses are hospital/ED discharge billing codes; they do not show whether the MI was "
    "present or acute at the time of the ECG.",
    "The STEMI/NSTEMI group labels are an ASSUMPTION for clinical-supervisor review.",
    "ASSUMPTION: one row per ECG unless a study_id column exists.",
    "Counts 1-9 print as <10; some larger cells are hidden too (secondary suppression).",
]
_CODE = re.compile(r"[A-Z][0-9][0-9A-Z]{1,6}")


def parse_codes(v) -> tuple[list[str], bool]:
    """(dot-less upper-case codes, parse_ok). Empty / NaN / '[]' -> ([], True)."""
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return [], True
    t = str(v).strip()
    if t in ("", "[]", "nan", "None"):
        return [], True
    items = None
    if t.startswith("["):
        try:
            lit = ast.literal_eval(t)
            if isinstance(lit, (list, tuple)):
                items = [str(x) for x in lit]
        except (ValueError, SyntaxError):
            items = None
    if items is None:
        items = re.split(r"[,;|\s\[\]'\"]+", t)
    codes = [re.sub(r"[^A-Z0-9]", "", x.upper()) for x in items if x.strip(" '\"")]
    ok = all(_CODE.fullmatch(c) for c in codes) and bool(codes)
    return ([c for c in codes if _CODE.fullmatch(c)], ok)


def _flag(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.lower().isin({"true", "1", "1.0", "t", "yes"})


def check_columns(path: Path) -> list[str]:
    cols = list(pd.read_csv(path, nrows=0).columns)
    missing = [c for c in REQUIRED if c not in cols]
    if missing:
        print("Required columns missing. Columns in the file (names only):")
        for c in cols:
            print(f"  {c}")
        print("Missing: " + ", ".join(missing))
        raise SystemExit(2)
    return cols


def file_identity(path: Path) -> tuple[int, str]:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return path.stat().st_size, h.hexdigest()


def flags_frame(path: Path, cols: list[str]) -> tuple[pd.DataFrame, dict[str, int]]:
    """One compact row per input row: subject, optional study, settings, group hits per column."""
    use = REQUIRED + (["study_id"] if "study_id" in cols else [])
    parts, bad = [], {c: 0 for c in DIAG_COLUMNS}
    for chunk in pd.read_csv(path, usecols=use, dtype=str, chunksize=CHUNK_ROWS,
                             keep_default_na=False, na_values=[""]):
        out = pd.DataFrame({"subject": chunk["subject_id"].to_numpy()})
        out["ecg"] = chunk["study_id"].to_numpy() if "study_id" in chunk else None
        for f in FLAG_COLUMNS:
            out[f] = _flag(chunk[f]).to_numpy()
        for c in DIAG_COLUMNS:
            parsed = chunk[c].map(parse_codes)
            bad[c] += int((~parsed.map(lambda p: p[1])).sum())
            codes = parsed.map(lambda p: p[0])
            out[f"{c}__nonempty"] = codes.map(bool).to_numpy()
            for name, pat in GROUPS:
                rx = re.compile(pat)
                out[f"{c}__{name}"] = codes.map(lambda cs: any(rx.fullmatch(x) for x in cs)).to_numpy()
        parts.append(out)
    df = pd.concat(parts, ignore_index=True)
    if df["ecg"].isna().all():
        df["ecg"] = range(len(df))                   # one row per ECG (ASSUMPTION)
    return df, bad


def _n(df: pd.DataFrame, mask: pd.Series) -> tuple[int, int]:
    return int(df.loc[mask, "ecg"].nunique()), int(df.loc[mask, "subject"].nunique())


def _s(n: int) -> str:
    return SUPPRESSED if 0 < n < 10 else str(int(n))


def suppress_parts(total: int, parts: list[int]) -> tuple[str, list[str]]:
    """total = sum of exclusive parts. 1-9 -> "<10"; 0 stays "0" (it reveals nothing).
    If exactly one part is hidden while the total is shown, the smallest other non-zero
    part is hidden too, so the hidden one cannot be back-calculated."""
    hidden = [0 < p < 10 for p in parts]
    total_hidden = 0 < total < 10
    if not total_hidden and sum(hidden) == 1:
        cand = [i for i, p in enumerate(parts) if p > 0 and not hidden[i]]
        if cand:
            hidden[min(cand, key=lambda i: parts[i])] = True
    return (SUPPRESSED if total_hidden else str(int(total)),
            [SUPPRESSED if h else str(int(p)) for p, h in zip(parts, hidden)])


def by_column(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name, _ in GROUPS:
        for c in DIAG_COLUMNS:
            e, p = _n(df, df[f"{c}__{name}"])
            rows.append({"group": name, "diagnosis_column": c, "ecgs": _s(e), "patients": _s(p)})
    return pd.DataFrame(rows)


def by_setting(df: pd.DataFrame, col: str = "all_diag_all") -> pd.DataFrame:
    """Exclusive setting parts per group (ED only / hosp only / both / neither = outpatient)."""
    ed, ho = df["ecg_taken_in_ed"], df["ecg_taken_in_hosp"]
    parts = [("ED only", ed & ~ho), ("hospital only", ~ed & ho), ("ED and hospital", ed & ho),
             ("neither (outpatient)", ~ed & ~ho)]
    rows = []
    for name, _ in GROUPS:
        g = df[f"{col}__{name}"]
        for unit in ("ecgs", "patients"):
            idx = 0 if unit == "ecgs" else 1
            total = _n(df, g)[idx]
            kids = [_n(df, g & m)[idx] for _, m in parts]
            t, ks = suppress_parts(total, kids)
            rows.append({"group": name, "diagnosis_column": col, "unit": unit, "total": t,
                         **{p[0]: v for p, v in zip(parts, ks)}})
    return pd.DataFrame(rows)


def disagreement(df: pd.DataFrame, ed_col: str = "ed_diag_ed", hosp_col: str = "hosp_diag_hosp") -> pd.DataFrame:
    """ECGs where both columns hold codes: group in both / ED only / hospital only / neither,
    plus the specific cross cases (no I21/I22 in one vs STEMI/NSTEMI in the other, STEMI vs NSTEMI)."""
    both = df[f"{ed_col}__nonempty"] & df[f"{hosp_col}__nonempty"]
    rows = []
    for name, _ in GROUPS:
        a, b = df[f"{ed_col}__{name}"] & both, df[f"{hosp_col}__{name}"] & both
        total = int(df.loc[both, "ecg"].nunique())
        kids = [_n(df, a & b)[0], _n(df, a & ~b)[0], _n(df, ~a & b)[0], _n(df, both & ~a & ~b)[0]]
        t, ks = suppress_parts(total, kids)
        rows.append({"comparison": f"{name}: {ed_col} vs {hosp_col}",
                     "ecgs_with_both_columns_coded": t, "in_both": ks[0], "ed_only": ks[1],
                     "hosp_only": ks[2], "in_neither": ks[3]})
    st, ns = GROUPS[0][0], GROUPS[1][0]
    cases = [
        (f"{ed_col} no I21/I22, {hosp_col} NSTEMI", ~df[f"{ed_col}__{ANY}"] & df[f"{hosp_col}__{ns}"]),
        (f"{ed_col} no I21/I22, {hosp_col} STEMI", ~df[f"{ed_col}__{ANY}"] & df[f"{hosp_col}__{st}"]),
        (f"{hosp_col} no I21/I22, {ed_col} NSTEMI", ~df[f"{hosp_col}__{ANY}"] & df[f"{ed_col}__{ns}"]),
        (f"{hosp_col} no I21/I22, {ed_col} STEMI", ~df[f"{hosp_col}__{ANY}"] & df[f"{ed_col}__{st}"]),
        (f"{ed_col} STEMI and {hosp_col} NSTEMI", df[f"{ed_col}__{st}"] & df[f"{hosp_col}__{ns}"]),
        (f"{ed_col} NSTEMI and {hosp_col} STEMI", df[f"{ed_col}__{ns}"] & df[f"{hosp_col}__{st}"]),
    ]
    for label, m in cases:
        rows.append({"comparison": label, "ecgs_with_both_columns_coded": "",
                     "in_both": _s(_n(df, m & both)[0])})
    return pd.DataFrame(rows)


def run(path: Path, ed_col: str = "ed_diag_ed", hosp_col: str = "hosp_diag_hosp") -> dict:
    cols = check_columns(path)
    for c in (ed_col, hosp_col):
        if c not in DIAG_COLUMNS:
            raise SystemExit(f"--ed-col/--hosp-col must be one of {DIAG_COLUMNS}")
    size, sha = file_identity(path)
    df, bad = flags_frame(path, cols)
    ident = pd.DataFrame({"item": ["file name", "file size (bytes)", "file sha256", "rows",
                                   "distinct ECGs (study_id or rows)", "distinct patients",
                                   *[f"unparseable cells in {c}" for c in DIAG_COLUMNS]],
                          "value": [path.name, size, sha, len(df), df["ecg"].nunique(),
                                    df["subject"].nunique(), *[bad[c] for c in DIAG_COLUMNS]]})
    return {"identity": ident, "by_column": by_column(df), "by_setting": by_setting(df),
            "disagreement": disagreement(df, ed_col, hosp_col)}


def main(argv: list[str] | None = None) -> dict:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--table", type=Path, required=True, help="records_w_diag_icd10.csv")
    ap.add_argument("--ed-col", default="ed_diag_ed", help="ED column for the disagreement table")
    ap.add_argument("--hosp-col", default="hosp_diag_hosp", help="hospital column for the disagreement table")
    ap.add_argument("--out", type=Path, default=None, help="optional aggregate CSV (new file only)")
    args = ap.parse_args(argv)
    if args.out is not None and args.out.exists():
        raise SystemExit(f"{args.out} exists; choose a new file name (nothing is overwritten)")
    res = run(args.table, args.ed_col, args.hosp_col)
    for c in CAVEATS:
        print(f"- {c}")
    for key in ("identity", "by_column", "by_setting", "disagreement"):
        print(f"\n== {key}")
        print(res[key].to_string(index=False))
    if args.out is not None:
        with open(args.out, "x", newline="") as f:
            for c in CAVEATS:
                f.write(f"# {c}\n")
            for key in ("identity", "by_column", "by_setting", "disagreement"):
                f.write(f"# == {key}\n")
                res[key].to_csv(f, index=False)
    return res


if __name__ == "__main__":
    main(sys.argv[1:])
