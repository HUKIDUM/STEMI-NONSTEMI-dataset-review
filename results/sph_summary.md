# SPH metadata review (local observation)

- Dataset: `sph`, release figshare collection 5779802 v1
- Script: `src/stemi/review/review_sph.py`; generated 2026-10-20T11:54:16+00:00
- Local observation of the downloaded file(s) named below; not a release-level fact (data_contract E2, E3). Labels are described, not converted into training labels (L1, L2).

## Input files

| local_path | url | sha256 | download_utc | checksum_match |
|---|---|---|---|---|
| data/samples/sph/metadata.csv | https://ndownloader.figshare.com/files/34793152 | c6f8dc5197758a3970aae554f8b6ee884d96656b121879bc0eb1adf367ea6d86 | 2026-10-20T11:52:20+00:00 | yes |
| data/samples/sph/code.csv | https://ndownloader.figshare.com/files/32630954 | 4d22759fd19d37133c78d439a5726f9e0bc412cc17483c424926ce9abb33c8fc | 2026-10-20T11:52:23+00:00 | yes |
| data/samples/sph/rule.pdf | https://ndownloader.figshare.com/files/35284594 | 3991b608fa1f9ab470a934a6437352ebd0080c9dd066dc5085cb155208dfec68 | 2026-10-20T11:52:25+00:00 | yes |

## Basic counts

| item | value |
|---|---|
| metadata.csv columns | ECG_ID, AHA_Code, Patient_ID, Age, Sex, N, Date |
| column used | ecg=ECG_ID, code=AHA_Code, patient=Patient_ID, age=Age, sex=Sex, n=N, date=Date |
| rows (ECGs) | 25770 |
| distinct ECG ids | 25770 |
| distinct patients | 24666 |
| code fields containing ';' / '+' | 3724 / 2470 |
| distinct primary codes | 44 |
| primary codes not in code.csv | none |
| distinct modifiers used | 308, 310, 330, 331, 332, 340, 341, 342, 346, 347, 349, 350, 362, 363, 367 |
| ECGs per patient: min / median / max | 1 / 1 / 5 |
| N (samples) min / median / max | 5000 / 5000 / 28000 |
| N / 500 s (500 Hz per [MCR p.3]) min / median / max | 10 / 10 / 56 |
| N value counts (top 5) | 5000: 18842; 6000: 2862; 5500: 1500; 6500: 608; 7500: 553 |
| age | 18–95 |
| sex | M: 14265; F: 11505 |
| date min / max (as stored) | 2019-08-01 00:00:00 / 2020-08-31 00:00:00 |

## Codes whose code.csv description mentions infarct / injury / ST elevation / ST deviation (listing only; L2)

ECGs with any: 3041; patients: 2939.

| code | description | n_ecgs | n_patients |
|---|---|---|---|
| 145 | ST deviation | 1829 | 1783 |
| 146 | ST deviation with T-wave change | 1063 | 1042 |
| 161 | Inferior MI | 120 | 117 |
| 165 | Anteroseptal MI | 91 | 82 |
| 160 | Anterior MI | 52 | 47 |
| 166 | Extensive anterior MI | 7 | 7 |

## MI codes by timing modifier: distinct ECGs (listing only; not acute labels, L2/L3)

| selection | n_ecgs | n_patients |
|---|---|---|
| any MI code ['160', '161', '165', '166'] | 260 | 242 |
| MI code with modifier 330 (Acute) | 7 | 7 |
| MI code with modifier 331 (Recent) | 12 | 9 |
| MI code with modifier 332 (Old) | 233 | 219 |
| MI code with none of the timing modifiers | 8 | 8 |
| MI code + Acute AND 145+363 (ST deviation + Elevation) on the same ECG | 1 | 1 |

## Modifiers attached to those codes

| code | description | modifier | modifier_description | n_ecgs | n_patients |
|---|---|---|---|---|---|
| 145 | ST deviation | 362 | Depression | 1024 | 1012 |
| 161 | Inferior MI | 332 | Old | 114 | 111 |
| 165 | Anteroseptal MI | 332 | Old | 75 | 70 |
| 160 | Anterior MI | 332 | Old | 47 | 42 |
| 145 | ST deviation | 363 | Elevation | 37 | 34 |
| 165 | Anteroseptal MI | 331 | Recent | 9 | 6 |
| 166 | Extensive anterior MI | 332 | Old | 7 | 7 |
| 165 | Anteroseptal MI | 330 | Acute | 4 | 4 |
| 161 | Inferior MI | 331 | Recent | 3 | 3 |
| 161 | Inferior MI | 330 | Acute | 2 | 2 |
| 160 | Anterior MI | 330 | Acute | 1 | 1 |

## All primary codes (top 40 by ECGs; full list in sph_code_counts.csv)

| code | description | n_ecgs | n_patients |
|---|---|---|---|
| 1 | Normal ECG | 13905 | 13498 |
| 22 | Sinus bradycardia | 2711 | 2640 |
| 147 | T-wave abnormality | 2218 | 2155 |
| 145 | ST deviation | 1829 | 1783 |
| 23 | Sinus arrhythmia | 1553 | 1527 |
| 105 | Incomplete right bundle-branch block | 1259 | 1238 |
| 60 | Ventricular premature complex(es) | 1067 | 1032 |
| 146 | ST deviation with T-wave change | 1063 | 1042 |
| 21 | Sinus tachycardia | 725 | 705 |
| 106 | Right bundle-branch block | 710 | 658 |
| 50 | Atrial fibrillation | 675 | 634 |
| 30 | Atrial premature complex(es) | 539 | 525 |
| 125 | Low voltage | 322 | 307 |
| 82 | Prolonged PR interval | 238 | 233 |
| 142 | Left ventricular hypertrophy | 209 | 201 |
| 120 | Right-axis deviation | 161 | 158 |
| 101 | Left anterior fascicular block | 154 | 149 |
| 121 | Left-axis deviation | 138 | 136 |
| 161 | Inferior MI | 120 | 117 |
| 51 | Atrial flutter | 99 | 88 |
| 165 | Anteroseptal MI | 91 | 82 |
| 153 | ST-T change due to ventricular hypertrophy | 88 | 86 |
| 104 | Left bundle-branch block | 84 | 79 |
| 36 | Junctional premature complex(es) | 64 | 63 |
| 160 | Anterior MI | 52 | 47 |
| 86 | AV block, varying conduction | 47 | 47 |
| 85 | 2:1 AV block | 35 | 32 |
| 155 | Early repolarization | 32 | 32 |
| 108 | Ventricular preexcitation | 27 | 27 |
| 148 | Prolonged QT interval | 24 | 23 |
| 88 | AV block, complete (third-degree) | 22 | 20 |
| 37 | Junctional escape complex(es) | 20 | 19 |
| 140 | Left atrial enlargement | 19 | 19 |
| 54 | Junctional tachycardia | 13 | 13 |
| 80 | Short PR interval | 11 | 11 |
| 83 | Second-degree AV block, Mobitz type I (Wenckebach) | 9 | 9 |
| 152 | TU fusion | 9 | 9 |
| 166 | Extensive anterior MI | 7 | 7 |
| 143 | Right ventricular hypertrophy | 6 | 6 |
| 102 | Left posterior fascicular block | 6 | 6 |
