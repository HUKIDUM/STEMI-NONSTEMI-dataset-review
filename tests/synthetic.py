"""Synthetic fixture builders that mimic documented layouts [MCR p.9; NB p.14-16].

All content is invented. Nothing here is real ECG data.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

LEADS_12 = ["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"]
# PTB Diagnostic: standard 12 + Frank X/Y/Z (C2.3), lowercase as in its headers
PTB_DIAG_15 = ["i", "ii", "iii", "avr", "avl", "avf",
               "v1", "v2", "v3", "v4", "v5", "v6", "vx", "vy", "vz"]


def write_hea(path: Path, record_name: str, fs: float, n_samples: int,
              leads: list[str], fmt: str = "16", comments: list[str] = ()) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"{record_name} {len(leads)} {fs:g} {n_samples}"]
    lines += [f"{record_name}.dat {fmt} 1000/mV 16 0 0 0 0 {lead}" for lead in leads]
    lines += [f"# {c}" for c in comments]
    path.write_text("\n".join(lines) + "\n")


def make_ptb_xl(root: Path, n: int = 4, *, fs_hr: float = 500) -> pd.DataFrame:
    """ptbxl_database.csv + records500/ + records100/ for the same ECGs."""
    rows = []
    for k in range(n):
        ecg_id = k + 1
        stem = f"{ecg_id:05d}"
        hr = f"records500/00000/{stem}_hr"
        lr = f"records100/00000/{stem}_lr"
        write_hea(root / f"{hr}.hea", f"{stem}_hr", fs_hr, int(fs_hr * 10), LEADS_12)
        write_hea(root / f"{lr}.hea", f"{stem}_lr", 100, 1000, LEADS_12)
        rows.append({"ecg_id": ecg_id, "patient_id": 100 + k // 2,
                     "filename_lr": lr, "filename_hr": hr})
    df = pd.DataFrame(rows)
    df.to_csv(root / "ptbxl_database.csv", index=False)
    return df


def make_mimic(root: Path, n: int = 3) -> pd.DataFrame:
    """record_list.csv (subject_id, study_id, path) + files/pNNNN/pSUBJECT/sSTUDY/."""
    rows = []
    for k in range(n):
        subject_id = 10000032 + k
        study_id = 40000000 + k
        rel = f"files/p{str(subject_id)[:4]}/p{subject_id}/s{study_id}/{study_id}"
        write_hea(root / f"{rel}.hea", str(study_id), 500, 5000, LEADS_12)
        rows.append({"subject_id": subject_id, "study_id": study_id, "path": rel})
    df = pd.DataFrame(rows)
    df.to_csv(root / "record_list.csv", index=False)
    return df


def make_code15(root: Path, exam_ids=(301, 302, 303, 304), *,
                valid_samples=(4096, 2800, 4000, 3000)) -> pd.DataFrame:
    """Mock shard: tracings N x 4096 x 12 zero-padded + exam_id vector as .npy
    (stand-in for the HDF5 layout, C2.2), and exams.csv in reversed row order."""
    root.mkdir(parents=True, exist_ok=True)
    n = len(exam_ids)
    tracings = np.zeros((n, 4096, 12), dtype=np.float32)
    rng = np.random.default_rng(0)
    for i, valid in enumerate(valid_samples):
        pad = (4096 - valid) // 2
        tracings[i, pad:pad + valid, :] = rng.normal(size=(valid, 12))
    np.save(root / "exams_part0_tracings.npy", tracings)
    np.save(root / "exams_part0_exam_id.npy", np.array(exam_ids, dtype=np.int64))
    exams = pd.DataFrame({"exam_id": list(exam_ids),
                          "age": [40 + i for i in range(n)],
                          "trace_file": "exams_part0.hdf5"})
    exams = exams.iloc[::-1].reset_index(drop=True)  # row order differs from shard (C2.2)
    exams.to_csv(root / "exams.csv", index=False)
    return exams


def make_ptb_diagnostic(root: Path, patients=("patient001", "patient002")) -> list[str]:
    records = []
    for p_i, patient in enumerate(patients):
        rec = f"s{p_i + 1:04d}_re"
        write_hea(root / patient / f"{rec}.hea", rec, 1000, 38400, PTB_DIAG_15,
                  comments=["synthetic header"])
        records.append(f"{patient}/{rec}")
    return records


def make_challenge(root: Path, stems=("JS00001", "JS00002")) -> None:
    """Challenge-style .hea + ``<stem>_val.npy`` standing in for .mat ``val``
    (leads x samples, C2.4). The inventory never opens the signal file."""
    for stem in stems:
        write_hea(root / f"{stem}.hea", stem, 500, 5000, LEADS_12, fmt="16+24",
                  comments=["Age: 50", "Dx: 000000"])
        np.save(root / f"{stem}_val.npy", np.zeros((12, 5000), dtype=np.int16))
