"""Pairwise combinability matrix for the 11 datasets (step S10).

    .venv/bin/python -I src/stemi/review/combine_matrix.py

Mechanical: attributes below are copied from VERIFIED rows of results/verified_facts.md
(each attribute names its row), and `verdict()` applies planner's rules in order. No
new judgement is made here. Outputs: results/combine_matrix.csv (55 unordered pairs),
results/combine_matrix_summary.md.
"""

from __future__ import annotations

if __package__ in (None, ""):          # run as a file under ``python -I``
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import argparse
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import pandas as pd

from stemi.review.common import RESULTS_DIR, md_table

SCRIPT = "src/stemi/review/combine_matrix.py"
TARGET_FS = 500                       # C1.3 provisional study setting
REF_GAIN = 1000.0                     # adc units per mV in PTB-XL and Challenge g1 headers


@dataclass(frozen=True)
class Attr:
    fs: float
    fixed_10s: bool
    duration: str
    lead_map_needed: bool             # rule c (lead order / naming differs)
    lead_note: str
    gain: float | None                # None = unknown (rule d)
    patient_id: bool                  # rule e
    labels: str                       # rule f
    rows: str                         # verified_facts rows used


CH = "Q5 device (g1); Q8 combine (technical part)"
ATTRS: dict[str, Attr] = {
    "ptb_xl": Attr(500, True, "10 s", False, "I…AVF, V1–V6 (upper case)", 1000.0, True,
                   "SCP-ECG statements", "ptb_xl Q1, Q5, Q8"),
    "mimic_iv_ecg": Attr(500, True, "10 s", True, "aVF before aVL", 200.0, True,
                         "machine text / ICD (credentialed)", "mimic_iv_ecg Q1, Q5, Q8"),
    "ptb_diagnostic": Attr(1000, False, "32–120 s", True, "15 ch, lower-case names", 2000.0, True,
                           "free-text clinical summary", "ptb_diagnostic Q1, Q5, Q8"),
    "sph": Attr(500, False, "10–56 s", False, "I…aVF, V1–V6", None, True,
                "AHA statements", "sph Q1, Q5, Q8"),
    "cpsc_2018": Attr(500, False, "9–118 s (g1)", False, "I…aVF, V1–V6", 1000.0, False,
                      "SNOMED CT", f"cpsc_2018 Q1, {CH}"),
    "cpsc_extra": Attr(500, False, "9.996–98 s (g1)", False, "I…aVF, V1–V6", 1000.0, False,
                       "SNOMED CT", f"cpsc_extra Q1, {CH}"),
    "georgia": Attr(500, False, "5–10 s", False, "I…aVF, V1–V6", 1000.0, False,
                    "SNOMED CT", f"georgia Q1, {CH}"),
    "chapman_shaoxing": Attr(500, True, "10 s", False, "I…aVF, V1–V6", 1000.0, False,
                             "SNOMED CT", f"chapman_shaoxing Q1, {CH}"),
    "ningbo": Attr(500, True, "10 s", False, "I…aVF, V1–V6", 1000.0, False,
                   "SNOMED CT", f"ningbo Q1, {CH}"),
    "code15": Attr(400, False, "7–10 s, zero-padded", True, "DI, DII, DIII names", None, True,
                   "rhythm flags (no MI labels)", "code15 Q1, Q5, Q6, Q8"),
    "incart": Attr(257, False, "1,800 s Holter", False, "I…AVF, V1–V6", None, True,
                   "beat annotations + patient text", "incart Q4, Q5, Q8"),
}
OVERLAP = {frozenset({"cpsc_2018", "cpsc_extra"}):
               ("same CPSC 2018 origin (O5)", "cpsc_2018, cpsc_extra Q8 combine (overlap: names)"),
           frozenset({"chapman_shaoxing", "ningbo"}):
               ("shared export; count match 10,247 + 34,905 = 45,152, complementary parts; never "
                "add ecg-arrhythmia on top (O4)", "chapman_shaoxing, ningbo Q8 combine (count match)")}


def verdict(a: str, b: str, attrs: dict[str, Attr] = ATTRS) -> tuple[str, list[str], list[str]]:
    """(verdict, reasons, verified_facts rows) for an unordered pair, rules in order."""
    A, B = attrs[a], attrs[b]
    rows = [A.rows, B.rows]
    if "incart" in (a, b):
        return ("No (supervised MI)",
                ["incart is 30-min Holter at 257 Hz, a different domain: windowed pretraining only"],
                rows + ["[MCR p.4]"])
    reasons = []
    fs_off = [f"{n} {x.fs:g} Hz" for n, x in ((a, A), (b, B)) if x.fs != TARGET_FS]
    if fs_off:
        reasons.append("a. resample: " + ", ".join(fs_off))
    dur = [f"{n} {x.duration}" for n, x in ((a, A), (b, B)) if not x.fixed_10s]
    if dur:
        reasons.append("b. length policy: " + ", ".join(dur))
    if A.lead_map_needed or B.lead_map_needed:
        reasons.append("c. lead map by name: " + ", ".join(
            f"{n} {x.lead_note}" for n, x in ((a, A), (b, B)) if x.lead_map_needed))
    if A.gain is None or B.gain is None or A.gain != B.gain:
        reasons.append("d. units/scale check: " + ", ".join(
            f"{n} {'unknown' if x.gain is None else f'{x.gain:g}/mV'}" for n, x in ((a, A), (b, B))))
    nopid = [n for n, x in ((a, A), (b, B)) if not x.patient_id]
    if nopid:
        reasons.append("e. no patient ID (" + ", ".join(nopid) + "): training use only (S7)")
    if A.labels != B.labels:
        extra = "; code15 has no MI labels at all" if "code15" in (a, b) else ""
        reasons.append(f"f. label systems differ: {A.labels} vs {B.labels}{extra}")
    ov = OVERLAP.get(frozenset({a, b}))
    if ov:
        reasons.append("g. overlap review: " + ov[0])
        rows.append(ov[1])
    return ("After checks" if reasons else "Yes (technical)"), reasons, rows


def build(out_dir: Path = RESULTS_DIR) -> pd.DataFrame:
    recs = []
    for a, b in combinations(ATTRS, 2):
        v, reasons, rows = verdict(a, b)
        recs.append({"ds_a": a, "ds_b": b, "verdict": v, "reasons": "; ".join(reasons),
                     "n_checks": len(reasons) if v == "After checks" else 0,
                     "source_rows": "verified_facts: " + " | ".join(rows)})
    df = pd.DataFrame(recs)
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_dir / "combine_matrix.csv", index=False)
    counts = df["verdict"].value_counts().rename_axis("verdict").rename("pairs").reset_index()
    after = df[df["verdict"] == "After checks"]
    fewest = after[after["n_checks"] == after["n_checks"].min()]
    attrs = pd.DataFrame([{"dataset": k, "fs_hz": v.fs, "duration": v.duration,
                           "lead_map_needed": v.lead_map_needed,
                           "gain_per_mV": "unknown" if v.gain is None else v.gain,
                           "patient_id": v.patient_id, "labels": v.labels, "rows": v.rows}
                          for k, v in ATTRS.items()])
    text = "\n".join([
        "# Combine matrix (mechanical; for planner review)", "",
        f"- Script: `{SCRIPT}`. Rules a–g and the incart rule as given by planner, applied in order; "
        "every applicable reason is listed. Attributes come only from verified_facts rows (table below).",
        "- Note: SPH gain is not observed (no SPH header or waveform was read), so rule d treats it as "
        "unknown. INCART gains vary per record, but the incart rule applies first.",
        "", "## Verdict counts", "", md_table(counts), "",
        f"## Pairs needing the fewest checks ({int(after['n_checks'].min())})", "",
        md_table(fewest[["ds_a", "ds_b", "reasons"]]), "",
        "## Number of checks per 'After checks' pair", "",
        md_table(after["n_checks"].value_counts().sort_index().rename_axis("n_checks")
                 .rename("pairs").reset_index()), "",
        "## Attributes used", "", md_table(attrs), ""])
    (out_dir / "combine_matrix_summary.md").write_text(text)
    return df


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    args = ap.parse_args(argv)
    df = build(args.out_dir)
    print(df["verdict"].value_counts().to_string())


if __name__ == "__main__":
    main()
