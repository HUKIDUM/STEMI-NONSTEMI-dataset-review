"""INCART 12-lead arrhythmia database 1.0.0 review (step S9). .hea and text files only.

    .venv/bin/python -I src/stemi/review/review_incart.py data/samples/incart

Outputs (results/):
    incart_headers.csv   one row per header (fs, samples, duration, leads, gains, comments)
    incart_summary.md    header stats, plus the verbatim text files (record descriptions,
                         patients/diagnoses) so diagnoses are read from the source text
Lines mentioning infarct are listed for review only (L2).
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

DATASET_ID = "incart"
RELEASE = "1.0.0 native"
SCRIPT = "src/stemi/review/review_incart.py"
TEXT_FILES = ("record-descriptions.txt", "files-patients-diagnoses.txt", "ANNOTATORS", "README")


def review(root: Path, out_dir: Path = RESULTS_DIR) -> dict:
    names = [l.strip() for l in (root / "RECORDS").read_text().splitlines() if l.strip()]
    rows = []
    for n in names:
        p = root / f"{n}.hea"
        if p.exists():
            h = parse_header(p)
            rows.append({"record": n, **header_row(h), "comments": " | ".join(h.comments)})
        else:
            rows.append({"record": n, "header_found": False})
    hdr = pd.DataFrame(rows)
    out_dir.mkdir(parents=True, exist_ok=True)
    hdr.to_csv(out_dir / "incart_headers.csv", index=False)

    dur = hdr["duration_s"]
    basics = {
        "records in RECORDS": len(names),
        "headers read": int(hdr["n_sig"].notna().sum()),
        "fs values": "; ".join(f"{k:g}: {v}" for k, v in hdr["fs"].value_counts().items()),
        "n_sig values": "; ".join(f"{k:g}: {v}" for k, v in hdr["n_sig"].value_counts().items()),
        "duration s min / max": f"{dur.min():g} / {dur.max():g}",
        "lead name sets": "; ".join(f"{k} ({v})" for k, v in hdr["lead_names"].value_counts().items()),
        "gains": "; ".join(f"{k} ({v})" for k, v in hdr["gains"].value_counts().items()),
        "units": "; ".join(hdr["units"].fillna("not given").unique()),
    }
    sections = [("Basic counts", md_table(pd.DataFrame(list(basics.items()),
                                                        columns=["item", "value"])))]
    infarct_lines = []
    for f in TEXT_FILES:
        p = root / f
        if not p.exists():
            sections.append((f"{f}", "not downloaded / not found"))
            continue
        text = p.read_text(errors="replace")
        infarct_lines += [f"{f}: {ln.strip()}" for ln in text.splitlines()
                          if re.search(r"infarct|\bMI\b|ischem|isch(a)?emi", ln, re.I)]
        sections.append((f"{f} (verbatim)", "```\n" + text.strip() + "\n```"))
    sections.insert(1, ("Lines mentioning infarct / MI / ischemia (listing only)",
                        "\n".join(f"- {l}" for l in infarct_lines) or "none"))
    sections.append(("Header comments (per record)",
                     md_table(hdr[["record", "comments"]]) if "comments" in hdr else "none"))
    write_summary(out_dir / "incart_summary.md", "INCART review (local observation)",
                  DATASET_ID, RELEASE, SCRIPT,
                  provenance([root / "RECORDS"] + [root / f for f in TEXT_FILES if (root / f).exists()]),
                  sections)
    return {"headers": hdr, "basics": basics, "infarct_lines": infarct_lines}


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("root", type=Path, help="data/samples/incart")
    ap.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    args = ap.parse_args(argv)
    res = review(args.root, args.out_dir)
    for k, v in res["basics"].items():
        print(f"{k}: {v}")
    print("\n".join(res["infarct_lines"]))


if __name__ == "__main__":
    main()
