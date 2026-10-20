"""Aggregate MI ICD counts for MIMIC-IV-ECG, for the USER to run on their own credentialed files (U1).

The team never runs this on real data and never sees the input files.
- Read-only. Paths come only from the command line. No network, pandas only.
- Prints aggregate counts only: no subject_id, hadm_id, study_id, dates or rows.
- Every count below 10 prints as "<10".
- Back-calculation: the only exact sum is "ECGs total = linked + not linked".
  Bucket totals are NOT the sum of their sub-code rows, because one admission can
  carry several codes. Even so, each family (one row plus the rows under it) gets
  secondary suppression: if exactly one row is hidden while the total is shown,
  the next-smallest row is hidden too. No subtotal rows are added beyond these.
- Writes nothing, except an optional aggregate CSV (--out, new file only).

    python -I src/stemi/review/mimic_icd_count.py \
        --diagnoses /path/to/hosp/diagnoses_icd.csv.gz \
        --admissions /path/to/hosp/admissions.csv.gz \
        --records /path/to/mimic-iv-ecg/record_list.csv \
        [--versions "MIMIC-IV x.y; MIMIC-IV-ECG 1.0"] [--out counts.csv]

Codes are matched exactly as stored (no dot) together with icd_version. The
script reports code groups only; it does NOT map them to STEMI / NSTEMI. A
proposed mapping is printed separately as an ASSUMPTION for the supervisor.
The optional MIMIC-IV-ECG-ext-ICD input is not supported: its file names and
value format were not confirmed from its documentation.
"""

from __future__ import annotations

if __package__ in (None, ""):          # run as a file under ``python -I``
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import argparse
from pathlib import Path

import pandas as pd

SUPPRESS_BELOW = 10
SUPPRESSED = "<10"
CHUNK_ROWS = 500_000
METRICS = ["admissions", "patients_with_admission", "admissions_with_linked_ecg",
           "ecgs_linked", "patients_with_linked_ecg"]

CAVEATS = [
    "ASSUMPTION (linkage): an ECG is linked to an admission when subject_id matches and "
    "admittime <= ecg_time <= dischtime.",
    "MIMIC-IV-ECG page (https://physionet.org/content/mimic-iv-ecg/1.0/): \"the ECG time stamps "
    "could be significantly out of sync with the corresponding time stamps\" in other MIMIC-IV "
    "modules, so linked counts are approximate.",
    "Diagnoses are hospital discharge billing codes; they do not show whether the MI was present "
    "or acute at the time of the ECG.",
    "The STEMI/NSTEMI group labels are an ASSUMPTION for clinical-supervisor review.",
    f"Counts below {SUPPRESS_BELOW} print as {SUPPRESSED}; some larger cells are also hidden "
    "(secondary suppression) so that hidden cells cannot be back-calculated.",
]
MAPPING_ASSUMPTION = [
    "ASSUMPTION for the supervisor (not applied by this script): I21.0-I21.3 (I210*-I213*) ~ "
    "STEMI; I21.4 (I214*) ~ NSTEMI; other I21 (e.g. I219, I21A*) ~ MI of other or unspecified "
    "type; I22* = subsequent MI; ICD-9 410.x does not cleanly separate STEMI and NSTEMI. "
    "Verify every code against ICD-10-CM / ICD-9-CM before use.",
]


# --------------------------------------------------------------------------- buckets


def bucket_of(code: str, version: int) -> tuple[str, str] | None:
    """(bucket, sub-code) for a dot-less code, or None if not an MI code of interest."""
    if version == 10 and code.startswith("I21"):
        if code[3:4] in ("0", "1", "2", "3"):
            return "ICD-10 I21.0-I21.3 (I210*-I213*)", code[:4]
        if code[3:4] == "4":
            return "ICD-10 I21.4 (I214*)", code[:4]
        return "ICD-10 other I21 (not I210-I214)", code
    if version == 10 and code.startswith("I22"):
        return "ICD-10 I22*", code
    if version == 9 and code.startswith("410"):
        return "ICD-9 410*", code[:4]
    return None


BUCKET_ORDER = ["ICD-10 I21.0-I21.3 (I210*-I213*)", "ICD-10 I21.4 (I214*)",
                "ICD-10 other I21 (not I210-I214)", "ICD-10 I22*", "ICD-9 410*"]
BOTH = "ICD-10 I210*-I213* AND I214* in the same admission"


# --------------------------------------------------------------------------- suppression


def _hide(n) -> bool:
    return n < SUPPRESS_BELOW


def suppress_family(parent: int, children: list[int]) -> tuple[str, list[str]]:
    """Primary (<10) plus secondary suppression for parent = f(children).

    If exactly one child is hidden while the parent is shown, the next-smallest
    visible child is hidden too. Children need not sum exactly to the parent (one
    admission can carry several codes); the rule is applied conservatively anyway.
    """
    hidden = [_hide(c) for c in children]
    parent_hidden = _hide(parent)
    if not parent_hidden and sum(hidden) == 1 and len(children) > 1:
        visible = [i for i, h in enumerate(hidden) if not h]
        hidden[min(visible, key=lambda i: children[i])] = True
    fmt = lambda n, h: SUPPRESSED if h else str(int(n))
    return fmt(parent, parent_hidden), [fmt(c, h) for c, h in zip(children, hidden)]


# --------------------------------------------------------------------------- reading


def read_diagnoses(path: Path) -> tuple[pd.DataFrame, int]:
    """Only MI-code rows are kept; returns (rows, total rows read)."""
    keep, total = [], 0
    for chunk in pd.read_csv(path, usecols=["subject_id", "hadm_id", "seq_num", "icd_code",
                                            "icd_version"], dtype={"icd_code": str},
                             chunksize=CHUNK_ROWS):
        total += len(chunk)
        code = chunk["icd_code"].astype(str).str.strip().str.upper()
        ver = pd.to_numeric(chunk["icd_version"], errors="coerce")
        m = (((ver == 10) & code.str.match(r"I2[12]")) | ((ver == 9) & code.str.match(r"410")))
        if m.any():
            keep.append(chunk.loc[m].assign(icd_code=code[m], icd_version=ver[m].astype(int)))
    cols = ["subject_id", "hadm_id", "seq_num", "icd_code", "icd_version"]
    return (pd.concat(keep, ignore_index=True) if keep else pd.DataFrame(columns=cols)), total


def read_chunked(path: Path, usecols: list[str], dates: list[str]) -> pd.DataFrame:
    parts = [c for c in pd.read_csv(path, usecols=usecols, parse_dates=dates,
                                    chunksize=CHUNK_ROWS)]
    return pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=usecols)


def tag(dx: pd.DataFrame) -> pd.DataFrame:
    b = [bucket_of(c, v) for c, v in zip(dx["icd_code"], dx["icd_version"])]
    dx = dx.assign(bucket=[x[0] if x else None for x in b], sub=[x[1] if x else None for x in b])
    return dx[dx["bucket"].notna()]


def link_ecgs(rec: pd.DataFrame, adm: pd.DataFrame) -> pd.DataFrame:
    m = rec.merge(adm, on="subject_id", how="inner")
    m = m[(m["admittime"] <= m["ecg_time"]) & (m["ecg_time"] <= m["dischtime"])]
    return m[["subject_id", "study_id", "hadm_id"]].drop_duplicates()


# --------------------------------------------------------------------------- counting


def _metrics(rows: pd.DataFrame, linked: pd.DataFrame) -> dict[str, int]:
    hadm = set(rows["hadm_id"])
    ecg = linked[linked["hadm_id"].isin(hadm)]
    return {"admissions": len(hadm), "patients_with_admission": rows["subject_id"].nunique(),
            "admissions_with_linked_ecg": ecg["hadm_id"].nunique(),
            "ecgs_linked": ecg["study_id"].nunique(),
            "patients_with_linked_ecg": ecg["subject_id"].nunique()}


def code_table(tagged: pd.DataFrame, linked: pd.DataFrame) -> pd.DataFrame:
    """Raw counts: one parent row per bucket x position, then its sub-code rows."""
    rows = []
    seq1 = pd.to_numeric(tagged["seq_num"], errors="coerce") == 1
    for position, pos_mask in (("any position", pd.Series(True, index=tagged.index)),
                               ("seq_num == 1", seq1)):
        t = tagged[pos_mask]
        for bucket in BUCKET_ORDER:
            tb = t[t["bucket"] == bucket]
            rows.append({"family": f"{bucket} | {position}", "level": "bucket", "group": bucket,
                         "position": position, **_metrics(tb, linked)})
            subs = sorted(tb["sub"].unique())
            if len(subs) > 1:
                for s in subs:
                    rows.append({"family": f"{bucket} | {position}", "level": "sub-code",
                                 "group": s, "position": position,
                                 **_metrics(tb[tb["sub"] == s], linked)})
    a = tagged[tagged["bucket"] == BUCKET_ORDER[0]]
    b = tagged[tagged["bucket"] == BUCKET_ORDER[1]]
    both = set(a["hadm_id"]) & set(b["hadm_id"])
    rows.append({"family": BOTH, "level": "bucket", "group": BOTH, "position": "any position",
                 **_metrics(tagged[tagged["hadm_id"].isin(both)], linked)})
    return pd.DataFrame(rows)


def apply_suppression(raw: pd.DataFrame) -> pd.DataFrame:
    out = raw.astype({m: object for m in METRICS}).copy()
    for _, fam in raw.groupby("family", sort=False):
        parent_idx = fam.index[fam["level"] == "bucket"][0]
        child_idx = list(fam.index[fam["level"] == "sub-code"])
        for m in METRICS:
            p, cs = suppress_family(raw.at[parent_idx, m], [raw.at[i, m] for i in child_idx])
            out.at[parent_idx, m] = p
            for i, c in zip(child_idx, cs):
                out.at[i, m] = c
    return out.drop(columns=["family"])


def ecg_context(rec: pd.DataFrame, linked: pd.DataFrame, adm: pd.DataFrame) -> pd.DataFrame:
    total = rec["study_id"].nunique()
    n_linked = linked["study_id"].nunique()
    p, (a, b) = suppress_family(total, [n_linked, total - n_linked])
    adm_p = SUPPRESSED if _hide(adm["hadm_id"].nunique()) else str(adm["hadm_id"].nunique())
    return pd.DataFrame({"item": ["ECGs total (record_list)", "ECGs linked to any admission",
                                  "ECGs not linked (outside every admit-discharge window)",
                                  "admissions total (admissions file)"],
                         "count": [p, a, b, adm_p]})


def run(diagnoses: Path, admissions: Path, records: Path) -> dict:
    dx, n_dx = read_diagnoses(diagnoses)
    adm = read_chunked(admissions, ["subject_id", "hadm_id", "admittime", "dischtime"],
                       ["admittime", "dischtime"])
    rec = read_chunked(records, ["subject_id", "study_id", "ecg_time"], ["ecg_time"])
    linked = link_ecgs(rec, adm)
    raw = code_table(tag(dx), linked)
    inputs = pd.DataFrame({"file": [diagnoses.name, admissions.name, records.name],
                           "rows_read": [n_dx, len(adm), len(rec)]})
    return {"inputs": inputs, "context": ecg_context(rec, linked, adm),
            "codes": apply_suppression(raw), "_raw": raw}


def main(argv: list[str] | None = None) -> dict:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--diagnoses", type=Path, required=True, help="hosp/diagnoses_icd.csv(.gz)")
    ap.add_argument("--admissions", type=Path, required=True, help="hosp/admissions.csv(.gz)")
    ap.add_argument("--records", type=Path, required=True, help="mimic-iv-ecg record_list.csv")
    ap.add_argument("--versions", default="not given",
                    help="e.g. 'MIMIC-IV 3.1; MIMIC-IV-ECG 1.0' (echoed in the output)")
    ap.add_argument("--out", type=Path, default=None, help="optional aggregate CSV (new file only)")
    args = ap.parse_args(argv)
    if args.out is not None and args.out.exists():
        raise SystemExit(f"{args.out} exists; choose a new file name (nothing is overwritten)")
    res = run(args.diagnoses, args.admissions, args.records)

    print(f"Versions (as given by the user): {args.versions}")
    print("Inputs (file name, rows read; inputs are file rows, not counts of people):")
    print(res["inputs"].to_string(index=False))
    for c in CAVEATS + MAPPING_ASSUMPTION:
        print(f"- {c}")
    print("\nECG linkage context:")
    print(res["context"].to_string(index=False))
    print("\nMI code groups (no STEMI/NSTEMI mapping applied):")
    print(res["codes"].to_string(index=False))
    if args.out is not None:
        table = pd.concat([
            res["context"].rename(columns={"item": "group"}).assign(level="context", position="-"),
            res["codes"]], ignore_index=True)[["level", "group", "position", "count"] + METRICS]
        with open(args.out, "x", newline="") as f:
            f.write(f"# versions: {args.versions}\n")
            for c in CAVEATS + MAPPING_ASSUMPTION:
                f.write(f"# {c}\n")
            table.to_csv(f, index=False)
    res.pop("_raw")
    return res


if __name__ == "__main__":
    main()
