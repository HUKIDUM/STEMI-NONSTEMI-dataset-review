"""ID-level overlap checks between related releases (step S10). IDs only, never signals (O9).

    .venv/bin/python -I src/stemi/review/overlap_ids.py

Checks (each reports what it could and could not compare):
- PTB-XL native 1.0.3 `ecg_id` vs Challenge 2021 `ptb-xl` record names (g*/RECORDS).
  Mapping "HRnnnnn" -> ecg_id nnnnn is an ASSUMPTION; it is only tested here
  (does the numeric range fit?), and confirming it needs headers (separate request).
- PTB Diagnostic native (RECORDS, 549) vs Challenge `ptb` names (516): names differ in
  form, so only counts are compared unless a mapping is found.
- CPSC 2018 vs CPSC-Extra: record-name prefixes and numeric ranges in the g1 samples.
Outputs: results/overlap_ids.csv, results/overlap_ids_summary.md
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

SAMPLES = Path(__file__).resolve().parents[3] / "data" / "samples"
SCRIPT = "src/stemi/review/overlap_ids.py"


def read_records(files: list[Path]) -> list[str]:
    out = []
    for f in files:
        out += [ln.strip() for ln in f.read_text().splitlines() if ln.strip()]
    return out


def split_name(name: str) -> tuple[str, int | None]:
    m = re.fullmatch(r"([A-Za-z_]*)(\d+)", name)
    return (m[1], int(m[2])) if m else (name, None)


def ptbxl_check(samples: Path) -> list[dict]:
    db = samples / "ptb_xl" / "ptbxl_database.csv"
    rec = sorted((samples / "ptb_xl" / "challenge-2021" / "training" / "ptb-xl").glob("g*/RECORDS"))
    if not db.exists() or not rec:
        return [{"check": "ptb_xl native vs challenge", "result": "not run: input missing"}]
    native = set(pd.read_csv(db, usecols=["ecg_id"])["ecg_id"].astype(int))
    names = read_records(rec)
    parts = [split_name(n) for n in names]
    prefixes = sorted({p for p, _ in parts})
    nums = {n for _, n in parts if n is not None}
    rows = [
        {"check": "ptb_xl: native ecg_id count", "result": len(native)},
        {"check": "ptb_xl: challenge record names", "result": len(names)},
        {"check": "ptb_xl: challenge distinct names", "result": len(set(names))},
        {"check": "ptb_xl: challenge name prefixes", "result": ", ".join(prefixes)},
        {"check": "ptb_xl: challenge numeric range", "result": f"{min(nums)}–{max(nums)}" if nums else "n/a"},
        {"check": "ptb_xl: native ecg_id range", "result": f"{min(native)}–{max(native)}"},
        {"check": "ptb_xl: numbers in both (IF HRn = ecg_id n; ASSUMPTION)", "result": len(nums & native)},
        {"check": "ptb_xl: challenge numbers not in native 1.0.3", "result": len(nums - native)},
        {"check": "ptb_xl: native ecg_id not in challenge", "result": len(native - nums)},
        {"check": "ptb_xl: challenge-only numbers (first 40)",
         "result": ", ".join(map(str, sorted(nums - native)[:40])) or "none"},
    ]
    return rows


def ptbdb_check(samples: Path) -> list[dict]:
    native_f = samples / "ptb_diagnostic" / "RECORDS"
    rec = sorted((samples / "ptb_diagnostic" / "challenge-2021" / "training" / "ptb").glob("g*/RECORDS"))
    if not native_f.exists() or not rec:
        return [{"check": "ptb_diagnostic native vs challenge", "result": "not run: input missing"}]
    native = read_records([native_f])
    names = read_records(rec)
    prefixes = sorted({split_name(n)[0] for n in names})
    nums = sorted(n for _, n in map(split_name, names) if n is not None)
    native_stems = {n.split("/")[-1] for n in native}
    return [
        {"check": "ptb_diagnostic: native records", "result": len(native)},
        {"check": "ptb_diagnostic: native patient folders", "result": len({n.split('/')[0] for n in native})},
        {"check": "ptb_diagnostic: challenge record names", "result": len(names)},
        {"check": "ptb_diagnostic: challenge name prefixes", "result": ", ".join(prefixes)},
        {"check": "ptb_diagnostic: challenge numeric range", "result": f"{nums[0]}–{nums[-1]}" if nums else "n/a"},
        {"check": "ptb_diagnostic: challenge names equal to a native record stem",
         "result": len(set(names) & native_stems)},
        {"check": "ptb_diagnostic: numbers 1..len(native RECORDS) missing from challenge",
         "result": ", ".join(map(str, sorted(set(range(1, len(native) + 1)) - set(nums)))) or "none"},
        {"check": "ptb_diagnostic: those native records IF Sn = n-th line of native RECORDS (ASSUMPTION)",
         "result": ", ".join(native[n - 1] for n in sorted(set(range(1, len(native) + 1)) - set(nums)))
                   or "none"},
        {"check": "ptb_diagnostic: record-level mapping",
         "result": "not possible from RECORDS alone (name forms differ); counts only"
         if not set(names) & native_stems else "partial name match, see counts"},
    ]


def cpsc_check(samples: Path) -> list[dict]:
    rows = []
    for ds, folder in (("cpsc_2018", "cpsc_2018"), ("cpsc_extra", "cpsc_2018_extra")):
        rec = sorted((samples / ds / "training" / folder).glob("g*/RECORDS"))
        if not rec:
            rows.append({"check": f"{ds}: g1 names", "result": "not run: input missing"})
            continue
        names = read_records(rec)
        parts = [split_name(n) for n in names]
        nums = sorted(n for _, n in parts if n is not None)
        rows.append({"check": f"{ds}: g1 RECORDS names (sample only)",
                     "result": f"{len(names)}; prefixes {', '.join(sorted({p for p, _ in parts}))}; "
                               f"numbers {nums[0]}–{nums[-1]}"})
    rows.append({"check": "cpsc_2018 vs cpsc_extra",
                 "result": "different name prefixes in the g1 samples; this does not show that the "
                           "ECGs are distinct (O5, O9: signal-level duplicates not assessed)"})
    return rows


def review(samples: Path = SAMPLES, out_dir: Path = RESULTS_DIR) -> pd.DataFrame:
    rows = ptbxl_check(samples) + ptbdb_check(samples) + cpsc_check(samples)
    df = pd.DataFrame(rows)
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_dir / "overlap_ids.csv", index=False)
    inputs = [p for p in [samples / "ptb_xl" / "ptbxl_database.csv", samples / "ptb_diagnostic" / "RECORDS"]
              if p.exists()]
    inputs += sorted((samples / "ptb_xl" / "challenge-2021").rglob("RECORDS"))[:2]
    inputs += sorted((samples / "ptb_diagnostic" / "challenge-2021").rglob("RECORDS"))[:2]
    write_summary(out_dir / "overlap_ids_summary.md", "Release overlap by ID (local observation)",
                  "ptb_xl, ptb_diagnostic, cpsc_2018, cpsc_extra",
                  "native vs Challenge 2021 1.0.3", SCRIPT, provenance(inputs),
                  [("ID checks", md_table(df)),
                   ("Limits", "IDs and counts only. No waveforms were compared, so signal-level "
                              "duplicates are not assessed (O9). Name-to-ID mappings marked ASSUMPTION "
                              "are untested until headers are read.")])
    return df


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--samples", type=Path, default=SAMPLES)
    ap.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    args = ap.parse_args(argv)
    print(review(args.samples, args.out_dir).to_string(index=False))


if __name__ == "__main__":
    main()
