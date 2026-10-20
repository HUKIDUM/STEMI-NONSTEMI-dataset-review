# Challenge 2021 `ningbo` header review (local observation)

- Dataset: `ningbo`, release PhysioNet Challenge 2021, 1.0.3
- Script: `src/stemi/review/review_challenge.py`; generated 2026-10-20T18:07:33+00:00
- Local observation of the downloaded file(s) named below; not a release-level fact (data_contract E2, E3). Labels are described, not converted into training labels (L1, L2).

## Input files

| local_path | url | sha256 | download_utc | checksum_match |
|---|---|---|---|---|
| data/samples/ningbo/training/ningbo/g1/RECORDS | https://physionet.org/files/challenge-2021/1.0.3/training/ningbo/g1/RECORDS | 32cb289987f4a376bb7aaee2e49499238fc5fec0e8f7d1f114aa8d423ecf0d3e | 2026-10-20T17:09:24+00:00 | not available |
| data/samples/challenge_label_maps/dx_mapping_scored.csv | https://raw.githubusercontent.com/physionetchallenges/evaluation-2021/main/dx_mapping_scored.csv | fad13ad9f7ca230e7e6392ac8a264cb7cd157879525129f964c5f708eabb41d0 | 2026-10-20T11:59:30+00:00 | not available |
| data/samples/challenge_label_maps/dx_mapping_unscored.csv | https://raw.githubusercontent.com/physionetchallenges/evaluation-2021/main/dx_mapping_unscored.csv | ce53c9e35406e922f1634a38bb13c31e8cf7603291641a16c201d8e679f4fe94 | 2026-10-20T11:59:31+00:00 | not available |
| data/samples/challenge_label_maps/ConditionNames_SNOMED-CT.csv | https://physionet.org/files/ecg-arrhythmia/1.0.0/ConditionNames_SNOMED-CT.csv | 05d6fa23acdcbb466b378310ccfad22ea6cef4d3abfa83e8f660c77016be028d | 2026-10-20T11:59:32+00:00 | not available |

## Basic counts

| item | value |
|---|---|
| headers read | 999 |
| records listed in g*/RECORDS | 1000 |
| distinct record names | 999 |
| records with empty Dx | 0 |
| fs values | 500: 999 |
| n_sig values | 12: 999 |
| duration s min / median / max | 10 / 10 / 10 |
| duration s, top 5 values | 10: 999 |
| records with duration exactly 10 s | 999 |
| lead name sets | I|II|III|aVR|aVL|aVF|V1|V2|V3|V4|V5|V6 (999) |
| gains | 1000.0: 999 |
| units | mV: 999 |
| sex values | Male: 567; Female: 430; Unknown: 2 |
| age (numeric) min / median / max | 0 / 38 / 89 |
| age non-numeric values | NaN: 2 |
| comment keys | Age (999); Sex (999); Dx (999); Rx (999); Hx (999); Sx (999) |
| any patient-ID-like comment key | none found |
| distinct SNOMED codes | 64 |
| unmapped codes | none |
| map files used | ConditionNames_SNOMED-CT.csv, dx_mapping_scored.csv, dx_mapping_unscored.csv |

## Scope

**g1 sample only (999 of 1000 records listed in g1/RECORDS; not the full source).** `publisher_count_full_source` = the `Ningbo` column of dx_mapping_*.csv (publisher's counts, meaning not defined by the publisher). Header checksums: not available (SHA256SUMS stream not approved); see results/download_manifest.csv.

## SNOMED codes whose name matches an MI / ST / ischaemia keyword (listing only; L2)

Records with any: 42. Keyword regexes: kw_infarct = `infarct|\bMI\b|STEMI`; kw_injury = `injury`; kw_st_elev = `ST[\s-]*(segment[\s-]*)?elev|\bSTE\b`; kw_st_depr = `ST[\s-]*(segment[\s-]*)?depr|\bSTD\b`; kw_ischemi = `isch[a]?emi`; kw_acute = `acute`; kw_q_wave = `q[\s-]*wave`; kw_st_other = `\bST[\s-]*T\b|\bST[\s-]*interval|\bST[\s-]*segment|non-?specific\s+ST`

| code | name | alt_name | abbreviation | n_records | publisher_count_full_source | map_source |
|---|---|---|---|---|---|---|
| 429622005 | st depression | ST drop down | STD | 31 | 1266 | dx_mapping_unscored.csv |
| 164917005 | qwave abnormal | abnormal Q wave | QAb | 11 | 828 | dx_mapping_scored.csv |
| 164865005 | myocardial infarction | Myocardial infgraction in the front wall | Myocardial infraction in the lower wall | Myocardial infraction in the side wall | myocardial infraction in back wall | MI | 4 | 83 | dx_mapping_unscored.csv |
| 54329005 | anterior myocardial infarction |  | AnMI | 3 | 57 | dx_mapping_unscored.csv |
| 57054005 | acute myocardial infarction |  | AMI | 1 | 49 | dx_mapping_unscored.csv |

## Other ST codes for review (kw_st_other; NOT MI-related by themselves)

| code | name | alt_name | abbreviation | n_records | publisher_count_full_source |
|---|---|---|---|---|---|
| 164930006 | st interval abnormal | ST extension | STIAb | 22 | 799 |

## All SNOMED codes (top 40 by records; full list in dx_counts.csv)

| code | name | abbreviation | n_records | publisher_count_full_source |
|---|---|---|---|---|
| 427084000 | sinus tachycardia | STach | 433 | 5687 |
| 426783006 | sinus rhythm | NSR | 166 | 6299 |
| 426177001 | sinus bradycardia | SB | 158 | 12670 |
| 164934002 | t wave abnormal | TAb | 144 | 5167 |
| 270492004 | 1st degree av block | IAVB | 126 | 893 |
| 427393009 | sinus arrhythmia | SA | 117 | 2550 |
| 55930002 | s t changes | STC | 100 | 4232 |
| 164890007 | atrial flutter | AFL | 97 | 7615 |
| 284470004 | premature atrial contraction | PAC | 84 | 1054 |
| 59931005 | t wave inversion | TInv | 69 | 2720 |
| 55827005 | left ventricular high voltage | LVHV | 64 | 4106 |
| 429622005 | st depression | STD | 31 | 1266 |
| 251146004 | low qrs voltages | LQRSV | 24 | 794 |
| 39732003 | left axis deviation | LAD | 24 | 1163 |
| 164930006 | st interval abnormal | STIAb | 22 | 799 |
| 427172004 | premature ventricular contractions | PVC | 22 | 1091 |
| 426761007 | supraventricular tachycardia | SVT | 22 | 137 |
| 47665007 | right axis deviation | RAD | 21 | 638 |
| 713422000 | atrial tachycardia | ATach | 21 | 176 |
| 365413008 | poor R wave Progression | PRWP | 20 | 638 |
| 61721007 | clockwise or counterclockwise vectorcardiographic loop | CVCL/CCVCL | 20 | 653 |
| 713427006 | complete right bundle branch block | CRBBB | 18 | 1096 |
| 164873001 | left ventricular hypertrophy | LVH | 16 | 632 |
| 698252002 | nonspecific intraventricular conduction disorder | NSIVCB | 15 | 536 |
| 445118002 | left anterior fascicular block | LAnFB | 14 | 380 |
| 164917005 | qwave abnormal | QAb | 11 | 828 |
| 251170000 | blocked premature atrial contraction | BPAC | 10 | 62 |
| 111975006 | prolonged qt interval | LQT | 10 | 337 |
| 106068003 | atrial rhythm | ARH | 10 | 215 |
| 251223006 | tall p wave | TPW | 9 | 215 |
| 6374002 | bundle branch block | BBB | 9 | 385 |
| 10370003 | pacing rhythm | PR | 7 | 1182 |
| 733534002 | complete left bundle branch block | CLBBB | 6 | 213 |
| 428417006 | early repolarization | ERe | 6 | 344 |
| 426995002 | junctional escape | JE | 6 | 60 |
| 75532003 | ventricular escape beat | VEsB | 6 | 49 |
| 425856008 | paroxysmal ventricular tachycardia | PVT | 5 | 109 |
| 195042002 | 2nd degree av block | IIAVB | 5 | 58 |
| 713426002 | incomplete right bundle branch block | IRBBB | 4 | 246 |
| 251205003 | prolonged P wave | PPW | 4 | 106 |

## Input note

Input table lists the first 3 g*/RECORDS files and the map files; all 999 headers are logged in results/download_manifest.csv.
