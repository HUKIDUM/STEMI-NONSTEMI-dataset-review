# Decision Log

Scope: tasks T1 (data inventory), T2 (label mapping) and T-DEMO (synthetic demo; scope extended by the team lead on 2026-10-19). Built under `data_contract.md` 0.1.0-draft and `research_plan.md` 0.1.0-draft.

Citation keys: CMP, MCR, NB (data_contract §0). Rule IDs refer to `data_contract.md` (C*, L*, S*, O*, P*, E*, V*) and `research_plan.md` §2.2 (M*).

Status values used here:
- **DECIDED (PDF)**: a hard rule stated by the PDFs.
- **PENDING SIGN-OFF (ASSUMPTION)**: a working decision the PDFs neither state nor contradict. Not decided until the user or clinical supervisor approves it.
- **PENDING SIGN-OFF (BG-UNCONFIRMED)**: background knowledge the PDFs don't confirm. Not decided.

## 1. Decisions taken from the PDFs (binding)

| # | Decision | Rule | Citation | Status |
|---|---|---|---|---|
| D1 | Dataset IDs use the exact engine keys (`ptb_xl`, `mimic_iv_ecg`, …) | §2.1 | [NB p.11–13] | DECIDED (PDF) |
| D2 | Every dataset reference carries the exact release string | V1 | [MCR p.3; NB p.9] | DECIDED (PDF) |
| D3 | PTB-XL `records100` is not counted as extra ECGs; only `records500` is used | C2.1, O2, M3 | [MCR p.3; MCR p.9; NB p.14] | DECIDED (PDF) |
| D4 | No MI code ≠ non-MI; such rows stay `unresolved` | L1, M4 | [MCR p.8; CMP p.5 step 3; NB p.23] | DECIDED (PDF) |
| D5 | Machine text, broad MI statements, ST/T changes and rhythm codes are never auto-converted to STEMI/NSTEMI | L2, L3, M5–M8 | [MCR p.8; CMP p.4] | DECIDED (PDF) |
| D6 | Uncertain/unresolved cases are kept, not forced into a class | L6 | [MCR p.10 item 3] | DECIDED (PDF) |
| D7 | Keep original label, source, ECG timing, evidence and reviewer decision for every label | L5 | [MCR p.8] | DECIDED (PDF) |
| D8 | All 11 sources currently have unverified acute three-class labels | L9 | [MCR p.8; NB p.24] | DECIDED (PDF) |
| D9 | Registry figures are documented releases, not observed files | §0 scope, E3 | [CMP p.2; MCR p.3] | DECIDED (PDF) |

## 2. Items pending user / supervisor sign-off

These are **not decided**. Questions go to the team lead.

| # | Item | Rule | Tag | Status |
|---|---|---|---|---|
| A1 | Four-status vocabulary `confirmed / candidate / unresolved / excluded` and its semantics | §3.2 | ASSUMPTION | PENDING SIGN-OFF |
| A2 | Allowed status transitions; only a review record can reach `confirmed` | L13 | ASSUMPTION | PENDING SIGN-OFF |
| A3 | `non-MI` confirmed only from positive evidence (what counts = Q4) | L14 | ASSUMPTION | PENDING SIGN-OFF |
| A4 | M0 default `unresolved` | M0 | ASSUMPTION (default) | PENDING SIGN-OFF |
| A5 | `label_source` category names | plan §2.1 | ASSUMPTION | PENDING SIGN-OFF |
| A6 | Approved MI-statement and ST/injury code lists are empty until clinical sign-off | M7, M8, plan Q2 | BG-UNCONFIRMED | PENDING SIGN-OFF |
| A7 | Acute window `ACUTE_WINDOW = None` (M9/M10 can't fire) | M9, Q2 | ASSUMPTION / open question | PENDING SIGN-OFF |
| A8 | Record-proxy patient key for sources without patient ID | S7 | ASSUMPTION | PENDING SIGN-OFF |
| A9 | `overlap_group` for same-institution/same-challenge sources | O11 | ASSUMPTION | PENDING SIGN-OFF |
| A10 | Semantic versioning of contract and derived artifacts | V4, V5 | ASSUMPTION | PENDING SIGN-OFF |
| A11 | Per-source label field names (e.g. PTB-XL `scp_codes`, challenge `#Dx:`) | plan §2.4 | BG-UNCONFIRMED | PENDING SIGN-OFF |
| A12 | CODE-15% `patient_id` column; no patient ID in challenge sources | §4 table | BG-UNCONFIRMED | PENDING SIGN-OFF |
| A13 | Country of origin per source, and collecting institutions other than SPH (Shandong Provincial Hospital, [CMP p.2]) | NEXT_STEPS.md §2 | BG-UNCONFIRMED | PENDING SIGN-OFF |
| A14 | Level A performance test: synthetic smoke test only, never reported as clinical performance. Now task T-DEMO, after T2 approval | NEXT_STEPS.md §3; TASKS.md T-DEMO | User-approved via team lead, 2026-10-19 | **DECIDED (user)** |
| A15 | Level B technical proxy on PTB-XL 1.0.3 records500 (approved-MI-statement vs positive-alternative target), never called acute STEMI/NSTEMI (L1–L3) | NEXT_STEPS.md §3; Q5 | ASSUMPTION | PENDING SIGN-OFF |
| A16 | Level C real three-class test is blocked until Q2–Q5, Q9, Q10 are answered and T3–T8 are done | NEXT_STEPS.md §3; plan step 8 gate [NB p.24; MCR p.1] | Blocked | NOT STARTED |
| A17 | T-DEMO metric set: per-class sensitivity/specificity and macro-F1 | plan step 8 | ASSUMPTION | PENDING SIGN-OFF |
| A18 | T-DEMO input 12 leads × 10 s × 500 Hz and the P6 lead order (synthetic only) | C1.3 [CMP p.5; MCR p.2; NB p.1], P6 | ASSUMPTION (provisional study setting, Q9) | PENDING SIGN-OFF |
| A19 | (e) The `linked_diagnoses` vocabulary {`STEMI`, `NSTEMI`, `no_acute_mi`} for `linked_clinical` inputs | M9–M11, L14, Q4 | ASSUMPTION; sent to team lead by planner-checker | PENDING SIGN-OFF |
| A20 | (g) Whether PTB-XL and PTB Diagnostic should share an overlap group. The code currently gives them separate groups. | O10, O11 | BG-UNCONFIRMED; sent to team lead | PENDING SIGN-OFF |
| A21 | Split procedure: generated once with a fixed seed at patient level, stratified, then frozen; assigned before any label is used for model selection; split ratios (Q10) | S8, S9 | ASSUMPTION | PENDING SIGN-OFF |

## 3. Decisions made during T1, T2 and T-DEMO

These were accepted by planner-checker in the reviews of 2026-10-19: T1-* in T1 rounds 1–2, T2-* in T2 round 1, D-* in T-DEMO round 1. They are implementation defaults. They decide nothing clinical, and every linked ASSUMPTION or BG-UNCONFIRMED item in §2 is still pending sign-off.

| # | Decision | Rule | Citation | Status |
|---|---|---|---|---|
| T1-1 | CODE-15% `patient_key` is null in the inventory. The PDFs give only `exam_id`. | §4 table, C2.2 | [MCR p.9] | ACCEPTED (conservative default); A12 still pending |
| T1-2 | Challenge-source `patient_key` is null. The S7 record proxy is applied later, not in the inventory. | §4 table, S7 | [MCR p.8] (Georgia linkage needs review) | ACCEPTED (conservative default); S7 still pending (A8) |
| T1-3 | The INCART Challenge subset (74) is not registered. Only native 1.0.0 (75) is registered, and a mismatched release raises an error. | O3, O7 | [MCR p.3; NB p.9] | ACCEPTED |
| T1-4 | Native channel order is kept in the inventory. Standard-12 leads are only *identified*, never reordered. | P4, P6 (ASSUMPTION), Q9 | [CMP p.2; CMP p.4] | ACCEPTED (model lead order still pending, A18) |
| T1-5 | `target_rate` is null with status "unresolved (C1.3, Q9)". | C1.3 | [CMP p.5; MCR p.2; NB p.1] | ACCEPTED |
| T1-6 | Environment is pandas + pytest only, with numpy present (pandas 3.0.6, numpy 2.5.4, pytest 9.1.1); no h5py. The CODE-15% HDF5 layout is mimicked with numpy `.npy` files behind a `shard_reader` interface; an HDF5 reader is deferred. | User rule via team lead; TASKS.md T1 AC5 | — | DECIDED (user); approved in T1 round 2 |
| T1-7 | `write_inventory` refuses to overwrite an existing file | P3; V5 | [MCR p.6; CMP p.5 step 5] | P3 DECIDED (PDF); the versioning scheme V5 is still pending (A10) |
| T2-1 | Production code lists empty, `ACUTE_WINDOW = None` and M12 list empty, so production output has zero candidates | M7–M10, M12; L4, L7; Q2 | [NB p.23; CMP p.5 step 3] | ACCEPTED (T2 round 1); the lists themselves are still pending (A6, A7) |
| T2-2 | M1, through a validated `ReviewDecision` (reviewer + date), is the only path to `confirmed`. Reviews may set only `confirmed`, `unresolved` or `excluded`. | L5, L7, L13 | [MCR p.8; CMP p.5 step 3] | ACCEPTED; the L13 semantics are still pending (A2) |
| T2-3 | (a) M3 runs as a pre-filter, so `records100` rows are dropped before any other rule | O2, M3 | [MCR p.3; NB p.14] | ACCEPTED |
| T2-4 | (b) M7 is checked before M8, following table order. The §2.3 sketch prefers M8, but the status and class come out the same. | M7, M8, L2 | [MCR p.8] | ACCEPTED |
| T2-5 | (c) The M11 conflict check runs before M9/M10, so a conflicting record can never become a candidate | M11, L6 | [MCR p.10 item 3] | ACCEPTED |
| T2-6 | (d) `rule_id = M0` (unresolved) for `linked_clinical` rows while the acute window is undefined | M9, M10, Q2 | — | ACCEPTED |
| T2-7 | (f) The L13 status-transition history log is deferred to T6 (clinical review) | L13 | — | ACCEPTED (deferred) |
| T2-8 | A missing patient key becomes `record_id` with `record_proxy` quality | S7 | — | Implemented; S7 is still pending (A8) |
| T2-9 | All five Challenge 2021 sources share overlap group `challenge_2021`; every other source is its own group | O11, O4, O5 | [MCR p.3; MCR p.8] | Implemented as a flagged constant; O11 is still pending (A9) |
| T2-10 | `pretraining_eligible` is `False` unless the caller sets it per dataset | L11 | [MCR p.8; NB p.33] | ACCEPTED |
| D-1 | The demo uses synthetic data only. Classes enter only through a synthetic review table via M1, with the production mapping config unchanged. | M1, L1, invariant 5; TASKS.md T-DEMO AC2 | — | ACCEPTED (T-DEMO round 1) |
| D-2 | Split groups on (`dataset_id`, `patient_key`), seeded and stratified, with only confirmed rows | S1, S8, S9 | [CMP p.5 step 4; MCR p.10 item 4] | ACCEPTED; S8/S9 are still pending (A21) |
| D-3 | Split ratio 70/15/15 | S8 example | — | Demo only; ASSUMPTION, Q10 open (A21) |
| D-4 | Hierarchical and flat models use the same split and features | S4 | [MCR p.10 item 5] | ACCEPTED |
| D-5 | Baseline is nearest-centroid on per-lead mean/SD/p10/p90, numpy only | User rule (no sklearn/torch/scipy) | — | Demo only; not a proposed model |
| D-6 | Seed 20261019; a new results file is written for each run, never overwritten | P3, V5 | [MCR p.6] | ACCEPTED; V5 is still pending (A10) |
| T1-8 | Bounded selection: a random `limit` of the first 10,000 metadata rows, with fixed seed 0 by default | plan step 1 | [NB p.29–30] | DECIDED (PDF default); the seed value 0 is an implementation choice |
