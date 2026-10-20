# Findings: `chapman_shaoxing` (PhysioNet Challenge 2021 1.0.3 folder `chapman_shaoxing`)

Author: coder, 2026-10-21. Status: **for planner verification**.

Source keys: **CH21**, **PA2020** and **DXM** as in `results/findings_cpsc_2018.md`; here the DXM column is `Chapman_Shaoxing`.
- **ZH2020** = Zheng et al. 2020, Sci Data, doi:10.1038/s41597-020-0386-x, https://pmc.ncbi.nlm.nih.gov/articles/PMC7016169/ (read 2026-10-21 through WebFetch; it describes the original 10,646-patient figshare release, not the Challenge folder).
- **EA** = https://physionet.org/content/ecg-arrhythmia/1.0.0/ (read 2026-10-20).
- **G1** = **g1 sample only**: the 999 `.hea` files in `training/chapman_shaoxing/g1/` (approval #8 option C). g1/RECORDS lists 1,000 names; `JS01052.hea` returned HTTP 404 (manifest). Header checksums: not available (SHA256SUMS stream not approved). Outputs: `results/challenge_chapman_shaoxing_*`.

| Key | Finding | Source |
|---|---|---|
| Q1 `labels` | SNOMED CT codes in `#Dx:` (G1: 35 distinct codes, none unmapped). The original release used letter labels (11 rhythms + 67 other conditions) mapped to SNOMED. Original MI/ST labels: MI, MIBW, MIFW, MILW, MISW (MI by wall), STDD "ST drop down", STE "ST extension", STTC "ST-T change", STTU "ST tilt up", AQW "abnormal Q wave". | G1; ZH2020 (label table); EA (ConditionNames_SNOMED-CT.csv) |
| Q2 `labellers` | "a licensed physician labeled the rhythm and other cardiac conditions"; a second licensed physician validated; "If there was a disagreement, a senior physician intervened and made a final decision." | ZH2020; EA |
| Q3 `collection` | Shaoxing People's Hospital (Shaoxing Hospital Zhejiang University School of Medicine), Shaoxing, China, with Chapman University. Years: **not found**. ZH2020: 10,646 patients (5,956 male / 4,690 female), ages 4–98; it describes a 10-s resting ECG per subject (one ECG per patient is implied, not stated). G1: Male 593 / Female 406; age 4–89 (median 61). | ZH2020; EA; G1 |
| Q4 `setting` | **Not found** ("12-lead resting ECG test"; in/outpatient not stated). | ZH2020 |
| Q5 `device` | "The data was stored into the GE MUSE ECG system" (storage system, not an acquisition model; [NB p.15]). 500 Hz, 10 s. G1: all 999 = 12 leads, 500 Hz, 5,000 samples (10 s), gain 1000/mV (mV), lead order I, II, III, aVR, aVL, aVF, V1–V6. | ZH2020; EA; G1 `results/challenge_chapman_shaoxing_headers.csv` |
| Q6 `stemi_nstemi` | **No STEMI/NSTEMI label; few MI labels.** Publisher's counts (DXM `Chapman_Shaoxing`): myocardial infarction 164865005 **40**; st elevation 164931005 176; st depression 429622005 402; qwave abnormal 235; nonspecific st t abnormality 1,158 (review only). G1 sample: st depression 33; qwave abnormal 18; st elevation 11; myocardial infarction 3; NSSTTA 98. **Label-origin caveat:** per ZH2020/EA, the codes that dx_mapping calls "st elevation" / "st depression" come from the original labels "ST tilt up" (STTU) / "ST drop down" (STDD), and the four MI-by-wall labels share one SNOMED code. | DXM; G1 `results/challenge_chapman_shaoxing_summary.md`; ZH2020; `ConditionNames_SNOMED-CT.csv` |
| Q7 `model_use` | ASSUMPTION (coder proposal): not an MI or STEMI/NSTEMI source (MI 40 in the full folder). Pretraining candidate (L11). | Q6 |
| Q8 `combine` | Preliminary: 500 Hz, 10 s, 12 leads (matches C1.3, no resampling or windowing). No patient ID in headers (G1); ZH2020 describes a 10-s resting ECG per subject in the original release (one ECG per patient is implied, not stated). **Overlap:** EA (45,152 ECGs) = Challenge Chapman 10,247 + Ningbo 34,905 (**count match only**, contract O4); the original figshare release had 10,646 records vs 10,247 in the Challenge folder (difference not explained by any source read). | ZH2020; EA; CH21; contract O4 |
| Q9 `access` | Open (CH21; EA "Anyone can access the files…"). | CH21; EA |
| Q10 `size_license` | 10,247 recordings in the Challenge folder (CH21); Challenge release CC BY 4.0; ZH2020 article CC BY 4.0, its metadata files CC0; EA CC BY 4.0. | CH21; ZH2020; EA |
