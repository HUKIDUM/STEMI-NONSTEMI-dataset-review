# Challenge 2021 `chapman_shaoxing` header review (local observation)

- Dataset: `chapman_shaoxing`, release PhysioNet Challenge 2021, 1.0.3
- Script: `src/stemi/review/review_challenge.py`; generated 2026-10-20T17:39:10+00:00
- Local observation of the downloaded file(s) named below; not a release-level fact (data_contract E2, E3). Labels are described, not converted into training labels (L1, L2).

## Input files

| local_path | url | sha256 | download_utc | checksum_match |
|---|---|---|---|---|
| data/samples/chapman_shaoxing/training/chapman_shaoxing/g1/RECORDS | https://physionet.org/files/challenge-2021/1.0.3/training/chapman_shaoxing/g1/RECORDS | fb10afd81ebafef83deab12e4bcb44dafa2121f4dc9dfb3150cfd72688355f1e | 2026-10-20T16:29:25+00:00 | not available |
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
| sex values | Male: 593; Female: 406 |
| age (numeric) min / median / max | 4 / 61 / 89 |
| age non-numeric values | none |
| comment keys | Age (999); Sex (999); Dx (999); Rx (999); Hx (999); Sx (999) |
| any patient-ID-like comment key | none found |
| distinct SNOMED codes | 35 |
| unmapped codes | none |
| map files used | ConditionNames_SNOMED-CT.csv, dx_mapping_scored.csv, dx_mapping_unscored.csv |

## Scope

**g1 sample only (999 of 1000 records listed in g1/RECORDS; not the full source).** `publisher_count_full_source` = the `Chapman_Shaoxing` column of dx_mapping_*.csv (publisher's counts, meaning not defined by the publisher). Header checksums: not available (SHA256SUMS stream not approved); see results/download_manifest.csv.

## SNOMED codes whose name matches an MI / ST / ischaemia keyword (listing only; L2)

Records with any: 54. Keyword regexes: kw_infarct = `infarct|\bMI\b|STEMI`; kw_injury = `injury`; kw_st_elev = `ST[\s-]*(segment[\s-]*)?elev|\bSTE\b`; kw_st_depr = `ST[\s-]*(segment[\s-]*)?depr|\bSTD\b`; kw_ischemi = `isch[a]?emi`; kw_acute = `acute`; kw_q_wave = `q[\s-]*wave`; kw_st_other = `\bST[\s-]*T\b|\bST[\s-]*interval|\bST[\s-]*segment|non-?specific\s+ST`

| code | name | alt_name | abbreviation | n_records | publisher_count_full_source | map_source |
|---|---|---|---|---|---|---|
| 429622005 | st depression | ST drop down | STD | 33 | 402 | dx_mapping_unscored.csv |
| 164917005 | qwave abnormal | abnormal Q wave | QAb | 18 | 235 | dx_mapping_scored.csv |
| 164931005 | st elevation | ST tilt up | STE | 11 | 176 | dx_mapping_unscored.csv |
| 164865005 | myocardial infarction | Myocardial infgraction in the front wall | Myocardial infraction in the lower wall | Myocardial infraction in the side wall | myocardial infraction in back wall | MI | 3 | 40 | dx_mapping_unscored.csv |

## Other ST codes for review (kw_st_other; NOT MI-related by themselves)

| code | name | alt_name | abbreviation | n_records | publisher_count_full_source |
|---|---|---|---|---|---|
| 428750005 | nonspecific st t abnormality | ST-T Change | NSSTTA | 98 | 1158 |

## All SNOMED codes (top 40 by records; full list in dx_counts.csv)

| code | name | abbreviation | n_records | publisher_count_full_source |
|---|---|---|---|---|
| 426177001 | sinus bradycardia | SB | 460 | 3889 |
| 164889003 | atrial fibrillation | AF | 177 | 1780 |
| 164934002 | t wave abnormal | TAb | 176 | 1876 |
| 426783006 | sinus rhythm | NSR | 174 | 1826 |
| 427084000 | sinus tachycardia | STach | 142 | 1568 |
| 55827005 | left ventricular high voltage | LVHV | 129 | 1295 |
| 428750005 | nonspecific st t abnormality | NSSTTA | 98 | 1158 |
| 164890007 | atrial flutter | AFL | 46 | 445 |
| 59118001 | right bundle branch block | RBBB | 35 | 454 |
| 270492004 | 1st degree av block | IAVB | 33 | 247 |
| 429622005 | st depression | STD | 33 | 402 |
| 39732003 | left axis deviation | LAD | 31 | 382 |
| 17338001 | ventricular premature beats | VPB | 28 | 294 |
| 284470004 | premature atrial contraction | PAC | 23 | 258 |
| 698252002 | nonspecific intraventricular conduction disorder | NSIVCB | 21 | 235 |
| 164909002 | left bundle branch block | LBBB | 19 | 205 |
| 164917005 | qwave abnormal | QAb | 18 | 235 |
| 233917008 | av block | AVB | 17 | 166 |
| 251146004 | low qrs voltages | LQRSV | 17 | 249 |
| 47665007 | right axis deviation | RAD | 14 | 215 |
| 59931005 | t wave inversion | TInv | 13 | 157 |
| 251199005 | countercolockwise rotation | CCR | 12 | 162 |
| 164931005 | st elevation | STE | 11 | 176 |
| 164912004 | p wave change | PWC | 7 | 95 |
| 111975006 | prolonged qt interval | LQT | 5 | 57 |
| 251198002 | clockwise rotation | CR | 4 | 76 |
| 428417006 | early repolarization | ERe | 3 | 22 |
| 164865005 | myocardial infarction | MI | 3 | 40 |
| 251180001 | ventricular trigeminy | VTrig | 2 | 8 |
| 164937009 | u wave abnormal | UAb | 2 | 22 |
| 164873001 | left ventricular hypertrophy | LVH | 2 | 15 |
| 446358003 | right atrial hypertrophy | RAH | 1 | 3 |
| 251173003 | atrial bigeminy | AB | 1 | 3 |
| 164947007 | prolonged pr interval | LPR | 1 | 12 |
| 67751000119106 | right atrial  high voltage | RAHV | 1 | 8 |

## Input note

Input table lists the first 3 g*/RECORDS files and the map files; all 999 headers are logged in results/download_manifest.csv.
