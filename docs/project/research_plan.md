# Research Plan: Acute STEMI / NSTEMI / non-MI ECG Classification

| Field | Value |
|---|---|
| Plan version | 0.1.0-draft (built under `data_contract.md` 0.1.0-draft) |
| Drafted | 2026-10-19 |
| Evidence base | The three PDFs in `19-oct-2026/` only. No downloads. |

Citation keys and tags are the same as `data_contract.md` §0:

- **CMP** = `ECG_Dataset_Comparison_Simple_Report.pdf`
- **MCR** = `ECG_Metadata_Compatibility_Report.pdf`
- **NB** = `MI_Metadata_Compatibility_Colab.ipynb - Colab.pdf`
- **ASSUMPTION** = a proposed decision that needs sign-off.
- **BG-UNCONFIRMED** = background knowledge not confirmed by the PDFs.

Contract rule IDs (C*, L*, S*, O*, P*, E*, V*) refer to `data_contract.md`.

## 0. Where we are

The 10 Oct 2026 run was documentary only. It covered 11 datasets and 55 pairs, and found 3 Low, 42 Moderate and 10 High pairs, all unconfirmed. It read no waveforms or local files and trained no model [CMP p.1; MCR p.1; MCR p.11]. The PDFs recommend this next stage: bounded metadata/header validation, then clinical-label review, then an agreed patient-level split plan [MCR p.1; MCR p.10]. The current results "do not yet justify an unconditional pooled training cohort" [MCR p.10].

**Constraint for this project:** do not download data. Code in steps 1–7 must be written and tested against **synthetic fixtures** that mimic the documented layouts [MCR p.9; NB p.14–16]. Running on real data happens only when the user supplies local paths (ASSUMPTION, consistent with the project memory and the user's brief).

## 1. Step-by-step analysis plan

### Step 1: Bounded metadata and header validation (PTB-XL, MIMIC-IV-ECG first)

- Compare available PTB-XL and MIMIC metadata and headers with the documented values. Save a table of observations, missing information and conflicts [CMP p.5 step 1; MCR p.10 item 1].
- Read only selected `.hea` files and never open sample arrays. The default selection is up to 50 candidates per source, drawn with a fixed seed from the first 10,000 metadata rows. Record missing headers and do not search for replacements [NB p.29–30].
- Candidate path columns: PTB-XL `ptbxl_database.csv:filename_hr`; MIMIC `record_list.csv:path` [NB p.30].
- Log the selection rule, files attempted, readable headers, missing files and conflicts. Label prefix previews and convenience samples [MCR p.10 item 1; NB p.27].
- Outputs are separate "local observation" artifacts and never overwrite the registry (E3) [NB p.25; NB p.29].
- **Deliverable:** `observed_metadata_<source>.csv` and `header_observations_<source>.csv` (file names are an ASSUMPTION).

### Step 2: Resolve priority technical evidence gaps

- Work in this order: units, gain/baseline, lead order, device semantics, filter metadata [MCR p.10 item 2].
- For each value, record the source URL, release, locator, reviewer and date. Never generalize one header to a whole release (E1, E2) [MCR p.10 item 2; NB p.10].
- MIMIC: verify header calibration and lead order, and inspect device/filter metadata [MCR p.6]. `cart_id` ≠ model; filter strings are not numeric cutoffs [NB p.27].
- CODE-15%: verify amplitude scale and padding interpretation [MCR p.8; NB p.16]. HDF5 schema checks inspect shape/dtype/chunking only and are not a calibration test [NB p.31].
- **Deliverable:** updated evidence review CSV in the notebook's `evidence_review_template.csv` format [NB p.10], plus the issue log (E5).

### Step 3: Define the model input specification

- The AI developer proposes lead order, electrical units, sampling rate and recording length. 12 leads / 500 Hz / 10 s is the current study setting, not proven optimal [CMP p.5 step 2; MCR p.2].
- Fix the policies the rulebook flagged: duration/padding (44 pairs), container conversion (39), resampling (27), lead selection (10), calibration review (5), preprocessing review (3) [MCR p.6].
- Per-source preprocessing must keep the native rate, target rate, original duration and padding mask. Never overwrite originals (P2, P3) [MCR p.6].
- **Deliverable:** `input_spec.json` (ASSUMPTION: name), versioned per V4.

### Step 4: Label-readiness table

- For each record, link the original label and ECG timing to supporting evidence for review with the clinical supervisor. Preserve uncertain and unresolved cases [MCR p.10 item 3; MCR p.8].
- Apply the code-level mapping rules in §2 below. The output contains only `candidate`, `unresolved` and `excluded` statuses. `confirmed` comes only from step 5.
- **Deliverable:** `label_readiness_<source>.parquet` with the schema in §2.1.

### Step 5: Clinical label review

- The data analyst and clinical supervisor agree how acute STEMI, NSTEMI and non-MI are established (L7) [CMP p.5 step 3].
- The reviewer works through the `candidate` queue and writes decision records. Only these records promote a label to `confirmed` (L13, ASSUMPTION).
- **Deliverable:** `review_decisions.csv` (append-only) and the reference-standard definition document.

### Step 6: Leakage controls and patient-level splits

- Group repeated ECGs by patient where defensible, document encounter linkage, and review alternate resolutions, original/challenge exports and derivative datasets (S1–S3, O1–O8) [MCR p.10 item 4; CMP p.5 step 4].
- Build the split manifest per S7–S9 (ASSUMPTION details).
- Automated audit: assert zero patient-key intersection across splits, zero `overlap_group` straddling a cross-source boundary (O11), and that PTB-XL `records100` never appears (O2).
- **Deliverable:** `splits_<version>.csv` and `split_audit_<version>.json`.

### Step 7: Per-source decision record

- For each source, record suitable / needs further checks / left out, with a reason, and keep track of conversions (E4) [CMP p.5 step 5].
- Record the pretraining role separately from the supervised role (L11) [MCR p.8; NB p.33].
- **Deliverable:** `source_decisions.csv`.

### Step 8: Freeze the comparison protocol

- Once labels and inclusion are reviewed, compare hierarchical (MI vs non-MI → STEMI vs NSTEMI) and flat three-class models on the **same** eligible cohort, splits and input specification (S4) [MCR p.2; MCR p.10 item 5].
- Plan source-specific results and external validation (S5) [MCR p.10 item 5].
- ASSUMPTION (not in PDFs): the primary metrics are per-class sensitivity/specificity, macro-F1 and AUROC with patient-level bootstrap CIs. For the hierarchical model, report stage-wise and end-to-end performance. Thresholds are chosen on validation only.
- **Gate:** no model training before steps 4–7 are signed off. This follows from "no source is approved for supervised acute three-class training" [NB p.24; MCR p.1].

### Step 9: Reporting

- Describe the upstream work as a documentary and optional metadata feasibility assessment. Report edition, input target, evidence coverage, rules, sample scope and clustering sensitivity [NB p.25].
- Do not claim that the notebook validates acute MI labels or model performance [NB p.25; NB p.33].

## 2. Code-level label mapping rules

These rules turn source annotations into the contract's label-status vocabulary (data_contract §3.2). They implement the hard rules L1–L12. Wherever a rule needs a concrete code list, the PDFs give none, so those lists are **BG-UNCONFIRMED** placeholders that the clinical supervisor must approve before use.

### 2.1 Output schema (one row per ECG)

| Column | Type | Rule / source |
|---|---|---|
| `dataset_id` | str | Engine key from data_contract §2.1 [NB p.11–13] |
| `release` | str | Exact release string (V1) [MCR p.3; NB p.9] |
| `record_id` | str | `ecg_id` / `study_id` / `exam_id` / file stem [MCR p.9] |
| `patient_key` | str \| null | §4 table in data_contract [MCR p.9] |
| `patient_key_quality` | enum `native`, `record_proxy` | S7 (ASSUMPTION) |
| `overlap_group` | str | O11 (ASSUMPTION) |
| `original_label` | str (verbatim, never edited) | L5 [MCR p.8] |
| `label_source` | enum `scp_statement`, `machine_text`, `snomed`, `aha_statement`, `rhythm_label`, `beat_annotation`, `linked_clinical`, `header_comment`, `none` | L5 [MCR p.8]. The category names are an ASSUMPTION. |
| `ecg_time` | datetime \| null | L5 [MCR p.8] |
| `supporting_evidence` | json \| null | L5 [MCR p.8] |
| `status` | enum `confirmed`, `candidate`, `unresolved`, `excluded` | data_contract §3.2 (ASSUMPTION semantics) |
| `proposed_class` | enum `STEMI`, `NSTEMI`, `non-MI`, `MI_unspecified` \| null | Set for `candidate` only |
| `final_class` | enum `STEMI`, `NSTEMI`, `non-MI` \| null | Set **only** when `status == confirmed` |
| `exclusion_reason` | str \| null | Required when `status == excluded` (E4) |
| `pretraining_eligible` | bool | L11 [MCR p.8] |
| `rule_id` | str | Which mapping rule (M1–M12) produced the row |
| `reviewer`, `review_date` | str \| null | E1 [NB p.10; MCR p.10] |
| `contract_version`, `mapping_version` | str | V4 (ASSUMPTION) |

### 2.2 Mapping rules (evaluated in order, first match wins)

| ID | Condition | Result | Basis |
|---|---|---|---|
| **M0** | Every row starts at this default | `status=unresolved`, `final_class=null` | L6 [MCR p.10]; ASSUMPTION for the default |
| **M1** | A review decision exists for this record in `review_decisions.csv` | Apply the reviewer's status and `final_class`. This is the **only** path to `confirmed`. | L5, L7 [MCR p.8; CMP p.5]; L13 ASSUMPTION |
| **M2** | Record fails a technical exclusion (e.g. non-reducible lead set, Holter context for supervised use) | `status=excluded`, `exclusion_reason=<code>` | E4 [CMP p.5]; INCART [MCR p.8] |
| **M3** | Duplicate representation (PTB-XL `records100`) | Drop the row entirely, not `excluded` | O2 [MCR p.3; NB p.14] |
| **M4** | `label_source == none` or no MI-related code present | `status=unresolved`. **Never** `non-MI`. | L1 [MCR p.8; CMP p.5; NB p.23] |
| **M5** | `label_source == machine_text` | `status=unresolved`. Text is kept in `original_label` for reviewers only. | L2 [MCR p.8]; L4 [NB p.23] |
| **M6** | `label_source == rhythm_label` or `beat_annotation` | `status=unresolved`, `pretraining_eligible` determined separately | L2 [MCR p.8]; INCART `.atr` [MCR p.9]; CODE [NB p.23] |
| **M7** | Code is in the reviewer-approved **ST/T-change / injury** list | `status=candidate`, `proposed_class=MI_unspecified` | L2 forbids auto-conversion to STEMI [MCR p.8]; candidate semantics are an ASSUMPTION |
| **M8** | Code is in the reviewer-approved **MI statement** list (PTB-XL SCP, SNOMED, AHA) | `status=candidate`, `proposed_class=MI_unspecified` | L2, L3 [MCR p.8; CMP p.4]; L4 [NB p.23] |
| **M9** | `label_source == linked_clinical` with an explicit STEMI or NSTEMI diagnosis and an ECG time inside the acute window | `status=candidate`, `proposed_class=STEMI` or `NSTEMI` | L5 timing [MCR p.8]. Linkage source is BG-UNCONFIRMED; the window is Q2. |
| **M10** | `label_source == linked_clinical` with documented positive evidence of no acute MI | `status=candidate`, `proposed_class=non-MI` | L14 (ASSUMPTION); Q4 |
| **M11** | Conflicting codes within one record (e.g. MI statement plus a contradicting linked diagnosis) | `status=unresolved`, `rule_id=M11`, conflict noted in `supporting_evidence` | L6 [MCR p.10] |
| **M12** | Dataset has no verified target-label source at all | Rows stay `unresolved`; `pretraining_eligible` may be set after technical/access review | L11 [MCR p.8; NB p.33] |

Invariants the code must enforce (unit-tested):

1. `final_class` is non-null **iff** `status == confirmed`, and `confirmed` rows always have `rule_id == M1` and a non-null `reviewer`. (Implements L5/L7.)
2. No row has `final_class == non-MI` unless `rule_id == M1`. (Implements L1.)
3. No row created by M5–M8 has `proposed_class ∈ {STEMI, NSTEMI}`. (Implements L2/L3.)
4. `original_label` is byte-identical to the source field. (Implements L5, P3.)
5. Only `status == confirmed` rows reach the supervised train/val/test loaders. All rows are allowed in the pretraining loader if `pretraining_eligible`. (Implements L11; ASSUMPTION for loader design.)
6. Every `excluded` row has a non-empty `exclusion_reason`. (Implements E4.)

### 2.3 Reference implementation sketch

ASSUMPTION: Python 3 with pandas. The function and constant names are proposals.

```python
# label_mapping.py  (sketch; code lists are BG-UNCONFIRMED placeholders)
MAPPING_VERSION = "0.1.0"

# Must be filled from a reviewer-approved file; empty until clinical sign-off (L4, L7).
APPROVED_MI_STATEMENT_CODES: dict[str, set[str]] = {}   # e.g. {"ptb_xl": {...}, "sph": {...}}
APPROVED_ST_INJURY_CODES:    dict[str, set[str]] = {}
ACUTE_WINDOW = None                                      # open question Q2

def map_record(rec, review=None, technical_exclusion=None):
    row = dict(rec, status="unresolved", proposed_class=None, final_class=None,
               exclusion_reason=None, rule_id="M0")                         # M0
    if review is not None:                                                   # M1
        return {**row, **review.as_label_fields(), "rule_id": "M1"}
    if technical_exclusion:                                                  # M2
        return {**row, "status": "excluded",
                "exclusion_reason": technical_exclusion, "rule_id": "M2"}
    src, codes = rec["label_source"], set(rec["codes"])
    if src == "none" or not codes:                                           # M4: never non-MI
        return {**row, "rule_id": "M4"}
    if src == "machine_text":                                                # M5
        return {**row, "rule_id": "M5"}
    if src in ("rhythm_label", "beat_annotation"):                           # M6
        return {**row, "rule_id": "M6"}
    ds = rec["dataset_id"]
    if src == "linked_clinical":                                             # M9/M10/M11
        return map_linked_clinical(row, rec, ACUTE_WINDOW)
    mi_hit = codes & APPROVED_MI_STATEMENT_CODES.get(ds, set())
    st_hit = codes & APPROVED_ST_INJURY_CODES.get(ds, set())
    if mi_hit or st_hit:                                                     # M7/M8
        return {**row, "status": "candidate", "proposed_class": "MI_unspecified",
                "rule_id": "M8" if mi_hit else "M7"}
    return {**row, "rule_id": "M4"}
```

`map_linked_clinical` returns `unresolved` while `ACUTE_WINDOW is None`, so M9/M10 cannot fire until Q2 is answered.

### 2.4 Per-source extraction notes for the mapper

| ID | Field(s) to read into `original_label` / `codes` | Status of that knowledge |
|---|---|---|
| `ptb_xl` | `ptbxl_database.csv` statement column, decoded via `scp_statements.csv` | Files [MCR p.9]. Column name `scp_codes` and its dict-of-likelihood format are BG-UNCONFIRMED. |
| `mimic_iv_ecg` | `machine_measurements.csv` report text → M5 only; `waveform_note_links.csv` for note linkage | Files [NB p.14–15]. Diagnosis/troponin linkage to MIMIC-IV clinical modules is BG-UNCONFIRMED (Q3). |
| `sph` | `metadata.csv` + `code.csv` AHA statements | Files [MCR p.9]; AHA review [MCR p.8]. Code semantics are BG-UNCONFIRMED. |
| Challenge sources | `.hea` header comment lines (SNOMED `Dx`) | `.hea`/`.mat` layout [MCR p.9]. `#Dx:` header convention is BG-UNCONFIRMED. |
| `code15` | `exams.csv` label columns, joined on `exam_id` | Join rule [MCR p.9]. Label column names and the absence of an MI class are BG-UNCONFIRMED. |
| `ptb_diagnostic` | `.hea` header comments | Layout [MCR p.9]. "Reason for admission" field is BG-UNCONFIRMED. |
| `incart` | `.atr` beat annotations → M6 | [MCR p.9; NB p.16] |

## 3. Test strategy (no real data)

- ASSUMPTION: unit tests use synthetic fixtures that reproduce the documented directory layouts and keys [MCR p.9; NB p.14–16]. These cover PTB-XL csv + `records500`/`records100`, MIMIC `files/p…/s…`, CODE HDF5 with padding, and PTB Diagnostic 15-lead.
- Required tests:
  - every invariant in §2.2
  - split audit (step 6)
  - `records100` exclusion (M3/O2)
  - CODE `exam_id` join vs row-order mismatch (C2.2)
  - PTB Diagnostic 15→12 lead selection (C2.3)

## 4. Open questions

These come on top of `data_contract.md` §9 Q1–Q12, which also block this plan.

1. Which plan step is the first deliverable for the team: step 1 (header validation code against fixtures) or step 4 (label mapper)?
2. Will a clinical supervisor sign off the approved code lists for M7/M8? Until then both lists stay empty and every record maps to `unresolved`/`excluded`, so there are no `candidate` rows yet.
3. Is the project allowed to build linkage code for MIMIC-IV clinical data (M9/M10) before access is confirmed?
4. Should `MI_unspecified` candidates that a reviewer cannot subtype become `excluded` or stay `unresolved`?
5. Are the evaluation metrics in step 8 (ASSUMPTION) acceptable, and which source, if any, is held out for external validation?
6. Should pretraining on unlabeled sources (L11) be part of this study or deferred?
