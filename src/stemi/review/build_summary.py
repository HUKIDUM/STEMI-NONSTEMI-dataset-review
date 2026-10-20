"""One row per dataset from the result files in results/ (step S10).

    .venv/bin/python -I src/stemi/review/build_summary.py

Every cell is computed from a results/ file or a downloaded metadata file in
data/samples/ (named in `source_files`); a value that
was not observed locally is "not observed" (the verified desk facts live in
results/verified_facts.md, not here). Challenge rows mix the g1 header sample (fs, leads,
duration) with the publisher's dx_mapping counts (MI codes); `scope` says which.
Output: results/dataset_summary.csv
"""

from __future__ import annotations

if __package__ in (None, ""):          # run as a file under ``python -I``
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import argparse
from pathlib import Path

import pandas as pd

from stemi.review.common import RESULTS_DIR, read_text_csv

SAMPLES = Path(__file__).resolve().parents[3] / "data" / "samples"

NA = "not observed"
COLUMNS = ["dataset_id", "scope", "ecgs", "patients", "fs_hz", "n_leads", "duration_s",
           "mi_related_ecgs", "mi_detail", "acute_or_timing_info", "stemi_nstemi_label",
           "source_files"]
CHALLENGE = {"cpsc_2018": "CPSC", "cpsc_extra": "CPSC_Extra", "georgia": "Georgia",
             "chapman_shaoxing": "Chapman_Shaoxing", "ningbo": "Ningbo"}


def _read(r: Path, name: str) -> pd.DataFrame | None:
    p = r / name
    return read_text_csv(p) if p.exists() else None


def _range(s: pd.Series) -> str:
    s = pd.to_numeric(s, errors="coerce").dropna()
    return NA if s.empty else (f"{s.min():g}" if s.min() == s.max() else f"{s.min():g}–{s.max():g}")


def _hdr(h: pd.DataFrame | None) -> dict:
    if h is None or h.empty:
        return {"fs_hz": NA, "n_leads": NA, "duration_s": NA}
    return {"fs_hz": _range(h["fs"]), "n_leads": _range(h["n_sig"]), "duration_s": _range(h["duration_s"])}


def _csv(path: Path, cols: list[str]) -> pd.DataFrame | None:
    return pd.read_csv(path, usecols=cols) if path.exists() else None


def ptb_xl(r: Path, samples: Path = SAMPLES) -> dict:
    c, st, h = _read(r, "ptb_xl_scp_counts.csv"), _read(r, "ptb_xl_mi_early_stadium.csv"), _read(r, "ptb_xl_headers.csv")
    row = {"dataset_id": "ptb_xl", "scope": "full metadata CSV; 20 seeded headers", **_hdr(h),
           "stemi_nstemi_label": "none (no STEMI/NSTEMI SCP statement)",
           "source_files": "ptb_xl_scp_counts.csv; ptb_xl_mi_early_stadium.csv; ptb_xl_headers.csv; "
                           "data/samples/ptb_xl/ptbxl_database.csv"}
    db = _csv(samples / "ptb_xl" / "ptbxl_database.csv", ["ecg_id", "patient_id"])
    if db is not None:
        row["ecgs"], row["patients"] = db["ecg_id"].nunique(), db["patient_id"].nunique()
    if st is not None:
        s = st.set_index("selection")
        row["mi_related_ecgs"] = int(s.loc["any listed MI/injury code", "n_ecgs"])
        early = [k for k in s.index if k.startswith("any listed code AND stadium1")][0]
        row["acute_or_timing_info"] = (f"infarction_stadium; MI code + Stadium I/I-II: "
                                       f"{s.loc[early, 'n_ecgs']} ECGs / {s.loc[early, 'n_patients']} patients")
    if c is not None:
        mi = c[c["diag_class_MI"]]
        row["mi_detail"] = f"{len(mi)} SCP codes with diagnostic_class MI"
    return row


def ptb_diagnostic(r: Path) -> dict:
    rec, t = _read(r, "ptb_diagnostic_records.csv"), _read(r, "ptb_diagnostic_mi_patient_timing.csv")
    row = {"dataset_id": "ptb_diagnostic", "scope": "all 549 headers", **_hdr(rec),
           "stemi_nstemi_label": "none",
           "source_files": "ptb_diagnostic_records.csv; ptb_diagnostic_mi_patient_timing.csv"}
    if rec is not None:
        row["ecgs"], row["patients"] = len(rec), rec["patient"].nunique()
        mi = rec[rec["c:Reason for admission"].astype(str).str.contains("infarct", case=False)]
        row["mi_related_ecgs"] = len(mi)
        row["mi_detail"] = f"reason for admission MI: {len(mi)} records / {mi['patient'].nunique()} patients"
    if t is not None:
        d = t.set_index("earliest_ecg_days_after_infarction")["n_patients"]
        row["acute_or_timing_info"] = f"infarction date vs ECG date; earliest ECG 0–1 d: {d.get('0-1', NA)} patients"
    return row


def mimic(r: Path) -> dict:
    p, h = _read(r, "download_plausibility.csv"), _read(r, "mimic_iv_ecg_headers.csv")
    row = {"dataset_id": "mimic_iv_ecg", "scope": "record_list.csv; 50 seeded headers", **_hdr(h),
           "mi_related_ecgs": "not checked (machine_measurements.csv not downloaded; ICD credentialed)",
           "acute_or_timing_info": "not in open files",
           "stemi_nstemi_label": "only via credentialed ICD-10 linkage (U1 script, not run)",
           "source_files": "download_plausibility.csv; mimic_iv_ecg_headers.csv"}
    if p is not None:
        q = p[p["dataset_id"] == "mimic_iv_ecg"].iloc[-1]
        row["ecgs"], row["patients"] = int(q["distinct_study_id"]), int(q["distinct_subject_id"])
    return row


def sph(r: Path, samples: Path = SAMPLES) -> dict:
    t = _read(r, "sph_mi_timing.csv")
    row = {"dataset_id": "sph", "scope": "metadata.csv + code.csv", "fs_hz": NA, "n_leads": NA,
           "duration_s": NA, "stemi_nstemi_label": "none",
           "source_files": "sph_mi_timing.csv; data/samples/sph/metadata.csv"}
    m = _csv(samples / "sph" / "metadata.csv", ["ECG_ID", "Patient_ID", "N"])
    if m is not None:
        row["ecgs"], row["patients"] = m["ECG_ID"].nunique(), m["Patient_ID"].nunique()
        row["duration_s"] = _range(m["N"] / 500) + " (N/500; 500 Hz per documentation)"
    if t is not None:
        s = t.set_index("selection")
        anymi = [k for k in s.index if k.startswith("any MI code")][0]
        row["mi_related_ecgs"] = int(s.loc[anymi, "n_ecgs"])
        row["mi_detail"] = f"AHA MI codes: {s.loc[anymi, 'n_ecgs']} ECGs / {s.loc[anymi, 'n_patients']} patients"
        acute = [k for k in s.index if "(Acute)" in k][0]
        row["acute_or_timing_info"] = f"modifier Acute: {s.loc[acute, 'n_ecgs']} ECGs"
    return row


def code15(r: Path, samples: Path = SAMPLES) -> dict:
    lab = _read(r, "code15_label_counts.csv")
    e = _csv(samples / "code15" / "exams.csv", ["exam_id", "patient_id"])
    counts = {} if e is None else {"ecgs": e["exam_id"].nunique(), "patients": e["patient_id"].nunique()}
    return {"dataset_id": "code15", **counts, "scope": "exams.csv", "fs_hz": NA, "n_leads": NA, "duration_s": NA,
            "mi_related_ecgs": 0 if lab is not None and not lab["name_matches_mi_regex"].any() else NA,
            "mi_detail": "no MI column (ST = sinus tachycardia)", "acute_or_timing_info": "none",
            "stemi_nstemi_label": "none",
            "source_files": "code15_label_counts.csv; data/samples/code15/exams.csv"}


def incart_diagnosis_records(path: Path) -> dict[str, int]:
    """files-patients-diagnoses.txt blocks: 'patient N' / record list / diagnosis text."""
    lines = path.read_text().splitlines()
    out: dict[str, int] = {}
    for i, ln in enumerate(lines):
        if ln.strip().lower().startswith("patient ") and i + 2 < len(lines):
            recs, dx = lines[i + 1].split(), lines[i + 2].strip()
            if dx and not dx.lower().startswith("patient "):
                out[dx] = out.get(dx, 0) + len(recs)
    return out


def incart(r: Path, samples: Path = SAMPLES) -> dict:
    h = _read(r, "incart_headers.csv")
    f = samples / "incart" / "files-patients-diagnoses.txt"
    pts = (sum(1 for ln in f.read_text().splitlines() if ln.strip().lower().startswith("patient "))
           if f.exists() else NA)
    dx = incart_diagnosis_records(f) if f.exists() else {}
    mi_rel = (f"{dx.get('Acute MI', 0)} records (Acute MI) + {dx.get('Earlier MI', 0)} (Earlier MI)"
              if dx else NA)
    return {"dataset_id": "incart", "scope": "all 75 headers + text files", **_hdr(h),
            "ecgs": len(h) if h is not None else NA, "patients": pts, "mi_related_ecgs": mi_rel,
            "mi_detail": "files-patients-diagnoses.txt: Acute MI 2 patients (6 records)",
            "acute_or_timing_info": "patient-level 'Acute MI' text", "stemi_nstemi_label": "none",
            "source_files": "incart_headers.csv; data/samples/incart/files-patients-diagnoses.txt"}


def challenge(r: Path, ds: str, pub: pd.DataFrame | None) -> dict:
    h = _read(r, f"challenge_{ds}_headers.csv")
    row = {"dataset_id": ds, "scope": "g1 header sample (fs/leads/duration); publisher dx_mapping (MI codes)",
           **_hdr(h), "acute_or_timing_info": "none observed", "stemi_nstemi_label": "none",
           "source_files": f"challenge_{ds}_headers.csv; challenge_dx_mapping_counts.csv"}
    if pub is not None and CHALLENGE[ds] in pub.columns:
        mi = pub[pub["kw_infarct"].astype(bool)]
        col = CHALLENGE[ds]
        g1 = _read(r, f"challenge_{ds}_dx_counts.csv")
        g1n = {} if g1 is None else dict(zip(g1["code"].astype(str), g1["n_records"]))
        timing = []
        for name in ("acute myocardial infarction", "old myocardial infarction"):
            hit = pub[pub["Dx"].str.lower() == name]
            if len(hit) and int(hit[col].iloc[0]):
                code = str(hit["SNOMEDCTCode"].iloc[0])
                timing.append(f"label '{name}' (publisher {int(hit[col].iloc[0]):,}; "
                              f"g1 {int(g1n.get(code, 0))})")
        if timing:
            row["acute_or_timing_info"] = "; ".join(timing) + "; no timing field"
        row["mi_detail"] = "; ".join(f"{d} {int(n)}" for d, n in zip(mi["Dx"], mi[col]) if n) or "no MI codes"
        row["mi_related_ecgs"] = "counts as listed, see mi_detail (publisher; may overlap)"
    return row


def build(r: Path = RESULTS_DIR, samples: Path = SAMPLES) -> pd.DataFrame:
    pub = _read(r, "challenge_dx_mapping_counts.csv")
    rows = [ptb_xl(r, samples), mimic(r), ptb_diagnostic(r), sph(r, samples)]
    rows += [challenge(r, ds, pub) for ds in CHALLENGE if (r / f"challenge_{ds}_headers.csv").exists()]
    rows += [code15(r, samples), incart(r, samples)]
    df = pd.DataFrame(rows).reindex(columns=COLUMNS)
    for c in ("ecgs", "patients"):
        df[c] = df[c].map(lambda v: str(int(v)) if isinstance(v, (int, float)) and pd.notna(v) else v)
    df = df.fillna(NA)
    df.to_csv(r / "dataset_summary.csv", index=False)
    return df


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--results", type=Path, default=RESULTS_DIR)
    args = ap.parse_args(argv)
    print(build(args.results).to_string(index=False))


if __name__ == "__main__":
    main()
