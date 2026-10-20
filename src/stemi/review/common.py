"""Shared helpers for the review scripts: provenance lookup and summary writing."""

from __future__ import annotations

import csv
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RESULTS_DIR = PROJECT_ROOT / "results"
MANIFEST_CSV = RESULTS_DIR / "download_manifest.csv"

OBSERVATION_NOTE = ("Local observation of the downloaded file(s) named below; not a release-level "
                    "fact (data_contract E2, E3). Labels are described, not converted into "
                    "training labels (L1, L2).")

# Keyword flags used only to LIST statements for review (L2): a flag never makes a label.
MI_KEYWORDS = {
    "kw_infarct": r"infarct|\bMI\b|STEMI",
    "kw_injury": r"injury",
    "kw_st_elev": r"ST[\s-]*elev|\bSTE\b",
    "kw_st_depr": r"ST[\s-]*depr|\bSTD\b",
    "kw_ischemi": r"isch[a]?emi",
    "kw_acute": r"acute",
    "kw_q_wave": r"q[\s-]*wave",
}


def keyword_flags(text: str | None) -> dict[str, bool]:
    t = "" if text is None or (isinstance(text, float) and pd.isna(text)) else str(text)
    return {k: bool(re.search(p, t, flags=re.IGNORECASE)) for k, p in MI_KEYWORDS.items()}


def provenance(local_paths: list[Path], manifest: Path = MANIFEST_CSV) -> pd.DataFrame:
    """url / sha256 / download date / checksum match for each local file, from the manifest."""
    rows = []
    known = {}
    if manifest.exists():
        with open(manifest, newline="") as f:
            for r in csv.DictReader(f):
                if r.get("sha256"):
                    known[r["local_path"]] = r            # last row for a path wins
    for p in local_paths:
        rel = Path(p).resolve()
        key = rel.relative_to(PROJECT_ROOT).as_posix() if rel.is_relative_to(PROJECT_ROOT) else str(p)
        r = known.get(key, {})
        rows.append({"local_path": key, "url": r.get("url", "not in download_manifest.csv"),
                     "sha256": r.get("sha256", ""), "download_utc": r.get("download_utc", ""),
                     "checksum_match": r.get("checksum_match", "")})
    return pd.DataFrame(rows)


def md_table(df: pd.DataFrame, max_rows: int | None = None) -> str:
    if max_rows is not None:
        df = df.head(max_rows)
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for row in df.itertuples(index=False):
        lines.append("| " + " | ".join("" if pd.isna(v) else str(v) for v in row) + " |")
    return "\n".join(lines)


def write_summary(path: Path, title: str, dataset_id: str, release: str, script: str,
                  inputs: pd.DataFrame, sections: list[tuple[str, str]]) -> None:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    parts = [f"# {title}", "",
             f"- Dataset: `{dataset_id}`, release {release}",
             f"- Script: `{script}`; generated {now}",
             f"- {OBSERVATION_NOTE}", "", "## Input files", "", md_table(inputs), ""]
    for head, body in sections:
        parts += [f"## {head}", "", body.rstrip(), ""]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(parts))
