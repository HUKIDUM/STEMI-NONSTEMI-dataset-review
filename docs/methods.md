# Methods (T1 data inventory, T2 label mapping, T-DEMO synthetic demo)

> All code described here runs on **synthetic fixtures** only. No real ECG data was downloaded, opened or processed. Dataset facts come from the documentary registry in the PDFs [CMP p.2; MCR p.3], not from observed files.

## 1. Evidence base

Three PDFs in `19-oct-2026/` (keys CMP, MCR, NB; data_contract §0). Governing docs: `data_contract.md`, `research_plan.md`. Task definitions and acceptance criteria: `TASKS.md`. Plain-language summary of the 10 Oct 2026 analysis, the 11-source table and the ordered next steps: `NEXT_STEPS.md` (planner-checker, 2026-10-19).

## 2. T1: Data inventory (approved, round 2)

Environment: `.venv` with pandas 3.0.6, numpy 2.5.4 and pytest 9.1.1 only. No h5py, scipy, sklearn or torch (user rule, via team lead).

### 2.1 Registry: `src/stemi/registry.py`

- `REGISTRY` holds 11 frozen `RegistryEntry` records, one per row of data_contract §2.1, keyed by the exact engine keys [NB p.11–13]. It is a read-only `MappingProxyType`, so assigning to it raises an error (E3, P3).
- Each entry stores:
  - release string (V1)
  - publisher ECG count and publisher Hz (the released rate, not the acquisition rate; P5)
  - lead count
  - duration as stated, kept as a string ("5–10", "Unknown", "7–10 (stored padded to 4096 samples)") and never converted to a number
  - container and source reference
  - §2.3 technical status and the "required before use" text [MCR p.8]
- Every entry is tagged `evidence_level = "documentary_publisher_level"`. That marks the values as copied from the PDFs, not measured [MCR p.3].
- `get_entry(dataset_id, release)` rejects unknown keys. It also raises `ReleaseMismatchError` for any release other than the registered one (V1, O3, O7). As a result, the INCART Challenge subset (74 records) can't be resolved to native 1.0.0 (75 records) [MCR p.3; NB p.9].
- PTB-XL 1.0.3 is registered with 21,799 ECGs. The historical count of 21,837 is never used for this release (O8) [NB p.9; NB p.14].
- `UPSTREAM_PROVENANCE` pins the 10 Oct 2026 run (V2) [MCR p.11; NB p.10; NB p.24]. The registry digest file `run_provenance.json` is not in this repo (Q1).

### 2.2 Inventory: `src/stemi/inventory.py`

What the inventory reads, and what it never reads:
- It reads metadata tables, WFDB `.hea` text and array shapes only.
- It never loads ECG sample values, and it never downloads or deletes anything.

What each output row contains:
- Every row is labelled `observation_type = "local_observation"` (E3) and carries a required `data_origin` of `synthetic_fixture` or `local_files`.
- The output has a fixed column list (`INVENTORY_COLUMNS`) that includes the P2 fields:
  - `dataset_id`, `release`, `record_id`, `patient_key`
  - `native_rate`, `target_rate`, `original_duration_s`, `stored_duration_s`
  - `padding_status`, `padding_mask`

How the rules are enforced:

| Behaviour | Rule |
|---|---|
| Registry values (`registry_hz`, `registry_leads`) are copied next to header observations for comparison. A disagreement is written to `conflicts` and the registry is left unchanged. | E2, P3 |
| A missing header is recorded (`header_found = False`). The code doesn't search for a replacement. | [NB p.29–30] |
| `target_rate` is null and `target_rate_status = "unresolved (C1.3, Q9)"`. It is never fixed at 500 Hz. | C1.3 |
| Native rate, acquisition rate and raw filter text are separate columns. | P5 |
| Optional bounded selection takes a random `limit` of the first 10,000 metadata rows with a fixed seed (default 0). The rule text is stored in `selection_rule`. | plan step 1 [NB p.29–30] |
| `write_inventory` refuses to overwrite an existing file. | P3, V5 (ASSUMPTION) |

Per-source readers:

| Function | Source layout | Rule-specific behaviour |
|---|---|---|
| `inventory_ptb_xl` | `ptbxl_database.csv` (`ecg_id`, `patient_id`, `filename_hr`) plus headers | Reads `filename_hr` only and raises an error if a path is not under `records500/`. `records100` is never counted (C2.1, O2). Patient key: `patient_id` [MCR p.9]. |
| `inventory_mimic_iv_ecg` | `record_list.csv` (`subject_id`, `study_id`, `path`) plus headers | Patient key: `subject_id`; record ID: `study_id` [MCR p.9]. `cart_id` and filter strings are not read (C2.6). |
| `inventory_ptb_diagnostic` | `patientNNN/*.hea` | Recognises the 15 channels, and `standard12_channel_map` maps each standard lead name to its native index while keeping native order (C2.3, P4). No 1000→500 Hz conversion is applied. Patient key: the patient folder name [MCR p.9]. |
| `inventory_challenge` | `*.hea` in a Challenge 2021 directory (`ningbo`, `chapman_shaoxing`, `georgia`, `cpsc_2018`, `cpsc_extra`) | Headers only; signal files are not opened. `patient_key` is null because the PDFs give no patient key; S7 is applied later. |
| `inventory_code15` | `exams.csv` plus shard arrays read through a `shard_reader` interface | Joins on `exam_id`, never on row position, and raises an error on duplicate or missing `exam_id` (C2.2) [MCR p.9]. `stored_duration_s` is 4096 / 400 = 10.24 s. `original_duration_s` stays null, and `padding_status` says the padding interpretation is unresolved [MCR p.3; NB p.16]. `patient_key` is null. |

CODE-15% is really distributed as HDF5 [MCR p.3], but reading HDF5 needs h5py, which isn't approved. The default `read_npy_shards` reads `<shard>_tracings.npy` and `<shard>_exam_id.npy` pairs instead. It opens the tracings with `mmap_mode`, so only the shape is read, not the values. An HDF5 reader is deferred.

## 3. T2: Label mapping (approved, round 1): `src/stemi/label_mapping.py`

The mapper turns source annotations into the contract's label-status vocabulary (data_contract §3.2; the semantics are an ASSUMPTION, A1). On its own it produces only `candidate`, `unresolved` and `excluded` rows. A label becomes `confirmed` only through a review decision. `MAPPING_VERSION = "0.1.0"`, and every row carries `contract_version` and `mapping_version` (V4, ASSUMPTION).

### 3.1 Production configuration (nothing clinical is decided)

| Constant | Production value | Effect | Basis |
|---|---|---|---|
| `APPROVED_MI_STATEMENT_CODES`, `APPROVED_ST_INJURY_CODES` | empty, read-only | M7/M8 cannot fire | L4, L7; plan Q2 (BG-UNCONFIRMED) |
| `ACUTE_WINDOW` | `None` | M9/M10 cannot fire | Q2 |
| `NO_TARGET_LABEL_SOURCE` (M12) | empty | Which sources qualify (e.g. `code15`) is not encoded | BG-UNCONFIRMED |
| `OVERLAP_GROUPS` | Each source is its own group, except the five Challenge 2021 sources, which share `challenge_2021` | Same-distribution sources stay together | O11 (ASSUMPTION); also covers O4, O5 |
| `LINKED_DIAGNOSES` | `STEMI`, `NSTEMI`, `no_acute_mi` | Vocabulary for `linked_clinical` inputs | ASSUMPTION, open question (e) |

Under this configuration the mapper produces **zero** `candidate` rows; a test checks this. Tests build their own `MappingConfig` to exercise M7–M10, and the module constants are never changed.

### 3.2 Rules (first match wins; every row carries `rule_id`)

| Rule | Implementation |
|---|---|
| M3 | Runs **first**, as a pre-filter: a PTB-XL `records100` path makes the record drop out completely (it returns `None`, not `excluded`) (O2). |
| M0 | Base row: `status = unresolved`, `rule_id = M0`. `release` is checked against the registry (V1). `label_source` must be one of the §2.1 enum values. |
| S7 | A missing `patient_key` becomes `record_id`, with `patient_key_quality = record_proxy`. Otherwise it is `native`. |
| M1 | The only path to `confirmed`. It requires a validated `ReviewDecision` with a non-empty reviewer and review date. The review status must be `confirmed`, `unresolved` or `excluded`. `final_class` must be set exactly when the status is `confirmed`, and an `excluded` review needs a reason. A review overrides any codes. |
| M2 | A technical exclusion needs a non-empty reason (E4). No source (e.g. INCART) is excluded in the code itself. |
| M9 / M10 / M11 | For `linked_clinical` inputs, the conflict check (M11) runs **before** M9/M10. Multiple diagnoses, or `no_acute_mi` together with MI/ST codes, gives `unresolved` with the conflict written to `supporting_evidence`. With `ACUTE_WINDOW = None`, rows stay `unresolved` with `rule_id = M0` and the note "acute window undefined (Q2)". With a window set, a timed STEMI/NSTEMI diagnosis gives a `candidate` with that class (M9), and `no_acute_mi` gives a `candidate` `non-MI` (M10, L14). |
| M4 | `label_source == none`, or no codes: `unresolved`, never non-MI (L1). |
| M5 / M6 | Machine text, rhythm labels and beat annotations: `unresolved` (L2). |
| M7, then M8 | ST/injury hit (M7) or MI-statement hit (M8): `candidate` with `MI_unspecified`, never STEMI/NSTEMI (L2, L3). The table order puts M7 first; the research_plan §2.3 sketch prefers M8, but status and proposed class come out the same either way. |
| M12 | `unresolved` for sources listed in `NO_TARGET_LABEL_SOURCE` (empty by default). |
| fallback | Codes present but none approved: `unresolved`, `rule_id = M4` (L1). |

`pretraining_eligible` defaults to `False` for every dataset. It can be set only per dataset by the caller (L11). `original_label` is passed through unchanged (L5, P3).

### 3.3 Invariants and loaders

`map_records` builds the §2.1 table and calls `validate_label_table`. That check enforces:
- the exact column list and enum values
- invariant 1: `final_class` is set exactly when the status is `confirmed`, and confirmed rows have rule M1 and a reviewer
- invariant 2: `non-MI` appears only via M1
- invariant 3: M5–M8 never propose STEMI/NSTEMI
- `proposed_class` appears only on `candidate` rows
- invariant 6: excluded rows have a reason

Invariant 4 (`original_label` is byte-identical to the source) and invariant 5 are covered by tests. For invariant 5, `supervised_rows` returns only `confirmed` rows, and `pretraining_rows` returns only rows where `pretraining_eligible` is true.

### 3.4 Interpretations accepted by planner-checker

(a) M3 is a pre-filter. (b) M7 is checked before M8, following the table order. (c) M11 is checked before M9/M10. (d) `rule_id` is M0 when the acute window is undefined. (f) The L13 transition history is deferred to T6. All five are conservative choices. Two items, (e) and (g), went to the team lead (see decision_log).

## 3b. T-DEMO: synthetic end-to-end demo (approved, round 1): `src/stemi/demo.py`

> **SYNTHETIC DATA ONLY.** The signals, patients and labels are all invented. The class patterns don't model real STEMI/NSTEMI morphology. This is a pipeline check, not a model trained on real ECGs. The research_plan step 8 gate still applies to all real data [NB p.24; MCR p.1].

Run from the project root:

```
PYTHONPATH=src .venv/bin/python -m stemi.demo [--seed N] [--n-patients N] [--out-dir DIR]
```

- The default seed is `DEFAULT_SEED = 20261019`, and the default output directory is `demo_results/`.
- Each run writes a new file, `demo_results_seed<seed>_<UTC timestamp>.json`, and never overwrites an old one (P3).
- The file starts with the disclaimer and lists every assumption the demo used.

### Pipeline

1. **Synthetic sources** (`build_synthetic_sources`). Two fake sources use the `ptb_xl` and `mimic_iv_ecg` layouts, each with 24 fake patients (the default) and 3 records per patient.
   - PTB-XL also gets `records100` copies of each record. These must never be read (C2.1, O2).
   - Patient keys are the same in both sources on purpose, so the split has to group on (`dataset_id`, `patient_key`).
   - Each record's signal is an invented 12 × 5000 array: 12 leads × 10 s × 500 Hz (C1.3 provisional; P6 lead order, ASSUMPTION). It contains spikes and bumps plus noise.
   - Each fake class adds an invented segment offset: positive in V1–V4 for "STEMI", negative in V4–V6 for "NSTEMI", none for "non-MI". Every patient has one class.
2. **Synthetic review table.** About 80% of records (`review_fraction = 0.8`, random) get a `confirmed` review with `reviewer = "synthetic_reviewer"`. This is the **only** way a class enters the pipeline (M1).
3. **T1 inventory.** `inventory_ptb_xl` and `inventory_mimic_iv_ecg` run with `data_origin = "synthetic_fixture"`.
4. **T2 mapping.** Every record has `label_source = "none"` and no codes, and the mapping uses `PRODUCTION_CONFIG` unchanged. Reviewed records therefore become `confirmed` (M1), and the rest stay `unresolved` (M4) and never become non-MI (L1).
5. **Supervised rows only.** `supervised_rows` keeps the `confirmed` rows (invariant 5).
6. **Patient-level split** (`patient_split`). Whole (`dataset_id`, `patient_key`) groups are assigned with a fixed seed, using 70/15/15 (the S8 example ratio; Q10 is open). Groups are stratified on their most common confirmed class (S1, S8). Only confirmed rows take part (S9).
7. **Features.** Per-lead mean, standard deviation, 10th and 90th percentile, giving 48 values per record.
8. **Baselines** (numpy only). Both models are nearest-centroid on features standardised with the training set's mean and SD.
   - **Flat:** a three-class model.
   - **Hierarchical:** stage 1 is MI vs non-MI. For records predicted MI, stage 2 is STEMI vs NSTEMI, trained on MI records only.
   - Both use the same split and features (S4).
9. **Metrics** (research_plan step 8, ASSUMPTION). Per class: sensitivity, specificity and F1. Also macro-F1 and a confusion matrix, for both the val and test sets. Thresholds aren't tuned.

### Demo tests: `tests/test_demo.py` (10 collected)

They check:
- zero patient-group overlap across splits
- only confirmed rows reach train/test
- unreviewed rows never get a class
- `records100` is never used
- both models share the split, and counts are reported
- the same seed gives the same results
- production constants are untouched
- the synthetic array shape
- the metrics on toy labels
- `main` writes a new file that contains the disclaimer

## 4. Tests and fixtures

Fixture builders live in `tests/synthetic.py`. Their content is invented and mimics the documented layouts [MCR p.9; NB p.14–16]. They write into pytest's `tmp_path`, and no real data is committed. They cover:
- PTB-XL: csv plus `records500/` and `records100/` for the same ECGs
- MIMIC: `record_list.csv` plus `files/p…/s…`
- CODE-15%: `.npy` shards, padded, with an `exams.csv` whose row order differs from the shards
- PTB Diagnostic: 15-channel headers in `patientNNN/`
- Challenge: `.hea` files, with the `val` array mocked as a leads × samples `.npy` (C2.4)

Totals: 78 tests (T1 35, T2 33, T-DEMO 10); see results.md for the observed runs.

T2 tests are in `tests/test_label_mapping.py` (33 collected). They check:
- the schema, and the production config being empty and yielding zero candidates
- that an injected config doesn't change the module constants
- each of invariants 1–6
- eight invalid-review cases for M1, and that an unvalidated review object is rejected
- M2 needs a reason and has no hard-coded INCART exclusion
- M3 drops `records100` rows
- M4/M5/M6 give `unresolved`
- M7/M8 fire only with injected lists, and M9/M10 need both a window and timing
- M11 conflicts carry evidence
- M12 is off by default, and `pretraining_eligible` defaults to `False`
- S7 record proxy and the O11 groups
- release and `label_source` validation

T1 tests are in `tests/test_registry.py` (18 collected) and `tests/test_inventory.py` (17 collected). Notable checks:
- the registry has the exact engine keys, and its values match the contract (parametrised over all 11 sources)
- durations stay strings, and the registry is read-only
- 21,837 is never used for PTB-XL 1.0.3, and the INCART Challenge subset isn't merged
- provenance is pinned
- PTB-XL uses `records500` only and rejects `records100` paths
- a header conflict never updates the registry, and a missing header is recorded
- bounded selection is seeded
- CODE-15% joins on `exam_id` rather than row order, records the stored length rather than an observed duration, refuses a positional join without `exam_id`, and accepts a custom shard reader
- PTB Diagnostic has 15 channels with the standard 12 identified in native order
- `write_inventory` refuses to overwrite a file
