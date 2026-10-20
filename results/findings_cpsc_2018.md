# Findings: `cpsc_2018` (CPSC 2018, PhysioNet Challenge 2021 1.0.3 folder `cpsc_2018`)

Author: coder, 2026-10-21. Status: **for planner verification**.

Source keys:
- **CH21** = https://physionet.org/content/challenge-2021/1.0.3/ (Data Sources; Data Description; Access), read 2026-10-20 through WebFetch.
- **PA2020** = Perez Alday et al. 2020, Physiol Meas 41:124003, doi:10.1088/1361-6579/abc960, https://pmc.ncbi.nlm.nih.gov/articles/PMC8015789/ (read 2026-10-20 through WebFetch).
- **DXM** = publisher's counts from `dx_mapping_scored.csv` / `dx_mapping_unscored.csv`, column `CPSC` (raw.githubusercontent.com/physionetchallenges/evaluation-2021/main, `main` branch, downloaded 2026-10-20 11:59Z; sha256 in `results/download_manifest.csv`). Counts as listed; their meaning is not defined by the publisher (for the INCART column they equal record counts, which suggests the same here).
- **G1** = **g1 sample only**: local observation of the 999 `.hea` files in `training/cpsc_2018/g1/`, downloaded 2026-10-20 (approval #8 option C). g1/RECORDS lists 1,000 names; `A1000.hea` returns HTTP 404 (and `A1000.mat` too; HEAD 2026-10-21). Header checksums: not available (SHA256SUMS stream not approved). Made by `src/stemi/review/review_challenge.py`; outputs `results/challenge_cpsc_2018_*`.

| Key | Finding | Source |
|---|---|---|
| Q1 `labels` | **SNOMED CT codes** in the header `#Dx:` field (comma-separated). G1: 9 distinct codes, none unmapped. CH21: "We mapped the labels for each recording to SNOMED-CT codes." | G1 `results/challenge_cpsc_2018_dx_counts.csv`; CH21, Data Description |
| Q2 `labellers` | **Not found** for this source. Looked at: CH21 (no source-specific method), PA2020 (only a general statement that Challenge labels were "machine-generated, over-read by a single cardiologist, and adjudicated by multiple cardiologists", not assigned per database), Liu et al. 2018, doi:10.1166/jmihi.2018.2442 (redirects to ingentaconnect.com, HTTP 403, not readable). | CH21; PA2020; doi.org redirect |
| Q3 `collection` | China Physiological Signal Challenge 2018, "held during the 7th International Conference on Biomedical Engineering and Biotechnology in Nanjing, China". Hospitals and years: **not found** (Liu 2018 not readable). PA2020: CPSC training recordings mean age 60.2 years, 54% male. G1: Male 521 / Female 478; age 7–92 (median 64; 1 "NaN"). CH21: "ages over 89 are not provided … recorded as 92". | CH21; PA2020 (Table 1 per WebFetch); G1 summary "Basic counts" |
| Q4 `setting` | **Not found**. | CH21; PA2020 |
| Q5 `device` | Device: **not found**. 500 Hz; CH21 says "between 6 and 144 seconds" for CPSC overall (contract note: the range covers the combined source). G1: 12 leads, fs 500, gain 1000/mV (units mV), duration 9–118 s (median 12.092 s; 364 of 999 exactly 10 s). | CH21, Data Sources; G1 `results/challenge_cpsc_2018_headers.csv` |
| Q6 `stemi_nstemi` | **Neither STEMI/NSTEMI nor an MI label.** MI-related codes in the full source (DXM `CPSC`): myocardial infarction 0; acute MI 0; **st elevation (164931005) 220; st depression (429622005) 869**. G1 sample: st elevation 31, st depression 114 records. ST elevation as a machine/report finding is not an MI outcome (L2). Name note: ConditionNames_SNOMED-CT.csv calls 164931005 "ST tilt up" and 429622005 "ST drop down". | DXM; G1 `results/challenge_cpsc_2018_summary.md` (MI/ST section) |
| Q7 `model_use` | ASSUMPTION (coder proposal): not a STEMI/NSTEMI or MI source. ST-elevation/depression codes could be a review set for ST-change detection only. Pretraining candidate (L11). | Q6; contract L2, L11 |
| Q8 `combine` | Preliminary (final in S10): 500 Hz, 12 leads, mostly >10 s (window policy needed). **No patient ID** in headers (G1: no patient-like comment key; keys are Age, Sex, Dx, Rx, Hx, Sx). PA2020: the Challenge changed only "approximate SNOMED CT codes", anonymised age/sex and amplitude resolution. Overlap with `cpsc_extra` (same challenge; O5) is unreviewed. | G1 `results/challenge_cpsc_2018_comment_keys.csv`; PA2020; contract O5, S7 |
| Q9 `access` | **Open**: "Anyone can access the files, as long as they conform to the terms of the specified license." | CH21, Access |
| Q10 `size_license` | 6,877 recordings (CH21 folder list); Challenge 2021 total 12.6 GB uncompressed; **CC BY 4.0** (whole Challenge release). Patients: not found. | CH21 |
