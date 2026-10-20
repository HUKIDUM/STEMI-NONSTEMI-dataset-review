# Findings: `ningbo` (PhysioNet Challenge 2021 1.0.3 folder `ningbo`)

Author: coder, 2026-10-21. Status: **for planner verification**.

Source keys: **CH21**, **PA2020** and **DXM** as in `results/findings_cpsc_2018.md`; here the DXM column is `Ningbo`. **EA** = https://physionet.org/content/ecg-arrhythmia/1.0.0/ (read 2026-10-20).
**G1** = **g1 sample only**: the 999 `.hea` files in `training/ningbo/g1/` (approval #8 option C; downloaded 2026-10-21 as a separate run with 1 worker after MIMIC finished). g1/RECORDS lists 1,000 names; `JS11646.hea` returned HTTP 404 (manifest). Header checksums: not available (SHA256SUMS stream not approved). Outputs: `results/challenge_ningbo_*`.

| Key | Finding | Source |
|---|---|---|
| Q1 `labels` | SNOMED CT codes in `#Dx:` (G1: 64 distinct codes, none unmapped). | G1 `results/challenge_ningbo_dx_counts.csv` |
| Q2 `labellers` | EA (which covers Chapman + Ningbo): "a licensed physician labeled the rhythm and other cardiac conditions", validated by a second licensed physician, and "If there was a disagreement, a senior physician intervened and made a final decision." A Ningbo-specific description: **not found** (the Ningbo paper cited on EA was not read). | EA |
| Q3 `collection` | Ningbo First Hospital, China (CH21: "Chapman University, Shaoxing People's Hospital (Chapman-Shaoxing) and Ningbo First Hospital (Ningbo) database"). Years: **not found**. G1: Male 567 / Female 430 / Unknown 2; age 0–89 (**median 38**, much younger than the other Challenge g1 samples, 61–65); "NaN" age 2. | CH21; EA; G1 summary "Basic counts" |
| Q4 `setting` | **Not found**. | CH21; EA |
| Q5 `device` | "The data was stored into the GE MUSE ECG system" (EA; storage, not acquisition [NB p.15]). CH21: 10 s, 500 Hz. G1: all 999 = 12 leads, 500 Hz, 5,000 samples (10 s), 1000/mV, lead order I, II, III, aVR, aVL, aVF, V1–V6. | EA; CH21; G1 `results/challenge_ningbo_headers.csv` |
| Q6 `stemi_nstemi` | **No STEMI/NSTEMI label**, but the **only Challenge source with "acute myocardial infarction"**. Publisher's counts (DXM `Ningbo`): **acute myocardial infarction 57054005: 49**; myocardial infarction 164865005: 83; anterior myocardial infarction 54329005: 57; st depression 1,266; qwave abnormal 828; st elevation 0; st interval abnormal 799 (review only). G1 sample: st depression 31; qwave abnormal 11; myocardial infarction 4; anterior MI 3; **acute MI 1** (record `#Dx: 164930006,164934002,426783006,445118002,57054005`, age 68, male). Origin caveat: codes 57054005 and 54329005 are **not in** `ConditionNames_SNOMED-CT.csv` (EA), so the original Ningbo label behind them is not known. "Acute" is a report/label wording, not an adjudicated outcome (L2, L3). | DXM; G1; `data/samples/challenge_label_maps/ConditionNames_SNOMED-CT.csv` (64 lines, no 57054005 / 54329005) |
| Q7 `model_use` | ASSUMPTION (coder proposal): the 49 acute-MI-coded ECGs are a possible review set for "acute MI statement" vs other (L4, L7), but there is no STEMI/NSTEMI split, and with no patient ID they are not usable for a held-out test (S7). Pretraining candidate. | Q6; contract S7, L4 |
| Q8 `combine` | Preliminary: 500 Hz, 10 s, 12 leads (matches C1.3). No patient ID in headers (G1). Overlap: EA total 45,152 = Chapman 10,247 + Ningbo 34,905 (**count match only**, O4). | G1; EA; CH21 |
| Q9 `access` | Open (CH21; EA). | CH21; EA |
| Q10 `size_license` | 34,905 recordings (CH21); Challenge release CC BY 4.0; EA CC BY 4.0. | CH21; EA |
