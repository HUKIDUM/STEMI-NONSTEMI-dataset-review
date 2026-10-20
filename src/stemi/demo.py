"""Synthetic end-to-end performance demo (TASKS.md T-DEMO).

SYNTHETIC DATA ONLY. Pipeline: synthetic fixtures -> T1 inventory -> T2 label
mapping (labels only via review decisions, M1) -> supervised_rows -> patient-level
split -> nearest-centroid baselines (flat and hierarchical) -> metrics.

Run from the project root:
    PYTHONPATH=src .venv/bin/python -m stemi.demo [--seed N] [--out-dir DIR]
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from . import CONTRACT_VERSION
from .inventory import inventory_mimic_iv_ecg, inventory_ptb_xl
from .label_mapping import (
    MAPPING_VERSION, PRODUCTION_CONFIG, map_records, reviews_from_frame, supervised_rows,
)

DISCLAIMER = ("SYNTHETIC DATA — numbers have no clinical meaning — not a model trained on "
              "real ECGs — research_plan step 8 gate still applies to real data.")

DEFAULT_SEED = 20261019
CLASSES = ("STEMI", "NSTEMI", "non-MI")
SPLITS = ("train", "val", "test")

# ASSUMPTIONS, all flagged in the results file:
FS_HZ = 500                     # C1.3 provisional study setting, not a decided input spec
DURATION_S = 10                 # C1.3 provisional
LEADS = ("I", "II", "III", "aVR", "aVL", "aVF",
         "V1", "V2", "V3", "V4", "V5", "V6")          # P6 ASSUMPTION (Q9)
SPLIT_FRACTIONS = (0.70, 0.15, 0.15)                  # S8 example ratio; Q10 open
DEMO_SOURCES = ("ptb_xl", "mimic_iv_ecg")
ASSUMPTIONS = [
    f"Input {len(LEADS)} leads x {DURATION_S} s x {FS_HZ} Hz is the C1.3 provisional setting, not a decided spec (Q9).",
    "Lead order I, II, III, aVR, aVL, aVF, V1-V6 follows P6 (ASSUMPTION).",
    "Split fractions 70/15/15 follow the S8 example; ratios are open question Q10.",
    "Metrics (per-class sensitivity/specificity, macro-F1) follow research_plan step 8 (ASSUMPTION).",
    "Class signal patterns are invented; they do not model real STEMI/NSTEMI morphology.",
    "Patient keys deliberately collide across the two fake sources; groups are (dataset_id, patient_key).",
]


# --------------------------------------------------------------------------- synthetic data


def synth_ecg(rng: np.random.Generator, cls: str, patient_gain: float) -> np.ndarray:
    """Invented 12 x 5000 ECG-like array. The class pattern is a fake segment offset."""
    n = FS_HZ * DURATION_S
    t = np.arange(n) / FS_HZ
    rr = 60 / rng.uniform(55, 95)
    beats = np.arange(rng.uniform(0, rr), DURATION_S, rr)
    base = np.zeros(n)
    seg = np.zeros(n)
    for b in beats:
        base += 1.0 * np.exp(-((t - b) / 0.012) ** 2)                 # spike
        base += 0.25 * np.exp(-((t - b - 0.28) / 0.05) ** 2)          # slow bump
        seg += ((t > b + 0.06) & (t < b + 0.20)).astype(float)        # post-spike segment
    lead_gain = patient_gain * rng.uniform(0.6, 1.4, size=(12, 1))
    x = lead_gain * base
    offset = np.zeros((12, 1))
    if cls == "STEMI":
        offset[6:10] = 0.25          # fake positive offset in V1-V4
    elif cls == "NSTEMI":
        offset[9:12] = -0.15         # fake negative offset in V4-V6
    x = x + offset * seg + rng.normal(0, 0.05, size=(12, n))
    return x.astype(np.float32)


def _write_hea(path: Path, name: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"{name} {len(LEADS)} {FS_HZ} {FS_HZ * DURATION_S}"]
    lines += [f"{name}.dat 16 1000/mV 16 0 0 0 0 {lead}" for lead in LEADS]
    path.write_text("\n".join(lines) + "\n")


def build_synthetic_sources(root: Path, seed: int, n_patients: int = 24,
                            records_per_patient: int = 3,
                            review_fraction: float = 0.8) -> pd.DataFrame:
    """Write fake PTB-XL / MIMIC layouts plus signal arrays (``<record>.npy``).

    Returns the synthetic review_decisions table. Each patient has one invented
    class; about ``1 - review_fraction`` of records get no review at all.
    """
    rng = np.random.default_rng(seed)
    reviews = []
    for ds in DEMO_SOURCES:
        meta = []
        for p in range(n_patients):
            patient = 10_000_001 + p            # same keys in both sources on purpose
            cls = CLASSES[p % len(CLASSES)]
            gain = rng.uniform(0.8, 1.2)
            for r in range(records_per_patient):
                rec_id = p * records_per_patient + r + 1
                if ds == "ptb_xl":
                    stem = f"{rec_id:05d}"
                    rel = f"records500/00000/{stem}_hr"
                    _write_hea(root / ds / f"{rel}.hea", f"{stem}_hr")
                    # records100 copy exists but must never be read (C2.1, O2)
                    _write_hea(root / ds / f"records100/00000/{stem}_lr.hea", f"{stem}_lr")
                    meta.append({"ecg_id": rec_id, "patient_id": patient,
                                 "filename_lr": f"records100/00000/{stem}_lr", "filename_hr": rel})
                else:
                    study = 40_000_000 + rec_id
                    rel = f"files/p{str(patient)[:4]}/p{patient}/s{study}/{study}"
                    _write_hea(root / ds / f"{rel}.hea", str(study))
                    meta.append({"subject_id": patient, "study_id": study, "path": rel})
                    rec_id = study
                np.save(root / ds / f"{rel}.npy", synth_ecg(rng, cls, gain))
                if rng.random() < review_fraction:
                    reviews.append({"dataset_id": ds, "record_id": str(rec_id), "status": "confirmed",
                                    "final_class": cls, "reviewer": "synthetic_reviewer",
                                    "review_date": "2026-10-19", "exclusion_reason": None,
                                    "notes": "synthetic demo label"})
        name = "ptbxl_database.csv" if ds == "ptb_xl" else "record_list.csv"
        pd.DataFrame(meta).to_csv(root / ds / name, index=False)
    return pd.DataFrame(reviews)


# --------------------------------------------------------------------------- pipeline


def patient_split(df: pd.DataFrame, seed: int) -> pd.Series:
    """Assign whole (dataset_id, patient_key) groups to splits with a fixed seed (S1, S8).

    Groups are stratified on their most common confirmed class (S8 "where possible").
    Expects confirmed rows only, so candidate/unresolved rows cannot move a patient (S9).
    """
    keys = list(zip(df["dataset_id"], df["patient_key"]))
    group_class = (pd.Series(df["final_class"].to_numpy(), index=pd.MultiIndex.from_tuples(keys))
                   .groupby(level=[0, 1]).agg(lambda s: sorted(s.mode())[0]))
    rng = np.random.default_rng(seed)
    assign = {}
    for cls in sorted(group_class.unique()):
        groups = sorted(group_class.index[group_class == cls])
        order = rng.permutation(len(groups))
        n_train = int(round(SPLIT_FRACTIONS[0] * len(groups)))
        n_val = int(round(SPLIT_FRACTIONS[1] * len(groups)))
        for rank, gi in enumerate(order):
            assign[groups[gi]] = ("train" if rank < n_train
                                  else "val" if rank < n_train + n_val else "test")
    return pd.Series([assign[k] for k in keys], index=df.index, name="split")


def features(x: np.ndarray) -> np.ndarray:
    """Simple per-lead statistics: mean, std, 10th and 90th percentile (48 values)."""
    return np.concatenate([x.mean(1), x.std(1), np.percentile(x, 10, axis=1),
                           np.percentile(x, 90, axis=1)])


class NearestCentroid:
    def fit(self, X: np.ndarray, y: np.ndarray) -> "NearestCentroid":
        self.mu, self.sd = X.mean(0), X.std(0) + 1e-8
        Z = (X - self.mu) / self.sd
        self.classes = np.array(sorted(set(y)))
        self.centroids = np.stack([Z[y == c].mean(0) for c in self.classes])
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        Z = (X - self.mu) / self.sd
        d = ((Z[:, None, :] - self.centroids[None]) ** 2).sum(-1)
        return self.classes[d.argmin(1)]


def fit_predict_flat(Xtr, ytr, Xte):
    return NearestCentroid().fit(Xtr, ytr).predict(Xte)


def fit_predict_hierarchical(Xtr, ytr, Xte):
    """Stage 1: MI vs non-MI. Stage 2 (MI only): STEMI vs NSTEMI."""
    mi_tr = np.where(ytr == "non-MI", "non-MI", "MI")
    stage1 = NearestCentroid().fit(Xtr, mi_tr).predict(Xte)
    is_mi = ytr != "non-MI"
    stage2 = NearestCentroid().fit(Xtr[is_mi], ytr[is_mi])
    out = stage1.astype(object)
    if (stage1 == "MI").any():
        out[stage1 == "MI"] = stage2.predict(Xte[stage1 == "MI"])
    return out.astype(str)


def metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """Per-class sensitivity/specificity/F1 and macro-F1 (research_plan step 8, ASSUMPTION)."""
    per_class, f1s = {}, []
    for c in CLASSES:
        tp = int(((y_pred == c) & (y_true == c)).sum())
        fn = int(((y_pred != c) & (y_true == c)).sum())
        fp = int(((y_pred == c) & (y_true != c)).sum())
        tn = int(((y_pred != c) & (y_true != c)).sum())
        sens = tp / (tp + fn) if tp + fn else None
        spec = tn / (tn + fp) if tn + fp else None
        prec = tp / (tp + fp) if tp + fp else 0.0
        f1 = 2 * prec * sens / (prec + sens) if sens and prec + sens else 0.0
        f1s.append(f1)
        per_class[c] = {"n": tp + fn, "sensitivity": sens, "specificity": spec, "f1": f1}
    confusion = {t: {p: int(((y_true == t) & (y_pred == p)).sum()) for p in CLASSES}
                 for t in CLASSES}
    return {"per_class": per_class, "macro_f1": float(np.mean(f1s)), "confusion": confusion,
            "n": int(len(y_true))}


def run_demo(workdir: Path, seed: int = DEFAULT_SEED, n_patients: int = 24) -> dict:
    """Run the whole pipeline on fixtures written under ``workdir``; returns results."""
    workdir = Path(workdir)
    review_table = build_synthetic_sources(workdir, seed, n_patients=n_patients)

    # T1 inventory (headers/metadata only)
    inv = pd.concat([
        inventory_ptb_xl(workdir / "ptb_xl", data_origin="synthetic_fixture"),
        inventory_mimic_iv_ecg(workdir / "mimic_iv_ecg", data_origin="synthetic_fixture"),
    ], ignore_index=True)

    # T2 mapping: no source annotations, so labels come only from reviews (M1); others M4
    records = [{"dataset_id": r.dataset_id, "record_id": r.record_id, "patient_key": r.patient_key,
                "label_source": "none", "original_label": None, "codes": [],
                "file_path": r.file_path} for r in inv.itertuples()]
    labels = map_records(records, reviews=reviews_from_frame(review_table),
                         config=PRODUCTION_CONFIG)
    sup = supervised_rows(labels).reset_index(drop=True)          # invariant 5
    paths = inv.set_index(["dataset_id", "record_id"])["file_path"]
    sup["split"] = patient_split(sup, seed)

    X = np.stack([features(np.load(workdir / ds / f"{paths[(ds, rid)]}.npy"))
                  for ds, rid in zip(sup["dataset_id"], sup["record_id"])])
    y = sup["final_class"].to_numpy(dtype=str)
    masks = {s: (sup["split"] == s).to_numpy() for s in SPLITS}

    models = {"flat_3class": fit_predict_flat, "hierarchical": fit_predict_hierarchical}
    results_metrics = {
        name: {s: metrics(y[masks[s]], fit(X[masks["train"]], y[masks["train"]], X[masks[s]]))
               for s in ("val", "test")}
        for name, fit in models.items()
    }
    n_per_class = {s: {c: int((y[masks[s]] == c).sum()) for c in CLASSES} for s in SPLITS}
    return {
        "disclaimer": DISCLAIMER,
        "seed": seed,
        "contract_version": CONTRACT_VERSION,
        "mapping_version": MAPPING_VERSION,
        "data_origin": "synthetic_fixture",
        "assumptions": ASSUMPTIONS,
        "sources": list(DEMO_SOURCES),
        "counts": {
            "inventory_rows": int(len(inv)),
            "label_status": labels["status"].value_counts().sort_index().to_dict(),
            "label_rule_id": labels["rule_id"].value_counts().sort_index().to_dict(),
            "supervised_rows": int(len(sup)),
            "patient_groups": {s: int(sup.loc[masks[s], ["dataset_id", "patient_key"]]
                                      .drop_duplicates().shape[0]) for s in SPLITS},
            "n_per_class": n_per_class,
        },
        "baseline": "nearest centroid on standardised per-lead mean/std/p10/p90 (numpy only)",
        "metrics": results_metrics,
        "_frames": {"labels": labels, "supervised": sup},   # dropped before writing
    }


def _unique_path(out_dir: Path, seed: int) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = out_dir / f"demo_results_seed{seed}_{stamp}.json"
    k = 1
    while path.exists():                      # never overwrite (P3, V5)
        path = out_dir / f"demo_results_seed{seed}_{stamp}_{k}.json"
        k += 1
    return path


def _fmt(v):
    return "n/a" if v is None else f"{v:.2f}"


def main(argv: list[str] | None = None) -> Path:
    ap = argparse.ArgumentParser(description=DISCLAIMER)
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--n-patients", type=int, default=24, help="fake patients per source")
    ap.add_argument("--out-dir", type=Path, default=Path("demo_results"))
    args = ap.parse_args(argv)

    with tempfile.TemporaryDirectory(prefix="stemi_demo_") as tmp:
        res = run_demo(Path(tmp), seed=args.seed, n_patients=args.n_patients)
    res.pop("_frames")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    out = _unique_path(args.out_dir, args.seed)
    res["generated_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    out.write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n")

    print(DISCLAIMER)
    print(f"seed={res['seed']}  supervised rows={res['counts']['supervised_rows']}  "
          f"label status={res['counts']['label_status']}")
    print(f"n per class per split: {res['counts']['n_per_class']}")
    for name, by_split in res["metrics"].items():
        m = by_split["test"]
        cls = "  ".join(f"{c}: sens {_fmt(v['sensitivity'])} spec {_fmt(v['specificity'])}"
                        for c, v in m["per_class"].items())
        print(f"[test] {name}: macro-F1 {m['macro_f1']:.2f}  {cls}")
    print(f"results: {out}")
    print(DISCLAIMER)
    return out


if __name__ == "__main__":
    main(sys.argv[1:])
