"""PTB Diagnostic ECG Database 1.0.0 review (step S5). Reads .hea text and list files only.

    .venv/bin/python -I src/stemi/review/review_ptbdb.py data/samples/ptb_diagnostic

Outputs (results/):
    ptb_diagnostic_records.csv        one row per header: patient, fs, channels, duration,
                                      every comment field (raw text)
    ptb_diagnostic_comment_counts.csv value counts of every comment key (records, patients)
    ptb_diagnostic_mi_timing.csv      MI records: acute-infarction date vs ECG date (days),
                                      only where both dates parse; listing for review only
    ptb_diagnostic_summary.md
Comment keys are matched as they appear in the files; a missing key is "not found".
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
from stemi.review.hea_parser import header_row, parse_header
from stemi.inventory import standard12_channel_map

DATASET_ID = "ptb_diagnostic"
RELEASE = "1.0.0 native"
SCRIPT = "src/stemi/review/review_ptbdb.py"
MISSING = "<missing>"

# Comment-key patterns (case-insensitive) used to pick columns; the raw key is reported.
KEY_PATTERNS = {
    "reason": r"^reason for admission$",
    "acute_loc": r"^acute infarction \(localization\)$",
    "former_loc": r"^former infarction \(localization\)$",
    "infarct_date": r"^infarction date( \(acute\))?$",
    "ecg_date": r"^ecg date$",
}


def find_key(keys, pattern: str) -> str | None:
    hits = [k for k in keys if re.search(pattern, k.strip(), flags=re.IGNORECASE)]
    return hits[0] if hits else None


def parse_date(s) -> pd.Timestamp | None:
    """Dates as written in the headers (e.g. 29-Sep-90, 01/10/1990); None if unparsable."""
    if s is None or pd.isna(s):
        return None
    t = str(s).strip()
    for fmt in ("%d-%b-%y", "%d-%b-%Y", "%d/%m/%Y", "%d/%m/%y", "%d.%m.%Y", "%d.%m.%y"):
        try:
            return pd.to_datetime(t, format=fmt)
        except (ValueError, TypeError):
            continue
    return None


def record_table(root: Path) -> pd.DataFrame:
    names = [ln.strip() for ln in (root / "RECORDS").read_text().splitlines() if ln.strip()]
    rows = []
    for name in names:
        p = root / f"{name}.hea"
        if not p.exists():
            rows.append({"record": name, "header_found": False, "patient": name.split("/")[0]})
            continue
        h = parse_header(p)
        row = {"record": name, "header_found": True, "patient": name.split("/")[0],
               **header_row(h),
               "standard12_present": standard12_channel_map(h.lead_names) is not None}
        row.update({f"c:{k}": v for k, v in h.comment_fields.items()})
        rows.append(row)
    return pd.DataFrame(rows)


def comment_counts(rec: pd.DataFrame) -> pd.DataFrame:
    parts = []
    for col in [c for c in rec.columns if c.startswith("c:")]:
        vals = rec[col].fillna(MISSING).astype(str)
        g = rec.assign(v=vals).groupby("v")
        parts.append(pd.DataFrame({"key": col[2:], "value": g.size().index,
                                   "n_records": g.size().to_numpy(),
                                   "n_patients": g["patient"].nunique().to_numpy()}))
    if not parts:
        return pd.DataFrame(columns=["key", "value", "n_records", "n_patients"])
    return pd.concat(parts, ignore_index=True).sort_values(["key", "n_records"],
                                                           ascending=[True, False])


def mi_timing(rec: pd.DataFrame, keys: dict) -> pd.DataFrame:
    rk, dk, ek = keys["reason"], keys["infarct_date"], keys["ecg_date"]
    if not rk:
        return pd.DataFrame({"note": ["reason-for-admission key not found"]})
    mi = rec[rec[f"c:{rk}"].astype(str).str.contains("infarct", case=False, na=False)].copy()
    cols = ["record", "patient", f"c:{rk}"]
    for k in (keys["acute_loc"], keys["former_loc"], dk, ek):
        if k:
            cols.append(f"c:{k}")
    out = mi[cols].copy()
    if dk and ek:
        d_inf = mi[f"c:{dk}"].map(parse_date)
        d_ecg = mi[f"c:{ek}"].map(parse_date)
        out["days_ecg_minus_infarction"] = [
            (e - i).days if e is not None and i is not None else None
            for e, i in zip(d_ecg, d_inf)]
    return out


def review(root: Path, out_dir: Path = RESULTS_DIR) -> dict:
    rec = record_table(root)
    allkeys = [c[2:] for c in rec.columns if c.startswith("c:")]
    keys = {name: find_key(allkeys, pat) for name, pat in KEY_PATTERNS.items()}
    counts = comment_counts(rec)
    timing = mi_timing(rec, keys)

    out_dir.mkdir(parents=True, exist_ok=True)
    rec.to_csv(out_dir / "ptb_diagnostic_records.csv", index=False)
    counts.to_csv(out_dir / "ptb_diagnostic_comment_counts.csv", index=False)
    timing.to_csv(out_dir / "ptb_diagnostic_mi_timing.csv", index=False)

    found = rec[rec["header_found"]]
    controls = root / "CONTROLS"
    n_controls = (len([l for l in controls.read_text().splitlines() if l.strip()])
                  if controls.exists() else "not found")
    basics = {
        "records in RECORDS": len(rec),
        "headers found": int(rec["header_found"].sum()),
        "distinct patient folders (RECORDS)": rec["patient"].nunique(),
        "lines in CONTROLS": n_controls,
        "n_sig values": ", ".join(f"{k}: {v}" for k, v in found["n_sig"].value_counts().items()),
        "fs values": ", ".join(f"{k:g}: {v}" for k, v in found["fs"].value_counts().items()),
        "duration s min / median / max": f"{found['duration_s'].min():g} / {found['duration_s'].median():g} / {found['duration_s'].max():g}",
        "records with all standard 12 leads by name": int(found["standard12_present"].sum()),
        "lead name sets": "; ".join(found["lead_names"].value_counts().index),
        "units values": ", ".join(found["units"].fillna("not given").value_counts().index),
        "comment keys found": "; ".join(allkeys) or "none",
        **{f"key used for {k}": v or "not found" for k, v in keys.items()},
    }
    reason_tbl = (counts[counts["key"] == keys["reason"]] if keys["reason"]
                  else pd.DataFrame({"note": ["not found"]}))
    timing_note = "Dates not both present; no day differences computed."
    if "days_ecg_minus_infarction" in timing.columns:
        d = timing["days_ecg_minus_infarction"].dropna()
        timing_note = (f"MI records (reason contains 'infarct'): {len(timing)}; "
                       f"patients {timing['patient'].nunique()}; with both dates parsed: {len(d)}.\n\n"
                       + md_table(d.describe().rename("days").reset_index())
                       + "\n\nDay bands (records): "
                       + ", ".join(f"{k}: {v}" for k, v in pd.cut(
                           d, [-10**6, -1, 1, 3, 7, 28, 10**6],
                           labels=["<0", "0-1", "2-3", "4-7", "8-28", ">28"]).value_counts(sort=False).items()))
    sections = [
        ("Basic counts", md_table(pd.DataFrame(list(basics.items()), columns=["item", "value"]))),
        ("Reason for admission (records / patients)", md_table(reason_tbl)),
        ("MI timing: ECG date minus infarction date (listing only; not an acute label, L2)",
         timing_note),
    ]
    for k in ("acute_loc", "former_loc"):
        if keys[k]:
            sections.append((f"{keys[k]} (records / patients)",
                             md_table(counts[counts["key"] == keys[k]])))
    files = [root / "RECORDS"] + ([controls] if controls.exists() else [])
    write_summary(out_dir / "ptb_diagnostic_summary.md",
                  "PTB Diagnostic ECG Database review (local observation)", DATASET_ID, RELEASE,
                  SCRIPT, provenance(files), sections
                  + [("Header files", f"{int(rec['header_found'].sum())} .hea files listed in RECORDS; "
                      "per-file provenance in results/download_manifest.csv.")])
    return {"records": rec, "counts": counts, "timing": timing, "basics": basics, "keys": keys}


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("root", type=Path, help="data/samples/ptb_diagnostic")
    ap.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    args = ap.parse_args(argv)
    res = review(args.root, args.out_dir)
    for k, v in res["basics"].items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
