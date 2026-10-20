# PTB Diagnostic ECG Database review (local observation)

- Dataset: `ptb_diagnostic`, release 1.0.0 native
- Script: `src/stemi/review/review_ptbdb.py`; generated 2026-10-20T12:41:40+00:00
- Local observation of the downloaded file(s) named below; not a release-level fact (data_contract E2, E3). Labels are described, not converted into training labels (L1, L2).

## Input files

| local_path | url | sha256 | download_utc | checksum_match |
|---|---|---|---|---|
| data/samples/ptb_diagnostic/RECORDS | https://physionet.org/files/ptbdb/1.0.0/RECORDS | 1bdcd205432b66e98389e095c8ea9f2f642f79265a1874929a9cb6de270852fe | 2026-10-20T11:48:15+00:00 | yes |
| data/samples/ptb_diagnostic/CONTROLS | https://physionet.org/files/ptbdb/1.0.0/CONTROLS | 444b9dee4f28a4030267c4963106d433ffff68ff32446d26120532d67b695582 | 2026-10-20T11:48:18+00:00 | yes |

## Basic counts

| item | value |
|---|---|
| records in RECORDS | 549 |
| headers found | 549 |
| distinct patient folders (RECORDS) | 290 |
| lines in CONTROLS | 80 |
| n_sig values | 15: 549 |
| fs values | 1000: 549 |
| duration s min / median / max | 32 / 115.2 / 120.012 |
| records with all standard 12 leads by name | 549 |
| lead name sets | i|ii|iii|avr|avl|avf|v1|v2|v3|v4|v5|v6|vx|vy|vz |
| units values |  |
| comment keys found | age; sex; ECG date; Diagnose; Reason for admission; Acute infarction (localization); Former infarction (localization); Additional diagnoses; Smoker; Number of coronary vessels involved; Infarction date (acute); Previous infarction (1) date; Previous infarction (2) date; Hemodynamics; Catheterization date; Ventriculography; Chest X-ray; Peripheral blood Pressure (syst/diast); Pulmonary artery pressure (at rest) (syst/diast); Pulmonary artery pressure (at rest) (mean); Pulmonary capillary wedge pressure (at rest); Cardiac output (at rest); Cardiac index (at rest); Stroke volume index (at rest); Pulmonary artery pressure (laod) (syst/diast); Pulmonary artery pressure (laod) (mean); Pulmonary capillary wedge pressure (load); Cardiac output (load); Cardiac index (load); Stroke volume index (load); Aorta (at rest) (syst/diast); Aorta (at rest) mean; Left ventricular enddiastolic pressure; Left coronary artery stenoses (RIVA); Left coronary artery stenoses (RCX); Right coronary artery stenoses (RCA); Echocardiography; Therapy; Infarction date; Admission date; Medication pre admission; Start lysis therapy (hh.mm); Lytic agent; Dosage (lytic agent); Additional medication; In hospital medication; Medication after discharge |
| key used for reason | Reason for admission |
| key used for acute_loc | Acute infarction (localization) |
| key used for former_loc | Former infarction (localization) |
| key used for infarct_date | Infarction date (acute) |
| key used for ecg_date | ECG date |
| ECG date 'a/b/yyyy' values: total / a>12 / b>12 (day-first evidence) | 541 / 374 / 0 |
| records where 'Infarction date (acute)' != 'Infarction date' | 3 |

## Reason for admission (records / patients)

| key | value | n_records | n_patients |
|---|---|---|---|
| Reason for admission | Myocardial infarction | 368 | 148 |
| Reason for admission | Healthy control | 80 | 52 |
| Reason for admission | n/a | 27 | 22 |
| Reason for admission | Bundle branch block | 17 | 15 |
| Reason for admission | Cardiomyopathy | 17 | 15 |
| Reason for admission | Dysrhythmia | 16 | 14 |
| Reason for admission | Hypertrophy | 7 | 7 |
| Reason for admission | Valvular heart disease | 6 | 6 |
| Reason for admission | Myocarditis | 4 | 4 |
| Reason for admission | Stable angina | 2 | 2 |
| Reason for admission | Heart failure (NYHA 2) | 1 | 1 |
| Reason for admission | Heart failure (NYHA 3) | 1 | 1 |
| Reason for admission | Heart failure (NYHA 4) | 1 | 1 |
| Reason for admission | Palpitation | 1 | 1 |
| Reason for admission | Unstable angina | 1 | 1 |

## MI timing: ECG date minus infarction date (listing only; not an acute label, L2)

MI records (reason contains 'infarct'): 368; patients 148; with both dates parsed: 343.

| index | days |
|---|---|
| count | 343.0 |
| mean | 24.845481049562682 |
| std | 119.92981391049975 |
| min | -1789.0 |
| 25% | 3.0 |
| 50% | 8.0 |
| 75% | 16.5 |
| max | 609.0 |

Day bands (records): <0: 1, 0-1: 61, 2-3: 35, 4-7: 68, 8-28: 115, >28: 63

## MI patients by their earliest ECG after the acute infarction date (listing only)

| earliest_ecg_days_after_infarction | n_patients |
|---|---|
| 0-1 | 60 |
| 2-3 | 18 |
| 4-7 | 20 |
| 8-28 | 23 |
| >28 | 2 |
| no ECG with both dates parsed (and >= 0 days) | 25 |

## 'Lytic agent' field over MI records (raw text; no clinical meaning assigned)

| value | n_records | n_patients |
|---|---|---|
| Streptokinase | 199 | 60 |
| n/a | 68 | 49 |
| Urokinase | 63 | 20 |
| Gamma-TPA | 31 | 15 |
| - | 5 | 2 |
| Ca-antagonist Theophyllin 5-Fluoro-uracil Mitomycin | 1 | 1 |
| Captopril Digoxin Furosemide Isosorbit-Dinitrate Lovastatin ASA Glibenclamide | 1 | 1 |

## Acute infarction (localization) (records / patients)

| key | value | n_records | n_patients |
|---|---|---|---|
| Acute infarction (localization) | no | 175 | 140 |
| Acute infarction (localization) | inferior | 89 | 30 |
| Acute infarction (localization) | antero-septal | 77 | 27 |
| Acute infarction (localization) | infero-lateral | 53 | 22 |
| Acute infarction (localization) | anterior | 47 | 17 |
| Acute infarction (localization) | antero-lateral | 43 | 16 |
| Acute infarction (localization) | n/a | 27 | 22 |
| Acute infarction (localization) | infero-postero-lateral | 16 | 7 |
| Acute infarction (localization) | postero-lateral | 5 | 2 |
| Acute infarction (localization) | posterior | 4 | 1 |
| Acute infarction (localization) | infero-latera | 3 | 1 |
| Acute infarction (localization) | infero-poster-lateral | 3 | 1 |
| Acute infarction (localization) | lateral | 3 | 1 |
| Acute infarction (localization) | antero-septo-lateral | 2 | 1 |
| Acute infarction (localization) | infero-posterior | 1 | 1 |
| Acute infarction (localization) | unknown | 1 | 1 |

## Former infarction (localization) (records / patients)

| key | value | n_records | n_patients |
|---|---|---|---|
| Former infarction (localization) | no | 423 | 209 |
| Former infarction (localization) | anterior | 27 | 14 |
| Former infarction (localization) | n/a | 27 | 22 |
| Former infarction (localization) | inferior | 23 | 13 |
| Former infarction (localization) | unknown | 14 | 13 |
| Former infarction (localization) | antero-lateral | 6 | 3 |
| Former infarction (localization) | infero-posterior | 5 | 3 |
| Former infarction (localization) | antero-septal | 4 | 1 |
| Former infarction (localization) | infero-lateral | 4 | 2 |
| Former infarction (localization) | postero-lateral | 4 | 1 |
| Former infarction (localization) | inferior ? | 3 | 1 |
| Former infarction (localization) | anterior (1), inferior (2) | 2 | 2 |
| Former infarction (localization) | inferior (1+2) | 2 | 1 |
| Former infarction (localization) | anterior (1), anterior (2) | 1 | 1 |
| Former infarction (localization) | anterior ? | 1 | 1 |
| Former infarction (localization) | antero-septal ? | 1 | 1 |
| Former infarction (localization) | infero-posterior (1), inferior (2) | 1 | 1 |
| Former infarction (localization) | infero-postero-lateral | 1 | 1 |

## Header files

549 .hea files listed in RECORDS; per-file provenance in results/download_manifest.csv.
