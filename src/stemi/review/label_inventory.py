"""Full label inventory per dataset (task S12-L, part L1). Uses only files in data/samples/.

    .venv/bin/python -I src/stemi/review/label_inventory.py

Writes results/label_inventory_<dataset>.csv (one row per label as written in the source)
and results/label_inventory_summary.md. Labels are listed, never converted (L1, L2).
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

from stemi.review.common import RESULTS_DIR, md_table, read_text_csv
from stemi.review.review_challenge import FOLDERS, MAP_COUNT_COLUMNS, load_maps, read_headers
from stemi.review.review_ptbdb import record_table
from stemi.review.review_ptbxl import explode_codes, load_statements
from stemi.review.review_sph import explode_statements

SAMPLES = Path(__file__).resolve().parents[3] / "data" / "samples"
MAPS = SAMPLES / "challenge_label_maps"
CHALLENGE_IDS = ("cpsc_2018", "cpsc_extra", "georgia", "chapman_shaoxing", "ningbo")
INV_COLUMNS = ["dataset_id", "label_kind", "label_as_written", "code", "code_system", "count",
               "count_type", "n_patients", "extra_count", "extra_count_type", "extra", "source_file"]
KEY_MISSING = "<key missing in header>"


def _rows(ds: str, recs: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(recs).reindex(columns=INV_COLUMNS)
    df["dataset_id"] = ds
    return df


def _rel(p: Path) -> str:
    try:
        return p.relative_to(SAMPLES.parents[1]).as_posix()
    except ValueError:
        return p.as_posix()


# --------------------------------------------------------------------------- per dataset


def ptb_xl_long(samples: Path) -> pd.DataFrame:
    db = read_text_csv(samples / "ptb_xl" / "ptbxl_database.csv")
    return explode_codes(db)


def inv_ptb_xl(samples: Path) -> pd.DataFrame:
    root = samples / "ptb_xl"
    st = load_statements(root / "scp_statements.csv")
    long = ptb_xl_long(samples)
    g = long.groupby("code")
    n_ecg, n_pat = g["ecg_id"].nunique(), g["patient_id"].nunique()
    n100 = long[long["likelihood"] == 100].groupby("code")["ecg_id"].nunique()
    recs = []
    for code in sorted(set(st.index) | set(long["code"])):
        s = st.loc[code] if code in st.index else None
        kinds = [k for k in ("diagnostic", "form", "rhythm") if s is not None and s.get(k) == 1]
        recs.append({
            "label_kind": "SCP statement (" + "/".join(kinds) + ")" if kinds else "SCP statement",
            "label_as_written": s["description"] if s is not None else "not in scp_statements.csv",
            "code": code, "code_system": "SCP-ECG (PTB-XL scp_statements.csv)",
            "count": int(n_ecg.get(code, 0)), "count_type": "records (ECGs with the code at any likelihood)",
            "n_patients": int(n_pat.get(code, 0)),
            "extra_count": int(n100.get(code, 0)), "extra_count_type": "records at likelihood 100",
            "extra": "" if s is None else (f"diagnostic_class={s.get('diagnostic_class', '')}; "
                                           f"diagnostic_subclass={s.get('diagnostic_subclass', '')}"),
            "source_file": "data/samples/ptb_xl/ptbxl_database.csv (scp_codes); scp_statements.csv"})
    return _rows("ptb_xl", recs)


def sph_long(samples: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    meta = read_text_csv(samples / "sph" / "metadata.csv", dtype=str)
    names = read_text_csv(samples / "sph" / "code.csv", dtype=str)
    names["Code"] = names["Code"].str.strip()
    return explode_statements(meta, "ECG_ID", "AHA_Code", "Patient_ID"), names


def inv_sph(samples: Path) -> pd.DataFrame:
    long, names = sph_long(samples)
    desc = dict(zip(names["Code"], names["Description"]))
    cat = dict(zip(names["Code"], names["Category"]))
    prim = long.drop_duplicates(["ecg", "code"]).groupby("code")
    recs = []
    for code in sorted(set(names.loc[names["Category"] != "Modifier", "Code"]) | set(long["code"]),
                       key=lambda c: int(c) if c.isdigit() else 10**9):
        has = code in prim.groups
        recs.append({"label_kind": "AHA primary statement", "label_as_written": desc.get(code, "not in code.csv"),
                     "code": code, "code_system": "AHA statement code (SPH code.csv)",
                     "count": prim.get_group(code)["ecg"].nunique() if has else 0, "count_type": "records",
                     "n_patients": prim.get_group(code)["patient"].nunique() if has else 0,
                     "extra": f"category={cat.get(code, '')}",
                     "source_file": "data/samples/sph/metadata.csv (AHA_Code); code.csv"})
    pairs = long[long["modifier"] != ""].groupby(["code", "modifier"])
    for (code, mod), grp in pairs:
        recs.append({"label_kind": "AHA statement + modifier",
                     "label_as_written": f"{desc.get(code, '?')} + {desc.get(mod, '?')}",
                     "code": f"{code}+{mod}", "code_system": "AHA statement code (SPH code.csv)",
                     "count": grp["ecg"].nunique(), "count_type": "records",
                     "n_patients": grp["patient"].nunique(), "extra": f"category={cat.get(code, '')}",
                     "source_file": "data/samples/sph/metadata.csv (AHA_Code); code.csv"})
    return _rows("sph", recs)


CODE15_LABELS = {"1dAVb": "first degree AV block", "RBBB": "right bundle branch block",
                 "LBBB": "left bundle branch block", "SB": "sinus bradycardia",
                 "AF": "atrial fibrillation", "ST": "sinus tachycardia (NOT ST elevation)",
                 "normal_ecg": "normal ECG per automatic annotation system"}


def code15_frame(samples: Path) -> pd.DataFrame:
    return read_text_csv(samples / "code15" / "exams.csv")


def _true(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.lower().isin({"true", "1"})


def inv_code15(samples: Path) -> pd.DataFrame:
    df = code15_frame(samples)
    recs = []
    for col, meaning in CODE15_LABELS.items():
        m = _true(df[col])
        recs.append({"label_kind": "boolean label column", "label_as_written": col, "code": col,
                     "code_system": "CODE-15% exams.csv column", "count": int(m.sum()),
                     "count_type": "records (exams)", "n_patients": int(df.loc[m, "patient_id"].nunique()),
                     "extra": f"meaning per https://zenodo.org/records/4916206: {meaning}",
                     "source_file": "data/samples/code15/exams.csv"})
    return _rows("code15", recs)


def challenge_g1(samples: Path, ds: str) -> pd.DataFrame:
    """One row per (record, SNOMED code) in the g1 headers."""
    root = samples / ds
    files = sorted((root / "training" / FOLDERS[ds]).glob("g*/*.hea"))
    hdr = read_headers(files, root)
    long = hdr[["record_name", "dx"]].assign(code=hdr["dx"].fillna("").str.split(",")).explode("code")
    long["code"] = long["code"].str.strip()
    return long[long["code"] != ""].drop_duplicates(["record_name", "code"])


def dx_mapping(maps: Path) -> pd.DataFrame:
    parts = []
    for f in ("dx_mapping_scored.csv", "dx_mapping_unscored.csv"):
        m = read_text_csv(maps / f, dtype={"SNOMEDCTCode": str})
        parts.append(m.assign(map_file=f))
    return pd.concat(parts, ignore_index=True)


def inv_challenge(samples: Path, ds: str) -> pd.DataFrame:
    maps = samples / "challenge_label_maps"
    dm = dx_mapping(maps)
    alt = load_maps(maps).set_index("code")["alt_name"]
    g1 = challenge_g1(samples, ds).groupby("code")["record_name"].nunique()
    col = MAP_COUNT_COLUMNS[ds]
    recs = []
    for r in dm.itertuples(index=False):
        code = str(r.SNOMEDCTCode)
        note = getattr(r, "Notes", "")
        recs.append({"label_kind": f"SNOMED CT code ({r.map_file})", "label_as_written": r.Dx,
                     "code": code, "code_system": "SNOMED CT (Challenge 2021 dx_mapping)",
                     "count": int(getattr(r, col)), "count_type": "publisher's count as listed",
                     "extra_count": int(g1.get(code, 0)), "extra_count_type": "sample (g1, 999)",
                     "extra": "; ".join(x for x in (f"abbreviation={r.Abbreviation}",
                                                    f"alt_name={alt.get(code, '')}" if alt.get(code, "") else "",
                                                    f"notes={note}" if isinstance(note, str) and note else "")
                                        if x),
                     "source_file": f"data/samples/challenge_label_maps/{r.map_file} (column {col}); "
                                    f"g1 headers data/samples/{ds}/training/{FOLDERS[ds]}/g1/*.hea"})
    for code in sorted(set(g1.index) - set(dm["SNOMEDCTCode"].astype(str))):
        recs.append({"label_kind": "SNOMED CT code (g1 only, not in dx_mapping)",
                     "label_as_written": alt.get(code, "unmapped"), "code": code,
                     "code_system": "SNOMED CT", "count": "not listed in dx_mapping",
                     "count_type": "publisher's count as listed", "extra_count": int(g1[code]),
                     "extra_count_type": "sample (g1, 999)",
                     "source_file": f"g1 headers data/samples/{ds}/training/{FOLDERS[ds]}/g1/*.hea"})
    return _rows(ds, recs)


PTBDB_KEYS = ("Reason for admission", "Acute infarction (localization)", "Former infarction (localization)")


def ptbdb_frame(samples: Path) -> pd.DataFrame:
    return record_table(samples / "ptb_diagnostic")


def inv_ptb_diagnostic(samples: Path) -> pd.DataFrame:
    rec = ptbdb_frame(samples)
    recs = []
    for key in PTBDB_KEYS:
        vals = rec[f"c:{key}"].fillna(KEY_MISSING) if f"c:{key}" in rec else pd.Series(KEY_MISSING, index=rec.index)
        for v, grp in rec.assign(v=vals).groupby("v"):
            recs.append({"label_kind": f"header comment: {key}", "label_as_written": v, "code": "",
                         "code_system": "free text (PTB-DB .hea comments)", "count": len(grp),
                         "count_type": "records", "n_patients": grp["patient"].nunique(),
                         "source_file": "data/samples/ptb_diagnostic/patient*/*.hea"})
    return _rows("ptb_diagnostic", recs)


def incart_patients(samples: Path) -> pd.DataFrame:
    """patient, records (list), diagnosis text from files-patients-diagnoses.txt."""
    lines = [ln.rstrip("\r") for ln in (samples / "incart" / "files-patients-diagnoses.txt").read_text().splitlines()]
    out = []
    for i, ln in enumerate(lines):
        m = re.fullmatch(r"\s*patient\s+(\d+)\s*", ln, flags=re.I)
        if m:
            recs = lines[i + 1].split() if i + 1 < len(lines) else []
            dx = lines[i + 2].strip() if i + 2 < len(lines) else ""
            if re.fullmatch(r"\s*patient\s+\d+\s*", dx, flags=re.I):
                dx = ""
            out.append({"patient": int(m[1]), "records": recs, "dx": dx})
    return pd.DataFrame(out)


def incart_record_terms(samples: Path) -> pd.DataFrame:
    """record, term from record-descriptions.txt (terms split on ',' and ';')."""
    lines = [ln.rstrip("\r").strip() for ln in (samples / "incart" / "record-descriptions.txt").read_text().splitlines()]
    out, cur = [], None
    for ln in lines:
        if re.fullmatch(r"I\d{2}", ln):
            cur = ln
        elif cur and ln:
            out += [{"record": cur, "term": t.strip()} for t in re.split(r"[,;]", ln) if t.strip()]
    return pd.DataFrame(out).drop_duplicates()


def inv_incart(samples: Path) -> pd.DataFrame:
    pts = incart_patients(samples)
    recs = []
    raw = pts.assign(dx=pts["dx"].replace("", "(no diagnosis text)"))
    for dx, grp in raw.groupby("dx"):
        recs.append({"label_kind": "patient diagnosis (raw text)", "label_as_written": dx, "code": "",
                     "code_system": "free text", "count": int(grp["records"].map(len).sum()),
                     "count_type": "records", "n_patients": len(grp),
                     "source_file": "data/samples/incart/files-patients-diagnoses.txt"})
    terms = pts[pts["dx"].str.contains(",")].assign(term=lambda d: d["dx"].str.split(",")).explode("term")
    terms["term"] = terms["term"].str.strip()
    for t, grp in terms.groupby("term"):
        recs.append({"label_kind": "patient diagnosis term (raw text split on commas)",
                     "label_as_written": t, "code": "", "code_system": "free text",
                     "count": int(grp["records"].map(len).sum()), "count_type": "records",
                     "n_patients": len(grp), "source_file": "data/samples/incart/files-patients-diagnoses.txt"})
    rt = incart_record_terms(samples)
    for t, grp in rt.groupby("term"):
        recs.append({"label_kind": "record description term", "label_as_written": t, "code": "",
                     "code_system": "free text", "count": grp["record"].nunique(), "count_type": "records",
                     "source_file": "data/samples/incart/record-descriptions.txt"})
    return _rows("incart", recs)


def inv_mimic(samples: Path) -> pd.DataFrame:
    return _rows("mimic_iv_ecg", [{
        "label_kind": "machine report statements", "label_as_written": "not checked: label file not downloaded",
        "count": "not checked", "count_type": "not checked",
        "extra": "machine_measurements.csv (report_0..report_17) not approved for download; "
                 "ICD diagnoses need credentialed access (U1 script)",
        "source_file": "none"}])


BUILDERS = {"ptb_xl": inv_ptb_xl, "mimic_iv_ecg": inv_mimic, "ptb_diagnostic": inv_ptb_diagnostic,
            "sph": inv_sph, **{ds: (lambda s, ds=ds: inv_challenge(s, ds)) for ds in CHALLENGE_IDS},
            "code15": inv_code15, "incart": inv_incart}


def build_inventory(samples: Path = SAMPLES, out_dir: Path = RESULTS_DIR) -> dict[str, pd.DataFrame]:
    out_dir.mkdir(parents=True, exist_ok=True)
    invs = {}
    for ds, fn in BUILDERS.items():
        df = fn(samples)
        df.to_csv(out_dir / f"label_inventory_{ds}.csv", index=False)
        invs[ds] = df
    summ = []
    for ds, df in invs.items():
        for kind, grp in df.groupby("label_kind", sort=False):
            cnt = pd.to_numeric(grp["count"], errors="coerce")
            summ.append({"dataset_id": ds, "label_kind": kind, "distinct_labels": len(grp),
                         "labels_with_count_gt_0": int((cnt > 0).sum()) if cnt.notna().any() else "not checked",
                         "count_type": "; ".join(sorted(set(grp["count_type"].astype(str)))),
                         "extra_count_type": "; ".join(sorted(set(grp["extra_count_type"].dropna().astype(str))))
                         or "-"})
    text = ["# Label inventory summary (local observation of the downloaded files)", "",
            "- Script: `src/stemi/review/label_inventory.py`; one CSV per dataset: "
            "`results/label_inventory_<dataset>.csv`.",
            "- Labels are listed as written; nothing is mapped or converted here (L1, L2).",
            "- Challenge sources: `count` = publisher's count as listed in dx_mapping (meaning not "
            "defined by the publisher); `extra_count` = g1 sample (999 headers).", "",
            md_table(pd.DataFrame(summ)), ""]
    (out_dir / "label_inventory_summary.md").write_text("\n".join(text))
    return invs


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--samples", type=Path, default=SAMPLES)
    ap.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    args = ap.parse_args(argv)
    for ds, df in build_inventory(args.samples, args.out_dir).items():
        print(f"{ds}: {len(df)} rows")


if __name__ == "__main__":
    main()
