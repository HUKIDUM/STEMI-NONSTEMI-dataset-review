# Combine matrix (mechanical; for planner review)

- Script: `src/stemi/review/combine_matrix.py`. Rules a–g and the incart rule as given by planner, applied in order; every applicable reason is listed. Attributes come only from verified_facts rows (table below).
- Note: SPH gain is not observed (no SPH header or waveform was read), so rule d treats it as unknown. INCART gains vary per record, but the incart rule applies first.

## Verdict counts

| verdict | pairs |
|---|---|
| After checks | 45 |
| No (supervised MI) | 10 |

## Pairs needing the fewest checks (2)

| ds_a | ds_b | reasons |
|---|---|---|
| ptb_xl | chapman_shaoxing | e. no patient ID (chapman_shaoxing): training use only (S7); f. label systems differ: SCP-ECG statements vs SNOMED CT |
| ptb_xl | ningbo | e. no patient ID (ningbo): training use only (S7); f. label systems differ: SCP-ECG statements vs SNOMED CT |
| cpsc_2018 | georgia | b. length policy: cpsc_2018 9–118 s (g1), georgia 5–10 s; e. no patient ID (cpsc_2018, georgia): training use only (S7) |
| cpsc_2018 | chapman_shaoxing | b. length policy: cpsc_2018 9–118 s (g1); e. no patient ID (cpsc_2018, chapman_shaoxing): training use only (S7) |
| cpsc_2018 | ningbo | b. length policy: cpsc_2018 9–118 s (g1); e. no patient ID (cpsc_2018, ningbo): training use only (S7) |
| cpsc_extra | georgia | b. length policy: cpsc_extra 9.996–98 s (g1), georgia 5–10 s; e. no patient ID (cpsc_extra, georgia): training use only (S7) |
| cpsc_extra | chapman_shaoxing | b. length policy: cpsc_extra 9.996–98 s (g1); e. no patient ID (cpsc_extra, chapman_shaoxing): training use only (S7) |
| cpsc_extra | ningbo | b. length policy: cpsc_extra 9.996–98 s (g1); e. no patient ID (cpsc_extra, ningbo): training use only (S7) |
| georgia | chapman_shaoxing | b. length policy: georgia 5–10 s; e. no patient ID (georgia, chapman_shaoxing): training use only (S7) |
| georgia | ningbo | b. length policy: georgia 5–10 s; e. no patient ID (georgia, ningbo): training use only (S7) |
| chapman_shaoxing | ningbo | e. no patient ID (chapman_shaoxing, ningbo): training use only (S7); g. overlap review: shared export; count match 10,247 + 34,905 = 45,152, complementary parts; never add ecg-arrhythmia on top (O4) |

## Number of checks per 'After checks' pair

| n_checks | pairs |
|---|---|
| 2 | 11 |
| 3 | 6 |
| 4 | 8 |
| 5 | 10 |
| 6 | 10 |

## Attributes used

| dataset | fs_hz | duration | lead_map_needed | gain_per_mV | patient_id | labels | rows |
|---|---|---|---|---|---|---|---|
| ptb_xl | 500 | 10 s | False | 1000.0 | True | SCP-ECG statements | ptb_xl Q1, Q5, Q8 |
| mimic_iv_ecg | 500 | 10 s | True | 200.0 | True | machine text / ICD (credentialed) | mimic_iv_ecg Q1, Q5, Q8 |
| ptb_diagnostic | 1000 | 32–120 s | True | 2000.0 | True | free-text clinical summary | ptb_diagnostic Q1, Q5, Q8 |
| sph | 500 | 10–56 s | False | unknown | True | AHA statements | sph Q1, Q5, Q8 |
| cpsc_2018 | 500 | 9–118 s (g1) | False | 1000.0 | False | SNOMED CT | cpsc_2018 Q1, Q5 device (g1); Q8 combine (technical part) |
| cpsc_extra | 500 | 9.996–98 s (g1) | False | 1000.0 | False | SNOMED CT | cpsc_extra Q1, Q5 device (g1); Q8 combine (technical part) |
| georgia | 500 | 5–10 s | False | 1000.0 | False | SNOMED CT | georgia Q1, Q5 device (g1); Q8 combine (technical part) |
| chapman_shaoxing | 500 | 10 s | False | 1000.0 | False | SNOMED CT | chapman_shaoxing Q1, Q5 device (g1); Q8 combine (technical part) |
| ningbo | 500 | 10 s | False | 1000.0 | False | SNOMED CT | ningbo Q1, Q5 device (g1); Q8 combine (technical part) |
| code15 | 400 | 7–10 s, zero-padded | True | unknown | True | rhythm flags (no MI labels) | code15 Q1, Q5, Q6, Q8 |
| incart | 257 | 1,800 s Holter | False | unknown | True | beat annotations + patient text | incart Q4, Q5, Q8 |
