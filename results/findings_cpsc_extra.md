# Findings: `cpsc_extra` (CPSC-Extra, PhysioNet Challenge 2021 1.0.3 folder `cpsc_2018_extra`)

Author: coder, 2026-10-21. Status: **for planner verification**.

Source keys: **CH21**, **PA2020** and **DXM** as in `results/findings_cpsc_2018.md`; here the DXM column is `CPSC_Extra`.
**G1** = **g1 sample only**: the 999 `.hea` files in `training/cpsc_2018_extra/g1/` (approval #8 option C, downloaded 2026-10-20). g1/RECORDS lists 1,000 names; `Q1033.hea` returns HTTP 404 (HEAD 2026-10-21). Header checksums: not available (SHA256SUMS stream not approved). Outputs: `results/challenge_cpsc_extra_*` (`src/stemi/review/review_challenge.py`).

| Key | Finding | Source |
|---|---|---|
| Q1 `labels` | SNOMED CT codes in `#Dx:`. G1: 49 distinct codes, none unmapped. | G1 `results/challenge_cpsc_extra_dx_counts.csv`; CH21 |
| Q2 `labellers` | **Not found** (same places as cpsc_2018: CH21, PA2020 general statement only, Liu 2018 not readable). | CH21; PA2020 |
| Q3 `collection` | The "unused data" of CPSC 2018 (China). Hospitals and years: not found. PA2020: CPSC-Extra mean age 63.7 years, 53% male. G1: Male 533 / Female 466; age −1 to 92 (median 65). The value −1 is in the file as written; its meaning is not documented. | CH21; PA2020; moody-challenge.physionet.org/2020 ("unused data (CPSC-Extra Database)"); G1 |
| Q4 `setting` | **Not found**. | CH21; PA2020 |
| Q5 `device` | Device: not found. G1: 12 leads, 500 Hz, gain 1000/mV, duration 9.996–98 s (median 12 s; 400 of 999 exactly 10 s). | G1 `results/challenge_cpsc_extra_headers.csv`; CH21 |
| Q6 `stemi_nstemi` | **No STEMI/NSTEMI label**, but **MI and old-MI codes exist**. Publisher's counts (DXM `CPSC_Extra`): myocardial infarction 164865005 **376**; old myocardial infarction 164867002 **1,168**; anterior myocardial infarction 54329005 62; myocardial ischemia 384; chronic myocardial ischemia 161; acute myocardial ischemia 1; st elevation 66; st depression 57; inferior ST segment depression 1; acute myocardial infarction 0. Also for review (not MI): nonspecific st t abnormality 1,290; st interval abnormal 481. G1 sample: old MI 337; MI 122; myocardial ischemia 101; chronic ischemia 45; st elevation 23; anterior MI 17; st depression 11; acute myocardial ischemia 1; inferior ST segment depression 1. "Old" vs unspecified MI gives a weak timing hint, but no acuity label and no subtype (L2, L3). ConditionNames_SNOMED-CT.csv lists four location names for 164865005 (front, lower, side, back wall). This suggests locations were collapsed into one code; noted, not interpreted. | DXM; G1 `results/challenge_cpsc_extra_summary.md`; `data/samples/challenge_label_maps/ConditionNames_SNOMED-CT.csv` |
| Q7 `model_use` | ASSUMPTION (coder proposal): MI-statement vs other review set (MI 376, old MI 1,168), after clinical review (L4). Not STEMI-vs-NSTEMI. Pretraining candidate. | Q6 |
| Q8 `combine` | Preliminary: 500 Hz, 12 leads, mostly >10 s. No patient ID (G1 comment keys). Overlap with `cpsc_2018` must be reviewed (O5); record names differ by prefix (A… vs Q…), but that alone proves nothing (S10). | G1; contract O5 |
| Q9 `access` | Open (CH21, Access). | CH21 |
| Q10 `size_license` | 3,453 recordings (CH21); CC BY 4.0 (whole Challenge). Patients: not found. | CH21 |
