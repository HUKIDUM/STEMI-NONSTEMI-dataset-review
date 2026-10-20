"""Common-label crosswalk across the 11 datasets (task S12-L, part L2).

    .venv/bin/python -I src/stemi/review/label_crosswalk.py

TEAM MAPPING by meaning, not a publisher fact; needs supervisor review. Every code used
is listed per row in `mapping_note`; edit MAPPING to change a choice. Record-level unions
are used where record-level data exist (PTB-XL, SPH, CODE-15, PTB-DB, INCART, Challenge
g1); the Challenge publisher counts are per code, so several codes are summed (may
double-count).

Cell vocabulary: a number | "0 (listed, count 0)" | "not present" | "not checked".
Output: results/label_crosswalk_common.csv (with "#" header lines).
"""

from __future__ import annotations

if __package__ in (None, ""):          # run as a file under ``python -I``
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import argparse
from pathlib import Path

import pandas as pd

from stemi.review.common import RESULTS_DIR
from stemi.review.label_inventory import (
    CHALLENGE_IDS, KEY_MISSING, SAMPLES, _true, challenge_g1, code15_frame, dx_mapping,
    incart_patients, incart_record_terms, ptb_xl_long, ptbdb_frame, sph_long,
)
from stemi.review.review_challenge import MAP_COUNT_COLUMNS
from stemi.review.review_ptbxl import load_statements

LISTED_ZERO = "0 (listed, count 0)"
NOT_PRESENT = "not present"
NOT_CHECKED = "not checked"
DATASETS = ["ptb_xl", "mimic_iv_ecg", "ptb_diagnostic", "sph", *CHALLENGE_IDS, "code15", "incart"]
COUNT_TYPE = {
    "ptb_xl": "records (ECGs; union of codes at any likelihood)",
    "mimic_iv_ecg": "not checked (label file not downloaded)",
    "ptb_diagnostic": "records (union)",
    "sph": "records (ECGs; union)",
    **{ds: "publisher's count as listed (sum of codes; may double-count when >1 code)"
       for ds in CHALLENGE_IDS},
    "code15": "records (exams; union)",
    "incart": "records (union)",
}
HEADER = "Team mapping by meaning, not a publisher fact; needs supervisor review"

PTBXL_MI = ["IMI", "ASMI", "ILMI", "AMI", "ALMI", "INJAS", "LMI", "INJAL", "IPLMI", "IPMI",
            "INJIN", "INJLA", "PMI", "INJIL"]
PTBDB_NOT_OLD = ["no", "n/a", "unknown", KEY_MISSING]

# label -> {"ptb_xl": [SCP], "sph": ["code" | "code+modifier"], "code15": [col],
#           "challenge": [SNOMED], "ptb_diagnostic": [(key, "in"|"not_in", values)],
#           "incart": [("dx" | "dx_term" | "rec" | "rec_contains", text)], "note": str}
MAPPING: dict[str, dict] = {
    "Normal ECG": {"ptb_xl": ["NORM"], "sph": ["1"], "code15": ["normal_ecg"], "challenge": [],
                   "note": "Challenge dx_mapping has no 'normal ECG' code (sinus rhythm is separate); "
                           "PTB-DB 'Healthy control' is a subject group, not mapped; CODE-15 normal_ecg "
                           "is from an automatic system"},
    "Sinus rhythm": {"ptb_xl": ["SR"], "challenge": ["426783006"],
                     "note": "SPH and CODE-15 have no sinus-rhythm label"},
    "Sinus bradycardia": {"ptb_xl": ["SBRAD"], "sph": ["22"], "code15": ["SB"], "challenge": ["426177001"],
                          "note": "Challenge 'bradycardia' 426627000 and INCART 'bradycardia' (not sinus-specific) not mapped"},
    "Sinus tachycardia": {"ptb_xl": ["STACH"], "sph": ["21"], "code15": ["ST"], "challenge": ["427084000"],
                          "note": "CODE-15 'ST' = sinus tachycardia; INCART 'tachycardia' not mapped"},
    "Atrial fibrillation": {"ptb_xl": ["AFIB"], "sph": ["50"], "code15": ["AF"], "challenge": ["164889003"],
                            "incart": [("rec", "atrial fibrillation")],
                            "note": "not mapped: Challenge 195080001 (AF and flutter), 282825002 paroxysmal AF, "
                                    "426749004 chronic AF, 314208002 rapid AF; INCART 'paroxysmal atrial fibrillation'"},
    "Atrial flutter": {"ptb_xl": ["AFLT"], "sph": ["51"], "challenge": ["164890007"],
                       "note": "Challenge 195080001 (AF and flutter) not mapped"},
    "1st-degree AV block": {"ptb_xl": ["1AVB"], "code15": ["1dAVb"], "challenge": ["270492004"],
                            "note": "'Prolonged PR interval' not mapped (PTB-XL LPR, Challenge 164947007, "
                                    "SPH 82): kept separate as the publishers do; SPH has no 1AVB label"},
    "LBBB": {"ptb_xl": ["CLBBB"], "sph": ["104"], "code15": ["LBBB"], "challenge": ["164909002", "733534002"],
             "note": "Challenge 164909002+733534002 scored as the same diagnosis (dx_mapping Notes); "
                     "ecg-arrhythmia ConditionNames maps LBBB, 'left back bundle branch block' and 'left front "
                     "bundle branch block' all to 164909002 (Chapman/Ningbo may include fascicular blocks); "
                     "incomplete LBBB (PTB-XL ILBBB, 251120003) not mapped"},
    "RBBB (complete)": {"ptb_xl": ["CRBBB"], "sph": ["106"], "code15": ["RBBB"],
                        "challenge": ["59118001", "713427006"], "incart": [("rec", "right bundle branch block")],
                        "note": "Challenge 59118001+713427006 scored as the same diagnosis; CODE-15 and "
                                "INCART say 'right bundle branch block' without 'complete'"},
    "RBBB (incomplete)": {"ptb_xl": ["IRBBB"], "sph": ["105"], "challenge": ["713426002"], "note": ""},
    "LAFB": {"ptb_xl": ["LAFB"], "sph": ["101"], "challenge": ["445118002"],
             "note": "see LBBB note: ConditionNames maps 'left front bundle branch block' to the LBBB code"},
    "PAC (atrial premature)": {"ptb_xl": ["PAC"], "sph": ["30"], "challenge": ["284470004", "63593006"],
                               "incart": [("rec", "APCs")],
                               "note": "Challenge PAC+SVPB scored as the same diagnosis; not mapped: SPH 31 "
                                       "(nonconducted), Challenge 251170000 blocked PAC, INCART 'blocked APCs', "
                                       "PTB-XL PRC(S)"},
    "PVC (ventricular premature)": {"ptb_xl": ["PVC"], "sph": ["60"], "challenge": ["427172004", "17338001"],
                                    "incart": [("rec_contains", "PVC")],
                                    "note": "Challenge PVC+VPB scored as the same diagnosis; Challenge 164884008 "
                                            "'ventricular ectopics' not mapped; INCART = any record term containing 'PVC'"},
    "LVH": {"ptb_xl": ["LVH"], "sph": ["142"], "challenge": ["164873001"],
            "incart": [("dx_term", "left ventricular hypertrophy")],
            "note": "not mapped: PTB-XL VCLVH (voltage criteria), Challenge 55827005 'left ventricular high "
                    "voltage', PTB-DB 'Hypertrophy' (side not stated); INCART is a patient-level diagnosis"},
    "Long QT": {"ptb_xl": ["LNGQT"], "sph": ["148"], "challenge": ["111975006"], "note": ""},
    "MI (any)": {"ptb_xl": PTBXL_MI, "sph": ["160", "161", "165", "166"],
                 "challenge": ["164865005", "57054005", "54329005", "164867002"],
                 "ptb_diagnostic": [("Reason for admission", "in", ["Myocardial infarction"])],
                 "incart": [("dx", "Acute MI"), ("dx", "Earlier MI")],
                 "note": "includes old/earlier MI; PTB-XL = all 14 diagnostic_class MI codes incl. 5 INJ* "
                         "'subendocardial injury'; ecg-arrhythmia ConditionNames maps MI, MIBW, MIFW, MILW "
                         "and MISW (MI by wall) all to 164865005 (Chapman/Ningbo); report statements, not "
                         "adjudicated (L2)"},
    "Old MI": {"sph": ["160+332", "161+332", "165+332", "166+332"], "challenge": ["164867002"],
               "ptb_diagnostic": [("Former infarction (localization)", "not_in", PTBDB_NOT_OLD)],
               "incart": [("dx", "Earlier MI")],
               "note": "PTB-XL has no 'old MI' statement; the infarction_stadium field (not a label) gives "
                       "MI-coded ECGs with Stadium III in either field: 963 ECGs / 923 patients; SPH = MI code + modifier 332 Old; PTB-DB = 'Former infarction "
                       "(localization)' other than no / n/a / unknown"},
    "ST elevation": {"ptb_xl": ["STE_"], "sph": ["145+363"], "challenge": ["164931005"],
                     "incart": [("rec", "ST elevation")],
                     "note": "PTB-XL STE_ is 'non-specific ST elevation' (mapped; flag for review); NST_ "
                             "'non-specific ST changes' not mapped; Challenge 164931005 came from Chapman's "
                             "'ST tilt up' (ConditionNames); SPH = 145 ST deviation + 363 Elevation"},
    "ST depression": {"ptb_xl": ["STD_"], "sph": ["145+362"], "challenge": ["429622005", "704997005"],
                      "incart": [("rec", "ST depression")],
                      "note": "PTB-XL STD_ is 'non-specific ST depression' (mapped; flag for review); "
                              "Challenge 429622005 came from Chapman's 'ST drop down'; 704997005 = inferior "
                              "ST segment depression"},
    "Ischaemia (any)": {"ptb_xl": ["ISC_", "ISCAL", "ISCIN", "ISCIL", "ISCAS", "ISCLA", "ISCAN"],
                        "challenge": ["164861001", "413444003", "413844008", "426434006", "425419005",
                                      "425623009"],
                        "note": "SPH has no ischaemia statement; INCART 'Transient ischemic attack (angina "
                                "pectoris)' is a patient diagnosis, not mapped"},
    "T-wave abnormality": {"ptb_xl": ["TAB_"], "sph": ["147"], "challenge": ["164934002"],
                           "note": "not mapped: PTB-XL NT_, INVT, LOWT, NDT; Challenge 59931005 T wave "
                                   "inversion; INCART 'negative T'"},
}


class Sources:
    """Loads every record-level table once."""

    def __init__(self, samples: Path = SAMPLES):
        self.ptbxl_long = ptb_xl_long(samples)
        self.ptbxl_codes = set(load_statements(samples / "ptb_xl" / "scp_statements.csv").index)
        self.sph_long, sph_names = sph_long(samples)
        self.sph_codes = set(sph_names["Code"])
        self.code15 = code15_frame(samples)
        self.dm = dx_mapping(samples / "challenge_label_maps")
        self.dm["SNOMEDCTCode"] = self.dm["SNOMEDCTCode"].astype(str)
        self.g1 = {ds: challenge_g1(samples, ds) for ds in CHALLENGE_IDS}
        self.ptbdb = ptbdb_frame(samples)
        self.incart_pts = incart_patients(samples)
        self.incart_terms = incart_record_terms(samples)


def _cell(n: int, listed: bool) -> str | int:
    if n > 0:
        return int(n)
    return LISTED_ZERO if listed else NOT_PRESENT


def cell_ptb_xl(s: Sources, codes: list[str]):
    if not codes:
        return NOT_PRESENT
    n = s.ptbxl_long.loc[s.ptbxl_long["code"].isin(codes), "ecg_id"].nunique()
    return _cell(n, any(c in s.ptbxl_codes for c in codes))


def cell_sph(s: Sources, codes: list[str]):
    if not codes:
        return NOT_PRESENT
    L = s.sph_long
    mask = pd.Series(False, index=L.index)
    for c in codes:
        code, _, mod = c.partition("+")
        mask |= (L["code"] == code) & ((L["modifier"] == mod) if mod else True)
    listed = all(part in s.sph_codes for c in codes for part in c.split("+"))
    return _cell(L.loc[mask, "ecg"].nunique(), listed)


def cell_code15(s: Sources, cols: list[str]):
    if not cols:
        return NOT_PRESENT
    return _cell(int(s.code15[cols].apply(_true).any(axis=1).sum()), True)


def cell_challenge(s: Sources, ds: str, codes: list[str]):
    if not codes:
        return NOT_PRESENT, NOT_PRESENT
    rows = s.dm[s.dm["SNOMEDCTCode"].isin(codes)].drop_duplicates("SNOMEDCTCode")
    listed = len(rows) > 0
    pub = _cell(int(rows[MAP_COUNT_COLUMNS[ds]].sum()), listed)
    g = s.g1[ds]
    return pub, _cell(g.loc[g["code"].isin(codes), "record_name"].nunique(), listed)


def cell_ptbdb(s: Sources, preds: list[tuple]):
    if not preds:
        return NOT_PRESENT
    rec, mask, listed = s.ptbdb, pd.Series(False, index=s.ptbdb.index), False
    for key, op, values in preds:
        col = rec[f"c:{key}"].fillna(KEY_MISSING)
        hit = col.isin(values) if op == "in" else ~col.isin(values)
        listed = listed or (bool(hit.any()) if op == "not_in" else bool(col.isin(values).any()))
        mask |= hit
    return _cell(int(mask.sum()), listed)


def cell_incart(s: Sources, preds: list[tuple]):
    if not preds:
        return NOT_PRESENT
    recs = set()
    for kind, text in preds:
        if kind in ("dx", "dx_term"):
            pts = s.incart_pts
            hit = (pts["dx"] == text) if kind == "dx" else pts["dx"].str.split(",").map(
                lambda xs: text in [x.strip() for x in xs])
            for r in pts.loc[hit, "records"]:
                recs |= set(r)
        else:
            t = s.incart_terms
            hit = (t["term"] == text) if kind == "rec" else t["term"].str.contains(text, regex=False)
            recs |= set(t.loc[hit, "record"])
    return _cell(len(recs), bool(recs))


def _note(label: str, m: dict) -> str:
    def fmt(v):
        if not v:
            return "—"
        if isinstance(v[0], tuple):
            return " | ".join(" ".join(str(x) if not isinstance(x, list) else "/".join(x) for x in p) for p in v)
        return "+".join(v)
    parts = [f"{k}: {fmt(m.get(k, []))}" for k in ("ptb_xl", "sph", "code15", "challenge",
                                                   "ptb_diagnostic", "incart")]
    multi = len(m.get("challenge", [])) > 1
    return ("; ".join(parts) + ("; Challenge: sum of codes (may double-count)" if multi else "")
            + (f"; NOTE: {m['note']}" if m.get("note") else ""))


def build(samples: Path = SAMPLES, out_dir: Path = RESULTS_DIR, sources: Sources | None = None) -> pd.DataFrame:
    s = sources or Sources(samples)
    rows = []
    for label, m in MAPPING.items():
        row = {"label": label, "ptb_xl": cell_ptb_xl(s, m.get("ptb_xl", [])),
               "mimic_iv_ecg": NOT_CHECKED,
               "ptb_diagnostic": cell_ptbdb(s, m.get("ptb_diagnostic", [])),
               "sph": cell_sph(s, m.get("sph", []))}
        for ds in CHALLENGE_IDS:
            row[ds], row[f"{ds}_g1"] = cell_challenge(s, ds, m.get("challenge", []))
        row["code15"] = cell_code15(s, m.get("code15", []))
        row["incart"] = cell_incart(s, m.get("incart", []))
        row["mapping_note"] = _note(label, m)
        rows.append(row)
    cols = ["label", *DATASETS[:4]]
    for ds in CHALLENGE_IDS:
        cols += [ds, f"{ds}_g1"]
    cols += ["code15", "incart", "mapping_note"]
    df = pd.DataFrame(rows)[cols]
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "label_crosswalk_common.csv", "w", newline="") as f:
        f.write(f"# {HEADER}\n")
        f.write("# Cell vocabulary: number | 0 (listed, count 0) | not present | not checked\n")
        for ds in DATASETS:
            f.write(f"# count type {ds}: {COUNT_TYPE[ds]}\n")
        f.write("# <challenge>_g1 columns: sample (g1, 999 headers), record-level union\n")
        f.write("# Script: src/stemi/review/label_crosswalk.py (MAPPING dict); "
                "inputs: data/samples/ (see results/label_inventory_*.csv)\n")
        df.to_csv(f, index=False)
    return df


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out-dir", type=Path, default=RESULTS_DIR)
    args = ap.parse_args(argv)
    df = build(out_dir=args.out_dir)
    print(df.drop(columns="mapping_note").to_string(index=False))


if __name__ == "__main__":
    main()
