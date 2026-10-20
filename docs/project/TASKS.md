# TASKS — Acute STEMI / NSTEMI / non-MI ECG research

Maintained by **planner-checker**. Governing docs: `data_contract.md` (0.1.0-draft) and `research_plan.md` (0.1.0-draft).
Evidence base: the three PDFs in `19-oct-2026/` only. **No data downloads. Synthetic fixtures only.**

Test command (from project root): `.venv/bin/python -m pytest`

Session scope (2026-10-19): **T1**, **T2** and **T-DEMO** (added on user request via team lead) are active. Everything else is out of scope this session.

## Task list

| ID | Title | Plan step | Owner | Status | Contract rules |
|---|---|---|---|---|---|
| T1 | Data inventory (synthetic only): source registry + fixtures + inventory table | 1 (+ §3 test strategy) | coder | **approved** (round 2) | C2.1–C2.9, §2.1, §2.3, O2, O3, O7, O8, P2, P5, E2, E3, V1, V2 |
| T2 | Label mapping M0–M12 on synthetic data | 4 (§2 mapping rules) | coder | **approved** (round 1) | L1–L14, §3.2, §2.1 schema, M0–M12, invariants 1–6, S7, O11, E4, V4 |
| T-DEMO | Synthetic end-to-end performance demo (no clinical meaning) | 1→4→6→8 on synthetic data | coder | **approved** (round 1; user-approved via team lead 2026-10-19) | C1.3, P6, L1, M1, S1, S4, S8, invariants 1 & 5, step 8 gate |
| T3 | Bounded header validation on real local PTB-XL / MIMIC files | 1 (real data) | — | blocked/not started — out of scope this session (needs user-supplied local paths) | E2, E3 |
| T4 | Resolve priority technical evidence gaps | 2 | — | blocked/not started — out of scope this session | E1, E2, E5, C2.2, C2.6, C2.9 |
| T5 | Model input specification (`input_spec.json`) | 3 | — | blocked/not started — out of scope this session (Q9) | C1.3, P1–P6 |
| T6 | Clinical label review (`review_decisions.csv`) | 5 | — | blocked/not started — out of scope this session (needs clinical supervisor; Q2, Q4, Q5) | L7, L13, L14 |
| T7 | Leakage controls, patient-level splits, split audit | 6 | — | blocked/not started — out of scope this session (Q6, Q7, Q10) | S1–S9, O1–O11 |
| T8 | Per-source decision record (`source_decisions.csv`) | 7 | — | blocked/not started — out of scope this session | E4, L11 |
| T9 | Freeze comparison protocol | 8 | — | blocked/not started — out of scope this session (gate: steps 4–7 signed off) | S4, S5 |
| T10 | Reporting | 9 | — | blocked/not started — out of scope this session | — |

## T1 — Data inventory (synthetic only)

Scope: research_plan step 1 (structure only, run on fixtures) + §3 fixtures. No real data, no downloads.

Acceptance criteria:

1. **Registry module** (`src/…`) encodes all 11 rows of data_contract §2.1 with the *exact* engine keys (`ptb_xl`, `mimic_iv_ecg`, `ningbo`, `chapman_shaoxing`, `georgia`, `cpsc_2018`, `cpsc_extra`, `sph`, `ptb_diagnostic`, `incart`, `code15`) and exact release strings (V1), publisher ECG count, Hz, leads, duration (ranges/unknown kept as stated, not coerced), container, source ref, plus the §2.3 technical status. Values are labelled publisher-level/documentary, not measured (E3).
2. Registry is read-only to the inventory code: observations never overwrite registry values (E3, P3). One observed header never updates a release-level fact (E2).
3. **Edition distinctness (O3, O7, O8):** INCART native 1.0.0 (75) is the registered edition; the Challenge subset (74) is never silently merged — if represented, it is a distinct edition entry/key. PTB-XL count is 21,799 for 1.0.3; the historical 21,837 must not appear as a 1.0.3 count (test asserts this).
4. **records100 (C2.1, O2):** inventory uses `records500` only; `records100` files are not counted as extra ECGs (test with a fixture containing both).
5. **Synthetic fixtures** (generated in `tmp_path` / a fixtures helper; no committed real data) mimicking documented layouts: PTB-XL `ptbxl_database.csv` (`ecg_id`, `patient_id`, `filename_hr`, `filename_lr`) + `records500/` + `records100/`; MIMIC `record_list.csv:path` + `files/p…/s…` (`subject_id`, `study_id`); CODE-15% `tracings` N×4096×12 with padding (HDF5 layout mocked with numpy — **.venv is pandas + pytest only, no h5py/scipy**, per team lead) and `exams.csv` whose row order differs from the HDF5 (join on `exam_id`, C2.2); PTB Diagnostic 15-channel header in `patientNNN/` (C2.3). Challenge `.hea`/`.mat` (`val` leads × samples, C2.4) is welcome but optional.
6. **Inventory table** with P2 fields per record: `dataset_id`, `release`, `record_id`, `patient_key`, `native_rate`, `target_rate`, `original_duration_s`, padding info/mask flag, plus an observation-type label marking rows as synthetic/local observation (E3). `target_rate` must not be silently fixed to 500 — the input spec is unresolved (C1.3, Q9); null or explicitly flagged provisional.
7. Rates stay in separate fields; no field mixes acquisition rate, released rate and filter cutoffs (P5). MIMIC `cart_id` not treated as device model; filter strings not parsed as numeric cutoffs (C2.6) — if these fields are touched at all.
8. CODE-15%: stored 4096/400 = 10.24 s recorded as *stored* length, not observed duration (C2.2).
9. PTB Diagnostic: 15 channels recognised; the standard-12 selection is identified (C2.3). No 1000→500 Hz conversion implemented as a decided policy.
10. Pinned upstream provenance (V2) available as a constant.
11. Tests pass with `.venv/bin/python -m pytest`.

## T2 — Label mapping (synthetic)

Acceptance criteria:

1. Implements M0–M12 in research_plan §2.2, evaluated in order, first match wins; every output row carries `rule_id`.
2. Output columns exactly match research_plan §2.1 (names, enum values).
3. `APPROVED_MI_STATEMENT_CODES` and `APPROVED_ST_INJURY_CODES` are **empty**; `ACUTE_WINDOW = None` (BG-UNCONFIRMED / Q2). Therefore M7/M8/M9/M10 cannot fire in production config; tests may inject lists/windows locally to exercise the branches.
4. M1 is the only path to `confirmed`; a review record lacking a reviewer must be rejected.
5. M3 drops PTB-XL `records100` rows entirely (not `excluded`).
6. M4: no code / `none` → `unresolved`, never `non-MI` (L1).
7. M11 conflicts → `unresolved` with conflict noted in `supporting_evidence`.
8. `pretraining_eligible` defaults to False (L11 requires technical/access review).
9. No hard-coded clinical decisions (e.g. INCART exclusion, overlap-group membership beyond what the contract states) — anything ASSUMPTION/BG-UNCONFIRMED is configurable and flagged.
10. Unit tests for all six invariants of research_plan §2.2, plus M3 and M11.
11. Tests pass.

## T-DEMO — Synthetic performance demo

User-approved via team lead. Starts only after T2 is approved. **Synthetic data only; numbers have no clinical meaning; not a model trained on real ECGs; the step 8 gate still applies to all real data.**

Acceptance criteria:

1. Generator for synthetic ECG-like arrays, 12 leads × 10 s × 500 Hz (C1.3 provisional, P6 lead order — both ASSUMPTION, flagged), for several fake patients across ≥2 fake sources, with fixed seed.
2. Labels STEMI / NSTEMI / non-MI enter **only** through a synthetic `review_decisions` table → M1 (with reviewer + date). Records without a review decision stay `unresolved` and never become non-MI (L1, invariant 1/2). Production code lists stay empty / `ACUTE_WINDOW = None` — the demo must not modify them.
3. Pipeline end to end: inventory (T1) → label mapping (T2) → patient-level split with fixed seed (S1, S8) → baseline classifier using numpy/pandas only (no sklearn/torch/scipy) → metrics.
4. Only `status == confirmed` rows reach train/test (invariant 5). Zero patient-key overlap across splits (S1).
5. Hierarchical (MI vs non-MI → STEMI vs NSTEMI) and flat three-class evaluated on the **same** split and same features (S4), if feasible.
6. Metrics: per-class sensitivity/specificity and macro-F1, flagged as ASSUMPTION (research_plan step 8).
7. Runnable as `.venv/bin/python -m src.demo` (or similar); writes a small results file whose content carries the synthetic/no-clinical-meaning disclaimer; seeded and reproducible.
8. Tests: no patient overlap across splits; only confirmed rows reach training; all prior tests still pass.

## Review log

| Date | Task | Round | Outcome | Notes |
|---|---|---|---|---|
| 2026-10-19 | — | — | Tasks defined | T1 assigned to coder |
| 2026-10-19 | T1 | 1 | **Changes requested** | 34 passed observed. Rejected only for the disallowed dependency: h5py imported in src/tests, listed in pyproject, installed in .venv (team rule from user: pandas + pytest only). All contract checks passed (V1, V2, §2.3, E2, E3, P3, P5, C1.3, C2.1–C2.3, C2.6, O2, O3, O7, O8). Coder defaults accepted: CODE/Challenge patient_key null, INCART Challenge unregistered, native lead order kept. |
| 2026-10-19 | T1 | 2 | **Approved** | Verified myself: `.venv/bin/python -m pytest` → 35 passed; .venv has only pandas 3.0.6, numpy 2.5.4, pytest 9.1.1; no h5py import in src/tests; pyproject deps = ["pandas"]. CODE-15% HDF5 layout mocked via `.npy` behind a `shard_reader` interface (C2.2 checks preserved); Challenge `val` mocked as leads×samples `.npy` (C2.4). Optional P4 improvement done: `standard12_channel_map` returns {lead: native index}; re-verified 35 passed. |
| 2026-10-19 | T2 | 1 | **Approved** | Verified myself: 68 passed (35 T1 + 33 T2); pandas/numpy only. Read `src/stemi/label_mapping.py` in full: §2.1 columns/enums exact; production lists empty + `ACUTE_WINDOW=None` (zero candidates); M1 sole path to confirmed with validated `ReviewDecision`; M2 reason required, no INCART hard-coding; M3 drops records100; M4/M5/M6 never non-MI (L1/L2); M11 conflicts unresolved; `pretraining_eligible` default False (L11); S7 record_proxy; O11 groups in one ASSUMPTION constant; invariants 1–6 tested incl. corrupted-table checks. Own probes: blank exclusion reason rejected; records100 dropped. Coder interpretations (a) M3 as pre-filter, (b) M7 before M8 per table order, (c) M11 before M9/M10, (d) rule_id M0 when window undefined, (f) L13 history deferred to T6 — accepted as conservative. (e) linked_diagnoses vocabulary and (g) PTB-XL/PTB Diagnostic grouping → sent to team lead. Note for T-DEMO: record_proxy keys can coincide across datasets (e.g. ningbo "7" vs georgia "7"), so splits must group on (dataset_id, patient_key) or broader. |
| 2026-10-19 | T-DEMO | 1 | **Approved** | **SYNTHETIC — no clinical meaning.** Verified myself: 78 passed (68 prior + 10 new); numpy/pandas only. Read `src/stemi/demo.py` in full: labels only via synthetic review table → M1 (unreviewed → M4 unresolved, 0 candidates); PRODUCTION_CONFIG untouched; `supervised_rows` gates training; split grouped on (dataset_id, patient_key), seeded, stratified on confirmed group class (S8 "where possible" — accepted); standardisation fit on train only; flat and hierarchical on same split/features (S4); disclaimer in file + stdout; never overwrites. Re-ran `PYTHONPATH=src .venv/bin/python -m stemi.demo --out-dir <scratchpad>` with seed 20261019: output identical to coder's `demo_results/demo_results_seed20261019_20261018T205003Z.json` except timestamp. Observed: 144 inventory rows; 110 confirmed (M1) / 34 unresolved (M4); patient groups train/val/test 32/6/9; n per class (STEMI/NSTEMI/non-MI) train 26/27/23, val 4/4/5, test 7/6/8. Test: flat macro-F1 1.00 (all sens/spec 1.00); hierarchical macro-F1 0.95 (NSTEMI sens 0.83, non-MI spec 0.92, rest 1.00). Val: both 1.00. Near-perfect scores reflect trivially separable invented patterns. |

## Open questions sent to team lead

Conservative default in force for each; none decided by the team.

1. ACUTE_WINDOW / acute-MI reference standard (contract Q2) — default None; M9/M10 never fire.
2. Approved MI-statement and ST/injury code lists for M7/M8 (plan Q2, BG-UNCONFIRMED) — default empty; zero candidates.
3. INCART scope (Q8) — no hard-coded exclusion; `pretraining_eligible=False`.
4. `overlap_group` membership (O11 ASSUMPTION) — Challenge-2021 sources share `challenge_2021`; all others separate.
5. `record_proxy` patient keys for sources without patient IDs (S7 ASSUMPTION; Q6) — implemented as drafted.
6. `linked_diagnoses` vocabulary {STEMI, NSTEMI, no_acute_mi} (ASSUMPTION) — inert until Q2/Q3.
7. PTB-XL + PTB Diagnostic shared overlap group? (BG-UNCONFIRMED) — default: separate.
8. CODE-15% `patient_id` column (BG-UNCONFIRMED) — not read; patient_key null.
9. h5py approval for a real HDF5 reader (CODE-15%, SPH) — deferred; `.npy` stand-in only.
10. Input spec (Q9), lead order (P6), split ratio (Q10), step-8 metric set — used provisionally in T-DEMO only, flagged.
11. Plus data_contract §9 Q1, Q3–Q7, Q11, Q12 and research_plan §4 Q3–Q6, unchanged.

**Session closed 2026-10-19:** T1, T2, T-DEMO approved; documenter finished; final report sent to team lead.
