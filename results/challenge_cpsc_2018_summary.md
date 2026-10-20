# Challenge 2021 `cpsc_2018` header review (local observation)

- Dataset: `cpsc_2018`, release PhysioNet Challenge 2021, 1.0.3
- Script: `src/stemi/review/review_challenge.py`; generated 2026-10-20T17:01:26+00:00
- Local observation of the downloaded file(s) named below; not a release-level fact (data_contract E2, E3). Labels are described, not converted into training labels (L1, L2).

## Input files

| local_path | url | sha256 | download_utc | checksum_match |
|---|---|---|---|---|
| data/samples/cpsc_2018/training/cpsc_2018/g1/RECORDS | https://physionet.org/files/challenge-2021/1.0.3/training/cpsc_2018/g1/RECORDS | fd724514f15baf7d80515ff3c9b9f7fe43f8887e9af9c5e75a2fc7fd470a300b | 2026-10-20T12:43:43+00:00 | not available |
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
| duration s min / median / max | 9 / 12.092 / 118 |
| duration s, top 5 values | 10: 364; 15: 36; 14: 36; 20: 35; 12: 30 |
| records with duration exactly 10 s | 364 |
| lead name sets | I|II|III|aVR|aVL|aVF|V1|V2|V3|V4|V5|V6 (999) |
| gains | 1000.0: 999 |
| units | mV: 999 |
| sex values | Male: 521; Female: 478 |
| age (numeric) min / median / max | 7 / 64 / 92 |
| age non-numeric values | NaN: 1 |
| comment keys | Age (999); Sex (999); Dx (999); Rx (999); Hx (999); Sx (999) |
| any patient-ID-like comment key | none found |
| distinct SNOMED codes | 9 |
| unmapped codes | none |
| map files used | ConditionNames_SNOMED-CT.csv, dx_mapping_scored.csv, dx_mapping_unscored.csv |

## Scope

**g1 sample only (999 of 1000 records listed in g1/RECORDS; not the full source).** `publisher_count_full_source` = the `CPSC` column of dx_mapping_*.csv (publisher's counts, meaning not defined by the publisher). Header checksums: not available (SHA256SUMS stream not approved); see results/download_manifest.csv.

## SNOMED codes whose name matches an MI / ST / ischaemia keyword (listing only; L2)

Records with any: 145. Keyword regexes: kw_infarct = `infarct|\bMI\b|STEMI`; kw_injury = `injury`; kw_st_elev = `ST[\s-]*(segment[\s-]*)?elev|\bSTE\b`; kw_st_depr = `ST[\s-]*(segment[\s-]*)?depr|\bSTD\b`; kw_ischemi = `isch[a]?emi`; kw_acute = `acute`; kw_q_wave = `q[\s-]*wave`; kw_st_other = `\bST[\s-]*T\b|\bST[\s-]*interval|\bST[\s-]*segment|non-?specific\s+ST`

| code | name | alt_name | abbreviation | n_records | publisher_count_full_source | map_source |
|---|---|---|---|---|---|---|
| 429622005 | st depression | ST drop down | STD | 114 | 869 | dx_mapping_unscored.csv |
| 164931005 | st elevation | ST tilt up | STE | 31 | 220 | dx_mapping_unscored.csv |

## Other ST codes for review (kw_st_other; NOT MI-related by themselves)

| code | name | alt_name | abbreviation | n_records | publisher_count_full_source |
|---|---|---|---|---|---|

## All SNOMED codes (top 40 by records; full list in dx_counts.csv)

| code | name | abbreviation | n_records | publisher_count_full_source |
|---|---|---|---|---|
| 59118001 | right bundle branch block | RBBB | 270 | 1857 |
| 164889003 | atrial fibrillation | AF | 180 | 1221 |
| 426783006 | sinus rhythm | NSR | 135 | 918 |
| 429622005 | st depression | STD | 114 | 869 |
| 164884008 | ventricular ectopics | VEB | 102 | 700 |
| 270492004 | 1st degree av block | IAVB | 102 | 722 |
| 284470004 | premature atrial contraction | PAC | 99 | 616 |
| 164931005 | st elevation | STE | 31 | 220 |
| 164909002 | left bundle branch block | LBBB | 30 | 236 |

## Input note

Input table lists the first 3 g*/RECORDS files and the map files; all 999 headers are logged in results/download_manifest.csv.
