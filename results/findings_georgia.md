# Findings: `georgia` (Georgia 12-lead ECG Challenge Database, PhysioNet Challenge 2021 1.0.3 folder `georgia`)

Author: coder, 2026-10-21. Status: **for planner verification**.

Source keys: **CH21**, **PA2020** and **DXM** as in `results/findings_cpsc_2018.md`; here the DXM column is `Georgia`.
**G1** = **g1 sample only**: the 999 `.hea` files in `training/georgia/g1/` (approval #8 option C, downloaded 2026-10-20). g1/RECORDS lists 1,000 names; `E01000.hea` returns HTTP 404 (HEAD 2026-10-21). Header checksums: not available (SHA256SUMS stream not approved). Outputs: `results/challenge_georgia_*`.

| Key | Finding | Source |
|---|---|---|
| Q1 `labels` | SNOMED CT codes in `#Dx:`. G1: 53 distinct codes, none unmapped. | G1 `results/challenge_georgia_dx_counts.csv`; CH21 |
| Q2 `labellers` | **Not found** per source. PA2020 has only the general statement ("machine-generated, over-read by a single cardiologist, and adjudicated by multiple cardiologists"); CH21: "Some databases use human-overread machine labels…" (not attributed). | PA2020; CH21 |
| Q3 `collection` | "The fourth source is the Georgia 12-lead ECG Challenge (G12EC) Database, Emory University, Atlanta, Georgia, USA" (PA2020); "a unique demographic of the Southeastern United States" (CH21). PA2020: mean age 60.5, 54% male, 15,742 patients (for the whole G12EC data, including hidden parts). Years: not found. G1: Male 564 / Female 435; age 20–89 (median 63), "NaN" for 24 records. | PA2020; CH21; G1 |
| Q4 `setting` | **Not found**. | PA2020; CH21 |
| Q5 `device` | Device: not found. CH21: "between 5 and 10 seconds long with a sampling frequency of 500 Hz". G1: 12 leads, 500 Hz, gain 1000/mV, duration 10 s for 989 and 5 s for 10 records. | CH21; G1 `results/challenge_georgia_headers.csv` |
| Q6 `stemi_nstemi` | **No STEMI/NSTEMI label**; MI codes are rare. Publisher's counts (DXM `Georgia`): myocardial infarction 7; acute myocardial ischemia 1; st elevation 134; st depression 38; anterior ischemia 281; inferior ischaemia 451; lateral ischaemia 903; qwave abnormal 464; nonspecific st t abnormality 1,883 and st interval abnormal 992 (both for review, not MI). G1 sample: qwave abnormal 73; lateral ischaemia 73; inferior ischaemia 43; anterior ischemia 39; st elevation 20; st depression 5; no MI code in g1. | DXM; G1 `results/challenge_georgia_summary.md` |
| Q7 `model_use` | ASSUMPTION (coder proposal): not an MI or STEMI/NSTEMI source (7 MI codes in the full source). Ischaemia/ST codes could be an ST-change review set only. Pretraining candidate. | Q6 |
| Q8 `combine` | Preliminary: 500 Hz, 12 leads, 5–10 s (5 s records need a padding policy, contract Q9). No patient ID in headers (G1 comment keys: Age, Sex, Dx, Rx 999 each, Hx 996). PA2020 gives 15,742 patients for G12EC, and CH21 gives 20,672 G12EC recordings in total. If both numbers cover the same set, some patients have more than one recording (**inference, not stated by the publisher**), and those patients cannot be grouped (S7). | G1; PA2020; contract S7 |
| Q9 `access` | Open (CH21, Access). | CH21 |
| Q10 `size_license` | 10,344 recordings in the public training set (CH21); CC BY 4.0 (whole Challenge). | CH21 |
