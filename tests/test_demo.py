"""T-DEMO: synthetic end-to-end demo. Numbers have no clinical meaning."""

import json

import numpy as np
import pandas as pd
import pytest

import stemi.label_mapping as lm
from stemi import demo


@pytest.fixture(scope="module")
def run(tmp_path_factory):
    return demo.run_demo(tmp_path_factory.mktemp("demo"), seed=7, n_patients=12)


def test_zero_patient_group_overlap_across_splits(run):  # S1
    sup = run["_frames"]["supervised"]
    groups = {s: set(zip(g["dataset_id"], g["patient_key"])) for s, g in sup.groupby("split")}
    assert set(groups) == set(demo.SPLITS)
    for a in demo.SPLITS:
        for b in demo.SPLITS:
            if a < b:
                assert not groups[a] & groups[b]
    # keys collide across sources on purpose; grouping must still be per (dataset_id, key)
    by_key = sup.groupby("patient_key")["dataset_id"].nunique()
    assert (by_key > 1).any()


def test_only_confirmed_rows_reach_train_and_test(run):  # invariant 5
    sup = run["_frames"]["supervised"]
    assert (sup["status"] == "confirmed").all()
    assert (sup["rule_id"] == "M1").all() and sup["reviewer"].notna().all()
    labels = run["_frames"]["labels"]
    assert len(sup) == (labels["status"] == "confirmed").sum() < len(labels)


def test_unreviewed_rows_never_get_a_class(run):  # L1, invariants 1/2
    labels = run["_frames"]["labels"]
    unrev = labels[labels["reviewer"].isna()]
    assert len(unrev) > 0
    assert (unrev["status"] == "unresolved").all() and (unrev["rule_id"] == "M4").all()
    assert unrev["final_class"].isna().all() and unrev["proposed_class"].isna().all()
    assert run["counts"]["label_status"].get("candidate", 0) == 0   # production config


def test_records100_never_used(run):  # C2.1, O2
    assert run["counts"]["inventory_rows"] == len(run["_frames"]["labels"])
    assert run["counts"]["inventory_rows"] == 12 * 3 * len(demo.DEMO_SOURCES)


def test_models_share_split_and_report_counts(run):  # S4
    for s in ("val", "test"):
        ns = {name: m[s]["n"] for name, m in run["metrics"].items()}
        assert len(set(ns.values())) == 1
        assert ns["flat_3class"] == sum(run["counts"]["n_per_class"][s].values())
    for m in run["metrics"].values():
        assert 0.0 <= m["test"]["macro_f1"] <= 1.0
        assert set(m["test"]["per_class"]) == set(demo.CLASSES)


def test_reproducible_same_seed(tmp_path):
    a = demo.run_demo(tmp_path / "a", seed=11, n_patients=9)
    b = demo.run_demo(tmp_path / "b", seed=11, n_patients=9)
    assert a["metrics"] == b["metrics"] and a["counts"] == b["counts"]
    pd.testing.assert_frame_equal(a["_frames"]["supervised"], b["_frames"]["supervised"])


def test_production_constants_untouched(run):
    assert dict(lm.APPROVED_MI_STATEMENT_CODES) == {}
    assert dict(lm.APPROVED_ST_INJURY_CODES) == {}
    assert lm.ACUTE_WINDOW is None


def test_synthetic_array_shape():
    x = demo.synth_ecg(np.random.default_rng(0), "STEMI", 1.0)
    assert x.shape == (12, 5000) and len(demo.LEADS) == 12


def test_metrics_on_toy_labels():
    y = np.array(["STEMI", "STEMI", "NSTEMI", "non-MI"])
    p = np.array(["STEMI", "NSTEMI", "NSTEMI", "non-MI"])
    m = demo.metrics(y, p)
    assert m["per_class"]["STEMI"]["sensitivity"] == 0.5
    assert m["per_class"]["NSTEMI"]["specificity"] == pytest.approx(2 / 3)
    assert m["per_class"]["non-MI"]["f1"] == 1.0
    assert m["confusion"]["STEMI"]["NSTEMI"] == 1


def test_main_writes_new_file_with_disclaimer(tmp_path, capsys):
    out1 = demo.main(["--seed", "3", "--n-patients", "6", "--out-dir", str(tmp_path)])
    out2 = demo.main(["--seed", "3", "--n-patients", "6", "--out-dir", str(tmp_path)])
    assert out1 != out2 and out1.exists() and out2.exists()       # never overwrites
    res = json.loads(out1.read_text())
    assert res["disclaimer"] == demo.DISCLAIMER and "_frames" not in res
    assert res["seed"] == 3 and res["data_origin"] == "synthetic_fixture"
    assert any("Q9" in a for a in res["assumptions"])
    assert capsys.readouterr().out.count(demo.DISCLAIMER) >= 2
