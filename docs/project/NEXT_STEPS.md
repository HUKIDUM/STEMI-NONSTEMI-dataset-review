# Next Steps: review of the previous analysis and plan forward

| Field | Value |
|---|---|
| Author | planner-checker (agent team) |
| Date | 2026-10-19 |
| Evidence | Only the three PDFs in `19-oct-2026/`. No data downloaded, no code run on real data. |
| Built under | `data_contract.md` 0.1.0-draft, `research_plan.md` 0.1.0-draft |

Citation keys (same as `data_contract.md` §0):
**CMP** = `ECG_Dataset_Comparison_Simple_Report.pdf`, **MCR** = `ECG_Metadata_Compatibility_Report.pdf`, **NB** = `MI_Metadata_Compatibility_Colab.ipynb - Colab.pdf`.
**ASSUMPTION** = a proposal that needs sign-off. **BG-UNCONFIRMED** = general background knowledge that the PDFs do **not** state. Check it against the publisher pages before relying on it.

---

## 1. What the previous analysis did (plain language)

**What it was.** On 10 Oct 2026 a Colab notebook compared the *published descriptions* of eleven ECG datasets. It asked one question: how much work would it take to make each pair of datasets look alike (sampling rate, leads, duration, file format, equipment, calibration and so on) before using them together for acute STEMI / NSTEMI / non-MI research [MCR p.2; NB p.1].

**What it did not do.** It opened no ECG signals and no downloaded files. It trained no model. It created no STEMI/NSTEMI/non-MI labels. The optional checks of local metadata, file headers and HDF5 files were all switched off [CMP p.1; MCR p.1; MCR p.11; NB p.24; NB p.28; NB p.30; NB p.31]. The findings therefore describe the documentation, not the files the project holds [MCR p.1].

**How it worked.** A registry stored 38 attributes per dataset, each with a value, an evidence type and a source pointer. Anything not documented was kept as "Unknown" [MCR p.2]. Rules then rated each of the 55 dataset pairs as Low, Moderate or High preparation effort. Any missing evidence made the rating "unconfirmed" (shown as "?") [MCR p.2; NB p.11].

**What it found.**

- **55 pairs:** 3 Low, 42 Moderate, 10 High, and **all 55 unconfirmed** [CMP p.1; MCR p.1].
  - The Low pairs are PTB-XL–Ningbo, PTB-XL–Chapman and Ningbo–Chapman [CMP p.3; MCR p.4].
  - All 10 High pairs involve INCART, because it is a 30-minute Holter recording rather than a diagnostic ECG [CMP p.3; MCR p.4].
- **Missing information:** 195 of 418 registry entries were documented and 223 (53.3%) were unknown [CMP p.4; MCR p.5]. Mean pairwise technical coverage was 42.5% [MCR p.5]. Device model, firmware, filter, electrode placement and simultaneity were rarely documented [MCR p.5].
- **Preparation work most often needed:**

  | Rule | Pairs |
  |---|---|
  | Duration/padding policy | 44 |
  | Container conversion | 39 |
  | Resampling | 27 |
  | Device review | 13 |
  | Lead selection | 10 |
  | Recording-context review | 10 |
  | Calibration review | 5 |
  | Preprocessing review | 3 |

  Source: [MCR p.6].
- **Per-dataset readiness:** 3 technical "Candidates" (PTB-XL, SPH, PTB Diagnostic) and 8 on "Hold". Candidate means only that no selected technical blocker triggered. It is *not* approval for training [MCR p.8].
- **Labels:** all eleven sources have **unverified** acute three-class labels. No dataset pair is ready for pooled supervised training [MCR p.1; MCR p.8; NB p.24].
- **Suggested first pair:** PTB-XL + MIMIC-IV-ECG, because data from both are already being collected for the project. The pair is rated Moderate with 50% technical coverage (8 of 16 attributes known for both). This is a proposal to investigate, not approval to combine them [CMP p.4; MCR p.6].

**Bottom line.** The analysis supports planning and a shortlist. It does not support training a pooled model yet [MCR p.10].

---

## 2. Data sources

Size = publisher ECG count, not a count of local files [MCR p.3]. Status = technical disposition from `target_readiness.csv` [MCR p.8]. Countries are **not stated in the PDFs**; the country column is BG-UNCONFIRMED throughout.

| Dataset (engine key) | Where it comes from: what the PDFs say | Country (BG-UNCONFIRMED) | Years [MCR p.3] | Device [MCR p.3; NB p.10] | Size (ECGs) | Labels available | Status |
|---|---|---|---|---|---|---|---|
| PTB-XL (`ptb_xl`), 1.0.3 records500 | PhysioNet, physionet.org/content/ptb-xl/1.0.3 [MCR p.11] | Germany | 1989–1996 | Schiller AG | 21,799 | SCP-ECG report statements in `ptbxl_database.csv` / `scp_statements.csv`; need clinical review for acute timing and subtype [MCR p.8–9; NB p.23] | **Candidate** |
| MIMIC-IV-ECG (`mimic_iv_ecg`), 1.0 | PhysioNet, physionet.org/content/mimic-iv-ecg/1.0 [MCR p.11] | USA | 2008–2019 | Burdick/Spacelabs; Philips; GE | 800,035 | Machine measurements and report text (not a label source, L2), plus note links [NB p.14–15]; needs clinical linkage and adjudication [MCR p.8] | Hold |
| Ningbo (`ningbo`), Challenge 2021 / 1.0.3 | PhysioNet Challenge 2021 distribution; source history at physionet.org/content/ecg-arrhythmia/1.0.0 [MCR p.11] | China | Unknown | Unknown ("GE MUSE is not proof of an acquisition model" [NB p.15]) | 34,905 | SNOMED codes in headers; need clinical review; "review label meaning" [MCR p.8; NB p.23] | Hold |
| Chapman-Shaoxing (`chapman_shaoxing`), Challenge 2021 / 1.0.3 | As Ningbo [MCR p.11] | China | Unknown | Unknown | 10,247 | SNOMED codes; need clinical review [NB p.23] | Hold |
| Georgia 12-lead (`georgia`), Challenge 2021 / 1.0.3 | PhysioNet Challenge 2021 [MCR p.11] | USA | Unknown | Unknown | 10,344 | SNOMED codes; need clinical review [NB p.23] | Hold |
| CPSC 2018 (`cpsc_2018`), Challenge 2021 / 1.0.3 | PhysioNet Challenge 2021 [MCR p.11] | China | Unknown | Unknown | 6,877 | SNOMED codes; need clinical review [NB p.23] | Hold |
| CPSC-Extra (`cpsc_extra`), Challenge 2021 / 1.0.3 | PhysioNet Challenge 2021 [MCR p.11] | China | Unknown | Unknown | 3,453 | SNOMED codes; need clinical review [NB p.23] | Hold |
| SPH (`sph`), Figshare collection 5779802 v1 | **Shandong Provincial Hospital** [CMP p.2]; Figshare; Liu et al., *Scientific Data* 2022 [MCR p.11] | China | 2019–2020 | MedEx MECG-200 | 25,770 | AHA statements in `code.csv`; need review [MCR p.8; NB p.23] | **Candidate** |
| PTB Diagnostic (`ptb_diagnostic`), 1.0.0 native | PhysioNet, physionet.org/content/ptbdb/1.0.0 [MCR p.11] | Germany | Unknown | Non-commercial PTB prototype | 549 | None stated in the PDFs. BG-UNCONFIRMED: header "reason for admission" field | **Candidate** |
| INCART (`incart`), 1.0.0 native | PhysioNet, physionet.org/content/incartdb/1.0.0 [MCR p.11] | Russia | Unknown | Unknown | 75 (Challenge subset 74, never mix [MCR p.3]) | Beat annotations only (`.atr`), not acute-MI outcomes [MCR p.9] | Hold (Holter) |
| CODE-15% (`code15`), Zenodo 4916206 | Zenodo record 4916206; author preprocessing docs on GitHub [MCR p.11] | Brazil | 2010–2016 | Unknown | 345,779 | Rhythm labels; target-label availability unverified [MCR p.8; NB p.23]. BG-UNCONFIRMED: no MI class | Hold |

Notes:

- "Where it comes from" means the publisher or host recorded in the registry. Apart from SPH, the PDFs do not name the collecting institution. BG-UNCONFIRMED examples: PTB-XL and PTB Diagnostic come from the Physikalisch-Technische Bundesanstalt (Berlin); MIMIC from Beth Israel Deaconess Medical Center (Boston); Georgia from Emory University; INCART from the St Petersburg Institute of Cardiological Technics; CODE from the Telehealth Network of Minas Gerais.
- Known overlap risks: PTB-XL 100 Hz vs 500 Hz copies (count once); Ningbo + Chapman also appear as a combined export; CPSC-Extra vs other CPSC exports; INCART native vs Challenge [MCR p.3; MCR p.8]. Signal-level duplicates were never checked [MCR p.10; NB p.25].

---

## 3. Recommended next steps (in order)

The order follows the PDFs' own recommendation: bounded metadata/header checks, then label review, then patient-level splits [MCR p.1; MCR p.10; CMP p.5]. Task IDs refer to `TASKS.md`.

1. **Finish the synthetic groundwork (in progress: T1 inventory, T2 label mapper).** This lets the code enforce the contract rules before any real data arrives.
2. **Bounded header check on real PTB-XL and MIMIC files (T3).** It needs the user to supply local paths. It reads only `.hea` headers, never signals: up to 50 per source with a fixed seed [NB p.29–30]. Output: observations, missing items and conflicts, kept separate from the registry [CMP p.5 step 1; E3].
3. **Close the priority evidence gaps (T4)**, in this order: units, gain/baseline, lead order, device semantics, filters [MCR p.10 item 2]. MIMIC calibration is the main blocker for that pair [MCR p.6].
4. **Agree the input specification (T5).** 12 leads / 500 Hz / 10 s is a study setting, not a proven choice [CMP p.5 step 2]. Open question Q9.
5. **Clinical label review (T6).** The supervisor defines what counts as acute STEMI, NSTEMI and non-MI, and reviews candidates. This is the step that creates usable labels [CMP p.5 step 3; MCR p.8].
6. **Patient-level splits and leakage audit (T7)** [CMP p.5 step 4; MCR p.10 item 4].
7. **Per-source decision record (T8)**, then **freeze the hierarchical-vs-flat comparison protocol (T9)** on the same cohort, splits and input [MCR p.10 item 5].

### What a first simple performance test would need

The PDFs say no source is approved for supervised acute three-class training [NB p.24; MCR p.1], and research_plan step 8 gates training on steps 4–7. A *clinically meaningful* performance number is therefore not possible yet. Three levels of "first test" are possible:

| Level | Dataset(s) | Labels | What it shows | Blocked by |
|---|---|---|---|---|
| **A. Pipeline smoke test** | Synthetic fixtures only (T1/T2) | Synthetic, randomly assigned | Code runs end to end (load → label map → split → train → metrics). **No clinical meaning; the number must not be reported as performance.** | Nothing beyond T1/T2. Needs the user to approve the scope (the team lead is confirming). |
| **B. Technical proxy on real data** (ASSUMPTION, needs user and supervisor approval) | PTB-XL 1.0.3 records500 only. It is a Candidate, has a documented `patient_id` for patient-level splits [MCR p.9], and is already being collected for the project [CMP p.4] | A proxy target such as "PTB-XL report contains a reviewer-approved MI statement" vs "contains a reviewer-approved positive alternative statement". Must **not** be called acute STEMI/NSTEMI (L2, L3), and code absence must **not** become non-MI (L1). | Whether the signal and pipeline work on real ECGs. Not the research target. | User-supplied local PTB-XL files (T3); approved code lists (BG-UNCONFIRMED; plan Q2); input spec (Q9); split ratio (Q10); a decision that a proxy task is acceptable at all (Q5) |
| **C. First real acute three-class test** | PTB-XL first. Adding MIMIC-IV-ECG needs calibration checks [MCR p.8] and clinical linkage (Q3) | `confirmed` labels from the clinical review (T6) only | The actual research question, still on a single source at first | Q2 (reference standard and acute window), Q3 (MIMIC clinical access), Q4 (positive non-MI evidence), Q5, Q9, Q10, and T3–T8 complete |

Recommendation: do **A** as soon as the user confirms, and treat **B** only as a technical check, explicitly labelled as such. **C** is the real milestone. It depends on the clinical supervisor more than on code.

---

## 4. Open questions that block progress

From `data_contract.md` §9 and `research_plan.md` §4. The most blocking ones:

- **Q1:** Is `metadata_compatibility_v1.zip` available? The PDFs cite it as the evidence base, but it is not in the repo [CMP p.6; MCR p.11].
- **Q2:** What is the acute-MI reference standard and acute time window?
- **Q3:** Does the project have access to MIMIC-IV clinical modules?
- **Q4:** What counts as positive evidence for non-MI?
- **Q5:** May PTB-XL MI statements ever reach `confirmed`?
- **Q9:** What is the final input specification?
- **Q10:** What split ratios will be used, and will a whole source be held out for external validation?
- **Plan Q2:** Will the supervisor sign off the MI-statement and ST/injury code lists?
- **New:** Is a performance test of level A or B (above) wanted, and is a proxy target acceptable?
