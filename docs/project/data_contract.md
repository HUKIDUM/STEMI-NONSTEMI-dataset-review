# Data Contract: Acute STEMI / NSTEMI / non-MI ECG Research

| Field | Value |
|---|---|
| Contract version | 0.1.0-draft (ASSUMPTION: semantic versioning, see §8) |
| Status | DRAFT, not yet reviewed by the clinical supervisor or AI developer |
| Drafted | 2026-10-19 |
| Evidence base | Only the three PDFs in `19-oct-2026/`. No dataset files were downloaded or opened. |

## 0. Sources and citation key

Every rule cites a PDF page. Page numbers are the printed PDF page numbers.

| Key | File | Pages |
|---|---|---|
| **CMP** | `19-oct-2026/ECG_Dataset_Comparison_Simple_Report.pdf` (report date 16 Oct 2026) | 6 |
| **MCR** | `19-oct-2026/ECG_Metadata_Compatibility_Report.pdf` (analysis date 10 Oct 2026) | 11 |
| **NB** | `19-oct-2026/MI_Metadata_Compatibility_Colab.ipynb - Colab.pdf` (executed export, 10 Oct 2026) | 34 |

Tags used in this file:

- **[CMP p.N] / [MCR p.N] / [NB p.N]**: the PDF states this.
- **ASSUMPTION**: a working decision proposed here. The PDFs neither state nor contradict it. It needs sign-off.
- **BG-UNCONFIRMED**: background knowledge about a dataset that the PDFs do **not** confirm. Verify it against the publisher documentation before relying on it.

Scope limit: the underlying evidence is documentary. No ECG arrays and no local dataset files were inspected, and the optional metadata, header and HDF5 checks were skipped [MCR p.1; MCR p.11; NB p.28; NB p.30; NB p.31]. Every technical value below describes a *documented release*, not observed files [CMP p.2; MCR p.3].

---

## 1. Research target

- **C1.1** The task is to classify an ECG as acute STEMI, NSTEMI or non-MI [CMP p.1; NB p.1].
- **C1.2** Two model designs will be compared: (a) a hierarchical MI vs non-MI model followed by STEMI vs NSTEMI, and (b) a flat three-class model [MCR p.2].
- **C1.3** Provisional model input: standard 12 leads, 10 s, 500 Hz. This is a study setting, "not proof of the best input" [CMP p.5; MCR p.2; NB p.1]. The AI developer must propose the final lead order, units, rate and length [CMP p.5 step 2].
- **C1.4** A shared sampling rate alone does not justify pooling sources [NB p.1; CMP p.4].

## 2. Datasets in scope

### 2.1 Registered releases

Values are publisher-level registry entries, not measured inventories [MCR p.3].

| ID (code key) | Dataset | Release / edition | ECGs (publisher) | Hz | Leads | Duration s | Container | Source ref |
|---|---|---|---|---|---|---|---|---|
| `ptb_xl` | PTB-XL | 1.0.3, records500 | 21,799 | 500 | 12 | 10 | WFDB-DAT | [MCR p.3; NB p.10] |
| `mimic_iv_ecg` | MIMIC-IV-ECG | 1.0 | 800,035 | 500 | 12 | 10 | WFDB-DAT | [MCR p.3; NB p.10] |
| `ningbo` | Ningbo | Challenge 2021 / 1.0.3 | 34,905 | 500 | 12 | 10 | WFDB-MAT | [MCR p.3; NB p.10] |
| `chapman_shaoxing` | Chapman-Shaoxing | Challenge 2021 / 1.0.3 | 10,247 | 500 | 12 | 10 | WFDB-MAT | [MCR p.3; NB p.10] |
| `georgia` | Georgia 12-lead | Challenge 2021 / 1.0.3 | 10,344 | 500 | 12 | 5–10 | WFDB-MAT | [MCR p.3; NB p.10] |
| `cpsc_2018` | CPSC 2018 | Challenge 2021 / 1.0.3 | 6,877 | 500 | 12 | 6–144* | WFDB-MAT | [MCR p.3; NB p.10] |
| `cpsc_extra` | CPSC-Extra | Challenge 2021 / 1.0.3 | 3,453 | 500 | 12 | 6–144* | WFDB-MAT | [MCR p.3; NB p.16] |
| `sph` | Shandong Provincial Hospital | Figshare collection 5779802 v1 | 25,770 | 500 | 12 | 10–60 | HDF5-record | [MCR p.3; NB p.15–16] |
| `ptb_diagnostic` | PTB Diagnostic | 1.0.0 native | 549 | 1000 | 15 | Unknown | WFDB-DAT | [MCR p.3; NB p.16] |
| `incart` | INCART | 1.0.0 native | 75 | 257 | 12 | 1800 (Holter) | WFDB-DAT | [MCR p.3; CMP p.3] |
| `code15` | CODE-15% | Zenodo 4916206 | 345,779 | 400 | 12 | 7–10 (stored padded to 4096 samples) | HDF5-shard | [MCR p.3; NB p.16] |

\* The CPSC 6–144 s range describes the combined source, not each subset [MCR p.3; NB p.15].

Dataset IDs are the engine keys printed in the notebook output [NB p.11–13]. Code must use these exact strings.

### 2.2 Known technical facts that bind the loader

- **C2.1** PTB-XL: use `records500`. The `records100` copies are another representation of the same ECGs and must not be counted as extra ECGs [MCR p.3; MCR p.9; NB p.14].
- **C2.2** CODE-15%: `tracings` has shape N × 4096 × 12. 4096 / 400 Hz = 10.24 s is the *stored* length including padding, not observed ECG duration [MCR p.3; NB p.16]. Join on `exam_id`, never on row position [MCR p.9]. Amplitude calibration is unresolved [NB p.16].
- **C2.3** PTB Diagnostic has 15 channels (standard 12 + Frank X/Y/Z). Select the standard 12 and plan a 1000→500 Hz conversion [MCR p.8; MCR p.9]. Its duration is unresolved [MCR p.3].
- **C2.4** Challenge `.mat` files store `val` as leads × samples [MCR p.9; NB p.15].
- **C2.5** SPH arrays are leads × variable samples [MCR p.9; NB p.16].
- **C2.6** MIMIC `cart_id` is not a device manufacturer or model [MCR p.3; MCR p.9; NB p.15; NB p.27]. Raw MIMIC filter strings must not be read as numeric cutoff frequencies [NB p.27].
- **C2.7** Do not infer collection years from challenge names, publication years or shifted patient timestamps [MCR p.3; NB p.15]. Documented periods: PTB-XL 1989–1996, MIMIC-IV-ECG 2008–2019, SPH 2019–2020, CODE-15% 2010–2016 [MCR p.3].
- **C2.8** Documented equipment: PTB-XL Schiller AG; MIMIC Burdick/Spacelabs, Philips, GE; SPH MedEx MECG-200; PTB Diagnostic a non-commercial PTB prototype; the rest are unknown [MCR p.3; NB p.10]. A brand alone does not prove equal acquisition settings [MCR p.3]. "GE MUSE is not proof of an acquisition model" (Ningbo, Chapman) [NB p.15].
- **C2.9** MIMIC physical units and calibration are unresolved in the registry. That does not mean the files lack them [CMP p.4; MCR p.6].

### 2.3 Technical disposition (as of 10 Oct 2026)

Source: `target_readiness.csv` as reported in [MCR p.8]. "Candidate" means only that the selected technical blockers did not trigger. It is **not** approval for training [MCR p.8].

| ID | Technical status | Required before use | Ref |
|---|---|---|---|
| `ptb_xl` | Candidate | Check acquisition gaps; review acute timing and subtype evidence | [MCR p.8] |
| `mimic_iv_ecg` | Hold | Verify amplitude calibration; review clinical linkage and adjudication | [MCR p.8] |
| `ningbo` | Hold | Verify calibration and acquisition details; review label meaning | [MCR p.8] |
| `chapman_shaoxing` | Hold | Verify calibration; distinguish original and challenge exports | [MCR p.8] |
| `georgia` | Hold | Verify calibration and 5–10 s window policy; review patient linkage | [MCR p.8] |
| `cpsc_2018` | Hold | Verify calibration; define variable-duration policy | [MCR p.8] |
| `cpsc_extra` | Hold | As CPSC 2018; review overlap with related CPSC exports | [MCR p.8] |
| `sph` | Candidate | Define duration policy; review AHA statements and acquisition gaps | [MCR p.8] |
| `ptb_diagnostic` | Candidate | Select standard 12 leads; plan 1000→500 Hz; verify duration | [MCR p.8] |
| `incart` | Hold | Review Holter domain and window-level eligibility before inclusion | [MCR p.8] |
| `code15` | Hold | Verify amplitude scale, padding interpretation and target-label availability | [MCR p.8] |

- **C2.10** All 55 pairwise compatibility ratings (3 Low, 42 Moderate, 10 High) are **unconfirmed** [CMP p.1; MCR p.1]. Low does not grant permission to pool, and High is not automatic exclusion [CMP p.1; NB p.11].
- **C2.11** No dataset pair is confirmed ready for pooled acute three-class supervised training [MCR p.1; NB p.24].
- **C2.12** First pair to investigate: PTB-XL + MIMIC-IV-ECG. It is rated Moderate with 50% technical evidence coverage, because data from both are already being collected for the project [CMP p.4; MCR p.6]. That is a proposal for review, not approval to combine [CMP p.4].
- **C2.13** An unknown attribute is an evidence gap, not proof of absence [MCR p.2; MCR p.5]. A supervisor-reviewed protocol must say how unknowns affect inclusion; unknowns are not permanent exclusions by default [MCR p.5].

## 3. Label rules

### 3.1 Hard rules (stated by the PDFs)

- **L1** Absence of an MI code or annotation must **never** create a non-MI label [MCR p.8; CMP p.5 step 3; NB p.23].
- **L2** Broad MI statements, machine interpretation text, ST/T-change labels and rhythm codes are **not** converted to acute STEMI or NSTEMI outcomes [MCR p.8].
- **L3** A general MI annotation does not supply the acute subtype the project needs [CMP p.4].
- **L4** The following label sources need separate clinical review before use: PTB-XL MI statements, machine interpretation text, AHA/SNOMED codes, and CODE rhythm labels [NB p.23].
- **L5** For every proposed target label, retain: the original label, its source, ECG timing, supporting clinical evidence, and the reviewer decision [MCR p.8].
- **L6** Uncertain and unresolved cases are preserved. They are not forced into one of the three classes [MCR p.10 item 3].
- **L7** The data analyst and clinical supervisor must agree how acute STEMI, NSTEMI and non-MI labels are established [CMP p.5 step 3].
- **L8** Technical readiness and clinical label validity are separate requirements. Passing one does not satisfy the other [MCR p.1; MCR p.6; CMP p.4; NB p.24].
- **L9** All eleven sources currently have **unverified** acute three-class labels [MCR p.8]. No STEMI/NSTEMI/non-MI labels were generated by the analysis [NB p.24].
- **L10** Registry or evidence edits never verify clinical outcome labels [NB p.10].
- **L11** A source without verified target labels may be considered for **pretraining** after technical and access review. That role must be recorded separately from supervised acute-MI training and from external clinical validation [MCR p.8; NB p.33].
- **L12** Final inclusion decisions belong in a reviewed study protocol [MCR p.8].

### 3.2 Label status vocabulary

The four statuses come from the user's brief. The PDFs mandate the *distinction* between verified and unresolved labels (L5, L6, L9) but do not define these exact four terms. Their precise semantics are therefore an **ASSUMPTION**, built to satisfy L1–L12.

| Status | Meaning | Who may assign it | May enter supervised train/test? |
|---|---|---|---|
| `confirmed` | One of {STEMI, NSTEMI, non-MI} with acute timing and supporting clinical evidence, and a recorded reviewer decision (L5, L7) | Clinical supervisor via review record only. Code never assigns it on its own. | Yes, once the protocol is frozen (L12) |
| `candidate` | Source evidence suggests a target class (e.g. an MI-related statement) but review is pending. Stores a `proposed_class`. | Mapping code | **No.** Review queue only. |
| `unresolved` | No usable evidence for any class, conflicting evidence, or missing timing. **The default.** Covers "no MI code" (L1). | Mapping code (default) | No |
| `excluded` | Deliberately removed from the task with a recorded `exclusion_reason` (e.g. Holter context, non-standard leads that cannot be reduced, reviewer rejected) | Mapping code (technical reasons) or reviewer | No (pretraining eligibility is tracked separately, L11) |

- **L13 (ASSUMPTION)** Status transitions allowed: `unresolved → candidate → confirmed | unresolved | excluded`, and `any → excluded`. Only a review record can move a label to `confirmed`. Every transition is logged with reviewer and date (consistent with [MCR p.10 item 2] provenance fields).
- **L14 (ASSUMPTION)** `non-MI` can only be `confirmed` from positive evidence of no acute MI (e.g. a reviewer-documented alternative diagnosis or adjudicated negative work-up). It can never come from the absence of a code (L1). What counts as positive evidence is open question Q4.

### 3.3 Per-source label notes

| ID | What the PDFs say about labels | What is NOT confirmed |
|---|---|---|
| `ptb_xl` | MI statements need clinical review; acute timing and subtype evidence must be reviewed [NB p.23; MCR p.8]. Metadata tables: `ptbxl_database.csv`, `scp_statements.csv` [MCR p.9]. | BG-UNCONFIRMED: SCP-ECG statement codes include MI-location codes (e.g. AMI, IMI, ASMI…) and ST-injury codes (INJAS, INJIN…). These are ECG-report statements, not adjudicated acute STEMI/NSTEMI outcomes, and they likely include old/chronic MI. |
| `mimic_iv_ecg` | Clinical linkage and adjudication need review [MCR p.8]. Files include `machine_measurements.csv`, `waveform_note_links.csv` [NB p.14–15]. Machine text is not a label source (L2). | BG-UNCONFIRMED: acute MI subtype might be derived by linking `subject_id` and ECG time to MIMIC-IV hospital diagnoses (e.g. ICD-10 I21.x) and/or troponin. That needs separate credentialed access to MIMIC-IV clinical modules. |
| `sph` | AHA statements need review [MCR p.8; NB p.23]. Files `metadata.csv`, `code.csv` [MCR p.9]. | BG-UNCONFIRMED: which AHA statement codes, if any, encode acute MI. |
| Challenge sources (`ningbo`, `chapman_shaoxing`, `georgia`, `cpsc_*`) | Label meaning must be reviewed (Ningbo) [MCR p.8]. SNOMED codes need clinical review [NB p.23]. | BG-UNCONFIRMED: challenge labels are SNOMED CT rhythm/morphology codes. Any MI codes present are unlikely to give acute subtype or timing. |
| `code15` | Target-label availability must be verified [MCR p.8]. Rhythm labels need clinical review [NB p.23]. | BG-UNCONFIRMED: CODE-15% labels are a small set of rhythm/conduction abnormalities with no MI class. If that holds, the source would serve only as a pretraining candidate (L11). |
| `ptb_diagnostic` | No label statement in PDFs beyond the general rules. | BG-UNCONFIRMED: header comments include a "reason for admission" field (e.g. myocardial infarction) and sometimes infarction age/location. |
| `incart` | `.atr` stores **beat** annotations [MCR p.9; NB p.16]. Holter context [CMP p.3]. | Beat annotations are not acute-MI outcome labels. The source is treated as pretraining-only or `excluded` for supervised training until Q8 is answered (ASSUMPTION). |

## 4. Patient-level split rules

- **S1** Identify repeated patients and overlapping records. Where patient identifiers allow it, keep each patient in exactly one split [CMP p.5 step 4; MCR p.10 item 4].
- **S2** Keep patients **and overlapping exports** separated across train/test splits [NB p.25].
- **S3** Document encounter linkage [MCR p.10 item 4]. Pairs stay provisional until patient/encounter linkage is reviewed [MCR p.6].
- **S4** Hierarchical and flat models must be compared on the **same** eligible cohort, the same patient splits and the same input specification [MCR p.10 item 5].
- **S5** Plan source-specific results and external validation with the AI team [MCR p.10 item 5].
- **S6** Train/test independence cannot be concluded from the current outputs [MCR p.10]. It must be shown by the split audit (see `research_plan.md` step 6).

Documented patient-grouping keys:

| ID | Grouping key | Ref |
|---|---|---|
| `ptb_xl` | `patient_id` (ECG key `ecg_id`, file `filename_hr`) | [MCR p.9] |
| `mimic_iv_ecg` | `subject_id` (ECG key `study_id`) | [MCR p.9] |
| `sph` | `Patient_ID` | [MCR p.9] |
| `ptb_diagnostic` | patient folder (e.g. `patient001/`) | [MCR p.9] |
| `code15` | Not given in PDFs (only `exam_id`) | BG-UNCONFIRMED: `exams.csv` has a `patient_id` column |
| `georgia` | Not given; patient linkage must be reviewed | [MCR p.8] |
| `ningbo`, `chapman_shaoxing`, `cpsc_2018`, `cpsc_extra`, `incart` | Not given in PDFs | BG-UNCONFIRMED: no patient ID is believed to be released |

- **S7 (ASSUMPTION)** If a source has no patient key, assign a split unit of `record_id` and set `patient_key_quality = "record_proxy"`. Such a source may not be used for the held-out test set of the primary comparison until Q6 is resolved.
- **S8 (ASSUMPTION)** Splits are generated once, with a fixed seed, at the patient level (grouped and stratified on the confirmed class where possible), then frozen in a versioned split manifest (§8). The ratio (e.g. 70/15/15) is open question Q10.
- **S9 (ASSUMPTION)** The split is assigned **before** any label is used for model selection, and `candidate`/`unresolved` records do not affect which patient lands in which split.

## 5. Cross-release overlap rules

- **O1** Related releases need an overlap review before datasets or splits are pooled [MCR p.3].
- **O2** PTB-XL 100 Hz and 500 Hz representations are the same ECGs. Count once [MCR p.3; NB p.14].
- **O3** INCART: native 1.0.0 has 75 records; the Challenge subset has 74. Never mix editions silently [MCR p.3; NB p.9].
- **O4** Ningbo and Chapman-Shaoxing also appear together in a combined export. Distinguish original and challenge exports [MCR p.3; MCR p.8].
- **O5** CPSC-Extra must be reviewed for overlap with related CPSC exports [MCR p.8].
- **O6** Review alternate resolutions, original/challenge exports and derivative datasets for overlap [MCR p.10 item 4].
- **O7** Native and challenge editions must remain distinguishable in every table [MCR p.3]. Always report the exact release [NB p.9].
- **O8** A historical PTB-XL count of 21,837 differs from release 1.0.3 (21,799). Counts from an earlier screenshot must not be mixed with 1.0.3 [NB p.9; NB p.14].
- **O9** No waveform hashes or near-duplicate signal detection have been done [NB p.25], and signal duplicates were not assessed [MCR p.10]. Overlap is therefore **unknown**, not absent.
- **O10 (BG-UNCONFIRMED)** Possible further overlaps that the PDFs do not mention: (a) PTB-XL is also redistributed inside the PhysioNet Challenge 2021 set; (b) PTB Diagnostic is also in the Challenge 2021 set; (c) the CODE-15% subset relates to the larger CODE cohort. If confirmed, each needs an O1 review.
- **O11 (ASSUMPTION)** Until reviewed, any two sources from the same originating institution or the same challenge distribution share an `overlap_group` and are placed together on one side of any cross-source train/test boundary.

## 6. Signal representation and preservation

- **P1** Agree, before implementation: lead names and order, physical units with verified conversion, target frequency, window and padding policy, patient grouping, inclusion rules, reviewed labels, and source-version identifiers [MCR p.9].
- **P2** Retain per record: source identifiers, release version, patient grouping, native rate, target rate, original duration and any padding mask [MCR p.6].
- **P3** Record each transformation with its justification. Never overwrite original files [MCR p.6; CMP p.5 step 5].
- **P4** Lead names and order must be confirmed per source. Order matters, not just count [CMP p.2; CMP p.4].
- **P5** Original acquisition frequency, released frequency and filter cutoff frequencies are different attributes and stay in separate fields [NB p.9].
- **P6 (ASSUMPTION)** Canonical lead order for the model tensor is `I, II, III, aVR, aVL, aVF, V1, V2, V3, V4, V5, V6`, with units in mV. The PDFs do not fix this (see C1.3 and Q9).

## 7. Evidence and decision records

- **E1** Each resolved attribute must carry: a typed value, exact source URL and locator, reviewer and review date. Release and scope stay unchanged [NB p.10; MCR p.10 item 2].
- **E2** A single sampled header cannot establish a fact about a whole release [NB p.10; MCR p.10 item 2].
- **E3** Local observations (CSV summaries, header checks, HDF5 schema) are separate artifacts. They never silently replace documentary facts or certify a full download [NB p.25; NB p.29]. Prefix previews and convenience samples must be labeled as such [MCR p.10 item 1; NB p.27].
- **E4** For each source, record whether it is suitable for the task, needs further checks, or is left out, with a reason [CMP p.5 step 5].
- **E5** Keep unresolved choices in an issue log with evidence source, proposed owner and decision status [MCR p.9].

## 8. Versioning

- **V1** Every dataset reference uses the exact release string from §2.1 [MCR p.3; NB p.9].
- **V2** The upstream assessment is pinned as: run `metadata_compatibility_v1`, timestamp 10 Oct 2026 09:11:04 UTC, engine 1.0.0, Python 3.13.16, NumPy 2.1.3, pandas 2.2.3, SciPy 1.16.3, Matplotlib 3.10.0, registry curation date 2026-10-10 [MCR p.11; NB p.10; NB p.24]. The registry digest is recorded in `run_provenance.json` [MCR p.11; NB p.24].
- **V3** Results artifacts to keep alongside this contract: `target_specification.json`, `dataset_profiles.csv`, `attribute_evidence.csv`, `pairwise_assessment.csv`, `pairwise_actions.csv`, `target_readiness.csv`, `rulebook.csv`, `run_provenance.json` [MCR p.9]. **Note:** `metadata_compatibility_v1.zip` is referenced by the PDFs but is not in this project folder (Q1).
- **V4 (ASSUMPTION)** This contract uses semantic versioning:
  - MAJOR: a change to label-status semantics, split units or the target class set.
  - MINOR: adding or removing a dataset, or a disposition change.
  - PATCH: wording or citation fixes.

  Each derived artifact (label table, split manifest, preprocessed tensors) records the contract version it was built under.
- **V5 (ASSUMPTION)** Derived artifacts are immutable once written. A change produces a new version tag (e.g. `labels_v0.2.0.parquet`, `splits_v0.2.0.csv`) plus a changelog entry, never an in-place edit (extends P3).

## 9. Open questions

1. Is `metadata_compatibility_v1.zip` (with `target_readiness.csv`, `attribute_evidence.csv`, etc.) available to the team? The PDFs cite it as the evidence base [CMP p.6; MCR p.11], but it is not in this repo.
2. What acute-MI reference standard will the clinical supervisor accept (e.g. adjudicated diagnosis, troponin + ECG criteria, discharge diagnosis), and what time window between ECG and event counts as "acute"? [CMP p.5 step 3; MCR p.8]
3. Does the project have, or intend to request, access to MIMIC-IV clinical modules for diagnosis/troponin linkage? Without it, MIMIC-IV-ECG labels cannot reach `confirmed` (BG-UNCONFIRMED path in §3.3).
4. What counts as positive evidence for a `confirmed` non-MI label (L14)?
5. Should PTB-XL MI statements be allowed to reach `confirmed` at all, given they are report statements without documented acuity [NB p.23; MCR p.8]?
6. For sources without a patient ID (Ningbo, Chapman, Georgia, CPSC, INCART), is a record-level split acceptable for training-only use, or must those sources stay out of evaluation (S7)?
7. Who owns overlap review for the Ningbo/Chapman combined export and the CPSC exports (O4, O5), and what method will be used (ID matching vs signal hashing, O9)?
8. Is INCART in scope at all (Holter, 30-minute recordings) [CMP p.3; MCR p.8], and if so, as windowed pretraining data only?
9. Final input specification: lead order, units, rate, length, and the padding/cropping policy for 5–10 s (Georgia), 6–144 s (CPSC) and 10–60 s (SPH) records [CMP p.5 step 2; MCR p.8; MCR p.6 Fig. 3].
10. Split ratios and whether a whole source is held out for external validation [MCR p.10 item 5].
11. How do unknown technical attributes affect inclusion? The PDFs ask for a supervisor-reviewed rule [MCR p.5].
12. Which PTB Diagnostic duration and subject count apply? The PTB page reports inconsistent subject counts [NB p.16], and duration is unknown [MCR p.3].
