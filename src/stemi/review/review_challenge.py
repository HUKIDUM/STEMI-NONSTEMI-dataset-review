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
    MI_KEYWORDS, RESULTS_DIR, keyword_flags, md_table, provenance, read_text_csv, write_summary,
)
from stemi.review.hea_parser import header_row, parse_header

RELEASE = "PhysioNet Challenge 2021, 1.0.3"
SCRIPT = "src/stemi/review/review_challenge.py"
FOLDERS = {"cpsc_2018": "cpsc_2018", "cpsc_extra": "cpsc_2018_extra", "georgia": "georgia",
           "ningbo": "ningbo", "chapman_shaoxing": "chapman_shaoxing",
           "ptb_xl_challenge": "ptb-xl", "ptb_diagnostic_challenge": "ptb"}
# Challenge-2021 dx_mapping names come first (they are the Challenge's own names);
# ConditionNames (ecg-arrhythmia) names are kept as alt_name, e.g. 164931005 is
# "st elevation" in dx_mapping but "ST tilt up" in ConditionNames.
MAP_FILES = ("dx_mapping_scored.csv", "dx_mapping_unscored.csv", "ConditionNames_SNOMED-CT.csv")


def _col(cols, pattern):
    hits = [c for c in cols if re.search(pattern, str(c), flags=re.IGNORECASE)]
    return hits[0] if hits else None


def load_maps(maps_dir: Path | None) -> pd.DataFrame:
    """code -> name (first map file that has it wins, in MAP_FILES order), abbreviation,
    map_source, and alt_name = every other distinct name for the code (joined by ' | ')."""
    parts = []
    for fname in MAP_FILES:
        p = maps_dir / fname if maps_dir else None
        if p is None or not p.exists():
            continue
        m = read_text_csv(p, dtype=str)
        code = _col(m.columns, r"snomed")
        name = _col(m.columns, r"^(dx|full name)$") or _col(m.columns, r"name|dx")
        abbr = _col(m.columns, r"abbrev|acronym")
        if not code or not name:
            continue
        parts.append(pd.DataFrame({"code": m[code].str.strip(), "name": m[name].str.strip(),
                                   "abbreviation": m[abbr].str.strip() if abbr else None,
                                   "map_source": fname}))
    if not parts:
        return pd.DataFrame(columns=["code", "name", "abbreviation", "map_source", "alt_name"])
    allm = pd.concat(parts, ignore_index=True)
    first = allm.drop_duplicates("code").set_index("code")
    alt = {}
    for code, grp in allm.groupby("code"):
        main = str(first.at[code, "name"]).lower()
        alt[code] = " | ".join(sorted({n for n in grp["name"].dropna() if n.lower() != main}))
    return first.assign(alt_name=pd.Series(alt)).reset_index()


MAP_COUNT_COLUMNS = {"cpsc_2018": "CPSC", "cpsc_extra": "CPSC_Extra", "incart": "StPetersburg",
                     "ptb_diagnostic_challenge": "PTB", "ptb_xl_challenge": "PTB_XL",
                     "georgia": "Georgia", "chapman_shaoxing": "Chapman_Shaoxing",
                     "ningbo": "Ningbo"}


def map_file_counts(maps_dir: Path) -> pd.DataFrame:
    """Per-source counts printed in dx_mapping_scored/unscored.csv (publisher file), one row
    per SNOMED code, with keyword flags on the Dx name (listing only)."""
    parts = []
    for fname in ("dx_mapping_scored.csv", "dx_mapping_unscored.csv"):
        p = maps_dir / fname
        if p.exists():
            m = read_text_csv(p, dtype={"SNOMEDCTCode": str})
            parts.append(m.assign(map_file=fname))
    if not parts:
        return pd.DataFrame()
    m = pd.concat(parts, ignore_index=True)
    flags = pd.DataFrame([keyword_flags(d) for d in m["Dx"]])
    m = pd.concat([m, flags], axis=1)
    m["any_mi_st_keyword"] = flags.drop(columns="kw_st_other").any(axis=1)
    return m


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
    texts = [("" if n == "unmapped" else n) + " " + ("" if pd.isna(a) else a)
             for n, a in zip(out["name"], out.get("alt_name", pd.Series([None] * len(out))))]
    flags = pd.DataFrame([keyword_flags(t) for t in texts])
    out = pd.concat([out, flags], axis=1)
    out["any_mi_st_keyword"] = flags.drop(columns="kw_st_other").any(axis=1)
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
    pub_col = MAP_COUNT_COLUMNS.get(dataset_id)
    if maps_dir is not None and pub_col:
        pub = map_file_counts(maps_dir)
        if len(pub) and pub_col in pub.columns:
            pub = (pub[["SNOMEDCTCode", pub_col]].drop_duplicates("SNOMEDCTCode")
                   .rename(columns={"SNOMEDCTCode": "code", pub_col: "publisher_count_full_source"}))
            dx = dx.merge(pub, on="code", how="left")
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
        ("Scope", f"**g1 sample only ({len(hdr)} of {len(listed)} records listed in g1/RECORDS; "
                  f"not the full source).** `publisher_count_full_source` = the "
                  f"`{pub_col}` column of dx_mapping_*.csv (publisher's counts, meaning not defined "
                  f"by the publisher). Header checksums: not available (SHA256SUMS stream not "
                  f"approved); see results/download_manifest.csv."),
        ("SNOMED codes whose name matches an MI / ST / ischaemia keyword (listing only; L2)",
         f"Records with any: {len(mi_records)}. Keyword regexes: "
         + "; ".join(f"{k} = `{v}`" for k, v in MI_KEYWORDS.items()) + "\n\n"
         + md_table(mi[[c for c in ["code", "name", "alt_name", "abbreviation", "n_records",
                                     "publisher_count_full_source", "map_source"] if c in mi.columns]])),
        ("Other ST codes for review (kw_st_other; NOT MI-related by themselves)",
         md_table(dx[dx["kw_st_other"] & ~dx["any_mi_st_keyword"]][
             [c for c in ["code", "name", "alt_name", "abbreviation", "n_records",
                          "publisher_count_full_source"] if c in dx.columns]])),
        ("All SNOMED codes (top 40 by records; full list in dx_counts.csv)",
         md_table(dx[[c for c in ["code", "name", "abbreviation", "n_records",
                                   "publisher_count_full_source"] if c in dx.columns]], max_rows=40)),
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


def write_map_counts(maps_dir: Path, out_dir: Path = RESULTS_DIR) -> pd.DataFrame:
    m = map_file_counts(maps_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    m.to_csv(out_dir / "challenge_dx_mapping_counts.csv", index=False)
    return m


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    if argv is None:
        import sys
        argv = sys.argv[1:]
    if argv[:1] == ["--map-counts"]:
        m = write_map_counts(Path(argv[1]))
        cols = ["Dx", "SNOMEDCTCode", "Abbreviation"] + [c for c in MAP_COUNT_COLUMNS.values()
                                                         if c in m.columns] + ["Total"]
        print(m.loc[m["any_mi_st_keyword"] | m["kw_st_other"], cols + ["kw_st_other"]].to_string(index=False))
        return
    ap.add_argument("dataset_id", choices=sorted(FOLDERS))
    ap.add_argument("root", type=Path, help="data/samples/<dataset_id>")
    ap.add_argument("--maps", type=Path, default=None, help="folder with SNOMED map CSVs")
    # also: review_challenge.py --map-counts <maps_dir>  -> results/challenge_dx_mapping_counts.csv
    ap.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    args = ap.parse_args(argv)
    res = review(args.dataset_id, args.root, args.maps, args.out_dir)
    for k, v in res["basics"].items():
        print(f"{k}: {v}")
    print(f"records with an MI/ST keyword code: {res['mi_records']}")


if __name__ == "__main__":
    main()
