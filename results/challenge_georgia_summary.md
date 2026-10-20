# Challenge 2021 `georgia` header review (local observation)

- Dataset: `georgia`, release PhysioNet Challenge 2021, 1.0.3
- Script: `src/stemi/review/review_challenge.py`; generated 2026-10-20T17:44:20+00:00
- Local observation of the downloaded file(s) named below; not a release-level fact (data_contract E2, E3). Labels are described, not converted into training labels (L1, L2).

## Input files

| local_path | url | sha256 | download_utc | checksum_match |
|---|---|---|---|---|
| data/samples/georgia/training/georgia/g1/RECORDS | https://physionet.org/files/challenge-2021/1.0.3/training/georgia/g1/RECORDS | 1de5cf7be3627d912ba32e8dbb5d6aba9dcdce5b203956925ffbcef66a330d85 | 2026-10-20T15:11:15+00:00 | not available |
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
| duration s min / median / max | 5 / 10 / 10 |
| duration s, top 5 values | 10: 989; 5: 10 |
| records with duration exactly 10 s | 989 |
| lead name sets | I|II|III|aVR|aVL|aVF|V1|V2|V3|V4|V5|V6 (999) |
| gains | 1000.0: 999 |
| units | mV: 999 |
| sex values | Male: 564; Female: 435 |
| age (numeric) min / median / max | 20 / 63 / 89 |
| age non-numeric values | NaN: 24 |
| comment keys | Age (999); Sex (999); Dx (999); Rx (999); Hx (996) |
| any patient-ID-like comment key | none found |
| distinct SNOMED codes | 53 |
| unmapped codes | none |
| map files used | ConditionNames_SNOMED-CT.csv, dx_mapping_scored.csv, dx_mapping_unscored.csv |

## Scope

**g1 sample only (999 of 1000 records listed in g1/RECORDS; not the full source).** `publisher_count_full_source` = the `Georgia` column of dx_mapping_*.csv (publisher's counts, meaning not defined by the publisher). Header checksums: not available (SHA256SUMS stream not approved); see results/download_manifest.csv.

## SNOMED codes whose name matches an MI / ST / ischaemia keyword (listing only; L2)

Records with any: 193. Keyword regexes: kw_infarct = `infarct|\bMI\b|STEMI`; kw_injury = `injury`; kw_st_elev = `ST[\s-]*(segment[\s-]*)?elev|\bSTE\b`; kw_st_depr = `ST[\s-]*(segment[\s-]*)?depr|\bSTD\b`; kw_ischemi = `isch[a]?emi`; kw_acute = `acute`; kw_q_wave = `q[\s-]*wave`; kw_st_other = `\bST[\s-]*T\b|\bST[\s-]*interval|\bST[\s-]*segment|non-?specific\s+ST`

| code | name | alt_name | abbreviation | n_records | publisher_count_full_source | map_source |
|---|---|---|---|---|---|---|
| 164917005 | qwave abnormal | abnormal Q wave | QAb | 73 | 464 | dx_mapping_scored.csv |
| 425623009 | lateral ischaemia |  | LIs | 73 | 903 | dx_mapping_unscored.csv |
| 425419005 | inferior ischaemia |  | IIs | 43 | 451 | dx_mapping_unscored.csv |
| 426434006 | anterior ischemia |  | AnMIs | 39 | 281 | dx_mapping_unscored.csv |
| 164931005 | st elevation | ST tilt up | STE | 20 | 134 | dx_mapping_unscored.csv |
| 429622005 | st depression | ST drop down | STD | 5 | 38 | dx_mapping_unscored.csv |

## Other ST codes for review (kw_st_other; NOT MI-related by themselves)

| code | name | alt_name | abbreviation | n_records | publisher_count_full_source |
|---|---|---|---|---|---|
| 428750005 | nonspecific st t abnormality | ST-T Change | NSSTTA | 149 | 1883 |
| 164930006 | st interval abnormal | ST extension | STIAb | 60 | 992 |

## All SNOMED codes (top 40 by records; full list in dx_counts.csv)

| code | name | abbreviation | n_records | publisher_count_full_source |
|---|---|---|---|---|
| 164934002 | t wave abnormal | TAb | 242 | 2306 |
| 426783006 | sinus rhythm | NSR | 191 | 1752 |
| 428750005 | nonspecific st t abnormality | NSSTTA | 149 | 1883 |
| 111975006 | prolonged qt interval | LQT | 146 | 1391 |
| 426177001 | sinus bradycardia | SB | 146 | 1677 |
| 427084000 | sinus tachycardia | STach | 137 | 1261 |
| 164873001 | left ventricular hypertrophy | LVH | 109 | 1232 |
| 59931005 | t wave inversion | TInv | 86 | 812 |
| 164917005 | qwave abnormal | QAb | 73 | 464 |
| 425623009 | lateral ischaemia | LIs | 73 | 903 |
| 164889003 | atrial fibrillation | AF | 70 | 570 |
| 39732003 | left axis deviation | LAD | 68 | 940 |
| 270492004 | 1st degree av block | IAVB | 61 | 769 |
| 164930006 | st interval abnormal | STIAb | 60 | 992 |
| 67741000119109 | left atrial enlargement | LAE | 58 | 870 |
| 284470004 | premature atrial contraction | PAC | 45 | 639 |
| 425419005 | inferior ischaemia | IIs | 43 | 451 |
| 59118001 | right bundle branch block | RBBB | 41 | 542 |
| 426434006 | anterior ischemia | AnMIs | 39 | 281 |
| 427393009 | sinus arrhythmia | SA | 38 | 455 |
| 17338001 | ventricular premature beats | VPB | 36 | 357 |
| 713426002 | incomplete right bundle branch block | IRBBB | 29 | 407 |
| 251146004 | low qrs voltages | LQRSV | 29 | 374 |
| 698252002 | nonspecific intraventricular conduction disorder | NSIVCB | 25 | 203 |
| 164931005 | st elevation | STE | 20 | 134 |
| 164890007 | atrial flutter | AFL | 18 | 186 |
| 164909002 | left bundle branch block | LBBB | 18 | 231 |
| 253352002 | left atrial abnormality | LAA | 16 | 72 |
| 428417006 | early repolarization | ERe | 16 | 140 |
| 47665007 | right axis deviation | RAD | 13 | 83 |
| 445118002 | left anterior fascicular block | LAnFB | 13 | 180 |
| 233917008 | av block | AVB | 11 | 74 |
| 89792004 | right ventricular hypertrophy | RVH | 7 | 86 |
| 266249003 | ventricular hypertrophy | VH | 7 | 71 |
| 251268003 | atrial pacing pattern | AP | 6 | 52 |
| 429622005 | st depression | STD | 5 | 38 |
| 195126007 | atrial hypertrophy | AH | 5 | 60 |
| 251120003 | incomplete left bundle branch block | ILBBB | 5 | 86 |
| 6374002 | bundle branch block | BBB | 4 | 116 |
| 253339007 | right atrial abnormality | RAAb | 3 | 14 |

## Input note

Input table lists the first 3 g*/RECORDS files and the map files; all 999 headers are logged in results/download_manifest.csv.
