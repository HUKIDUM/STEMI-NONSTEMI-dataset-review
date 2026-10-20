"""PhysioNet Challenge 2021 (1.0.3) source review (step S7). Reads .hea text only.

    .venv/bin/python -I src/stemi/review/review_challenge.py cpsc_2018 data/samples/cpsc_2018 \
        --maps data/samples/challenge_label_maps

``#Dx`` holds comma-separated SNOMED CT codes. Code names come from the map files
found in --maps (ConditionNames_SNOMED-CT.csv, dx_mapping_scored.csv,
dx_mapping_unscored.csv); a code in none of them is "unmapped". Keyword flags
on names are for listing only (L2).

Outputs (results/), prefix challenge_<dataset_id>_:
    dx_counts.csv     SNOMED code: records, name, map source, keyword flags
    headers.csv       one row per header (fs, samples, duration, leads, gain, units, age, sex)
    comment_keys.csv  every comment key with record count (e.g. is there any patient ID?)
    summary.md
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

RELEASE = "PhysioNet Challenge 2021, 1.0.3"
SCRIPT = "src/stemi/review/review_challenge.py"
FOLDERS = {"cpsc_2018": "cpsc_2018", "cpsc_extra": "cpsc_2018_extra", "georgia": "georgia",
           "ningbo": "ningbo", "chapman_shaoxing": "chapman_shaoxing",
           "ptb_xl_challenge": "ptb-xl", "ptb_diagnostic_challenge": "ptb"}
MAP_FILES = ("ConditionNames_SNOMED-CT.csv", "dx_mapping_scored.csv", "dx_mapping_unscored.csv")


def _col(cols, pattern):
    hits = [c for c in cols if re.search(pattern, str(c), flags=re.IGNORECASE)]
    return hits[0] if hits else None


def load_maps(maps_dir: Path | None) -> pd.DataFrame:
    """code -> name (first map file that has it wins, in MAP_FILES order), abbreviation."""
    parts = []
    for fname in MAP_FILES:
        p = maps_dir / fname if maps_dir else None
        if p is None or not p.exists():
            continue
        m = pd.read_csv(p, dtype=str)
        code = _col(m.columns, r"snomed")
        name = _col(m.columns, r"^(dx|full name)$") or _col(m.columns, r"name|dx")
        abbr = _col(m.columns, r"abbrev|acronym")
        if not code or not name:
            continue
        parts.append(pd.DataFrame({"code": m[code].str.strip(), "name": m[name].str.strip(),
                                   "abbreviation": m[abbr].str.strip() if abbr else None,
                                   "map_source": fname}))
    if not parts:
        return pd.DataFrame(columns=["code", "name", "abbreviation", "map_source"])
    return pd.concat(parts, ignore_index=True).drop_duplicates("code")


def header_files(root: Path, folder: str) -> list[Path]:
    return sorted((root / "training" / folder).glob("g*/*.hea"))


def read_headers(files: list[Path], root: Path) -> pd.DataFrame:
    rows = []
    for p in files:
        h = parse_header(p)
        f = h.comment_fields
        rows.append({"file": p.relative_to(root).as_posix(), **header_row(h),
                     "age": f.get("Age"), "sex": f.get("Sex"), "dx": f.get("Dx", ""),
                     "comment_keys": "|".join(f)})
    return pd.DataFrame(rows)


def dx_counts(hdr: pd.DataFrame, maps: pd.DataFrame) -> pd.DataFrame:
    long = hdr[["record_name", "dx"]].assign(code=hdr["dx"].fillna("").str.split(","))
    long = long.explode("code")
    long["code"] = long["code"].str.strip()
    long = long[long["code"] != ""].drop_duplicates(["record_name", "code"])
    out = long.groupby("code").size().rename("n_records").reset_index()
    out = out.merge(maps, on="code", how="left")
    out["name"] = out["name"].fillna("unmapped")
    flags = pd.DataFrame([keyword_flags(n if n != "unmapped" else "") for n in out["name"]])
    out = pd.concat([out, flags], axis=1)
    out["any_mi_st_keyword"] = flags.any(axis=1)
    return out.sort_values("n_records", ascending=False)


def review(dataset_id: str, root: Path, maps_dir: Path | None,
           out_dir: Path = RESULTS_DIR) -> dict:
    folder = FOLDERS[dataset_id]
    files = header_files(root, folder)
    if not files:
        raise FileNotFoundError(f"no headers under {root}/training/{folder}/g*/")
    hdr = read_headers(files, root)
    maps = load_maps(maps_dir)
    dx = dx_counts(hdr, maps)
    keys = (hdr["comment_keys"].str.split("|").explode().value_counts()
            .rename_axis("comment_key").rename("n_records").reset_index())

    pre = f"challenge_{dataset_id}_"
    out_dir.mkdir(parents=True, exist_ok=True)
    dx.to_csv(out_dir / f"{pre}dx_counts.csv", index=False)
    hdr.to_csv(out_dir / f"{pre}headers.csv", index=False)
    keys.to_csv(out_dir / f"{pre}comment_keys.csv", index=False)

    listed = sorted({ln.strip().rstrip("/") for g in (root / "training" / folder).glob("g*/RECORDS")
                     for ln in g.read_text().splitlines() if ln.strip()})
    dur = hdr["duration_s"]
    basics = {
        "headers read": len(hdr),
        "records listed in g*/RECORDS": len(listed),
        "distinct record names": hdr["record_name"].nunique(),
        "records with empty Dx": int((hdr["dx"].fillna("") == "").sum()),
        "fs values": "; ".join(f"{k:g}: {v}" for k, v in hdr["fs"].value_counts().items()),
        "n_sig values": "; ".join(f"{k}: {v}" for k, v in hdr["n_sig"].value_counts().items()),
        "duration s min / median / max": f"{dur.min():g} / {dur.median():g} / {dur.max():g}",
        "duration s, top 5 values": "; ".join(f"{k:g}: {v}" for k, v in dur.value_counts().head(5).items()),
        "records with duration exactly 10 s": int((dur == 10).sum()),
        "lead name sets": "; ".join(f"{k} ({v})" for k, v in hdr["lead_names"].value_counts().items()),
        "gains": "; ".join(f"{k}: {v}" for k, v in hdr["gains"].value_counts().items()),
        "units": "; ".join(f"{k}: {v}" for k, v in hdr["units"].fillna("not given").value_counts().items()),
        "sex values": "; ".join(f"{k}: {v}" for k, v in hdr["sex"].fillna("<missing>").value_counts().items()),
        "age (numeric) min / median / max": (lambda a: f"{a.min():g} / {a.median():g} / {a.max():g}")(
            pd.to_numeric(hdr["age"], errors="coerce")),
        "age non-numeric values": "; ".join(f"{k}: {v}" for k, v in hdr.loc[
            pd.to_numeric(hdr["age"], errors="coerce").isna(), "age"].fillna("<missing>").value_counts().items()) or "none",
        "comment keys": "; ".join(f"{k} ({v})" for k, v in zip(keys["comment_key"], keys["n_records"])),
        "any patient-ID-like comment key": ", ".join(k for k in keys["comment_key"]
                                                     if re.search(r"patient|subject|id", k, re.I)) or "none found",
        "distinct SNOMED codes": len(dx),
        "unmapped codes": ", ".join(dx.loc[dx["name"] == "unmapped", "code"]) or "none",
        "map files used": ", ".join(sorted(maps["map_source"].unique())) or "none (all unmapped)",
    }
    mi = dx[dx["any_mi_st_keyword"]]
    mi_records = hdr[hdr["dx"].fillna("").str.split(",").map(
        lambda cs: bool(set(c.strip() for c in cs) & set(mi["code"])))]
    sections = [
        ("Basic counts", md_table(pd.DataFrame(list(basics.items()), columns=["item", "value"]))),
        ("SNOMED codes whose name matches an MI / ST / ischaemia keyword (listing only; L2)",
         f"Records with any: {len(mi_records)}. Keyword regexes: "
         + "; ".join(f"{k} = `{v}`" for k, v in MI_KEYWORDS.items()) + "\n\n"
         + md_table(mi[["code", "name", "abbreviation", "n_records", "map_source"]
                       + list(MI_KEYWORDS)])),
        ("All SNOMED codes (top 40 by records; full list in dx_counts.csv)",
         md_table(dx[["code", "name", "abbreviation", "n_records"]], max_rows=40)),
    ]
    inputs = provenance(sorted((root / "training" / folder).glob("g*/RECORDS"))[:3]
                        + [maps_dir / f for f in MAP_FILES if maps_dir and (maps_dir / f).exists()])
    write_summary(out_dir / f"{pre}summary.md",
                  f"Challenge 2021 `{folder}` header review (local observation)", dataset_id,
                  RELEASE, SCRIPT, inputs,
                  sections + [("Input note", f"Input table lists the first 3 g*/RECORDS files and the "
                                              f"map files; all {len(hdr)} headers are logged in "
                                              "results/download_manifest.csv.")])
    return {"headers": hdr, "dx": dx, "keys": keys, "basics": basics, "mi_records": len(mi_records)}


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("dataset_id", choices=sorted(FOLDERS))
    ap.add_argument("root", type=Path, help="data/samples/<dataset_id>")
    ap.add_argument("--maps", type=Path, default=None, help="folder with SNOMED map CSVs")
    ap.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    args = ap.parse_args(argv)
    res = review(args.dataset_id, args.root, args.maps, args.out_dir)
    for k, v in res["basics"].items():
        print(f"{k}: {v}")
    print(f"records with an MI/ST keyword code: {res['mi_records']}")


if __name__ == "__main__":
    main()
