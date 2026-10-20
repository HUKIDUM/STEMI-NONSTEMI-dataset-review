# Challenge 2021 `cpsc_2018_extra` header review (local observation)

- Dataset: `cpsc_extra`, release PhysioNet Challenge 2021, 1.0.3
- Script: `src/stemi/review/review_challenge.py`; generated 2026-10-20T17:01:27+00:00
- Local observation of the downloaded file(s) named below; not a release-level fact (data_contract E2, E3). Labels are described, not converted into training labels (L1, L2).

## Input files

| local_path | url | sha256 | download_utc | checksum_match |
|---|---|---|---|---|
| data/samples/cpsc_extra/training/cpsc_2018_extra/g1/RECORDS | https://physionet.org/files/challenge-2021/1.0.3/training/cpsc_2018_extra/g1/RECORDS | 6445b26a2942196c3c3e6a0e67d4d1120a5d63dcdb96a4f9e5cc92d008c77ac7 | 2026-10-20T13:56:13+00:00 | not available |
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
| duration s min / median / max | 9.996 / 12 / 98 |
| duration s, top 5 values | 10: 400; 15: 65; 11: 60; 12: 53; 13: 36 |
| records with duration exactly 10 s | 400 |
| lead name sets | I|II|III|aVR|aVL|aVF|V1|V2|V3|V4|V5|V6 (999) |
| gains | 1000.0: 999 |
| units | mV: 999 |
| sex values | Male: 533; Female: 466 |
| age (numeric) min / median / max | -1 / 65 / 92 |
| age non-numeric values | none |
| comment keys | Age (999); Sex (999); Dx (999); Rx (999); Hx (999); Sx (999) |
| any patient-ID-like comment key | none found |
| distinct SNOMED codes | 49 |
| unmapped codes | none |
| map files used | ConditionNames_SNOMED-CT.csv, dx_mapping_scored.csv, dx_mapping_unscored.csv |

## Scope

**g1 sample only (999 of 1000 records listed in g1/RECORDS; not the full source).** `publisher_count_full_source` = the `CPSC_Extra` column of dx_mapping_*.csv (publisher's counts, meaning not defined by the publisher). Header checksums: not available (SHA256SUMS stream not approved); see results/download_manifest.csv.

## SNOMED codes whose name matches an MI / ST / ischaemia keyword (listing only; L2)

Records with any: 549. Keyword regexes: kw_infarct = `infarct|\bMI\b|STEMI`; kw_injury = `injury`; kw_st_elev = `ST[\s-]*(segment[\s-]*)?elev|\bSTE\b`; kw_st_depr = `ST[\s-]*(segment[\s-]*)?depr|\bSTD\b`; kw_ischemi = `isch[a]?emi`; kw_acute = `acute`; kw_q_wave = `q[\s-]*wave`; kw_st_other = `\bST[\s-]*T\b|\bST[\s-]*interval|\bST[\s-]*segment|non-?specific\s+ST`

| code | name | alt_name | abbreviation | n_records | publisher_count_full_source | map_source |
|---|---|---|---|---|---|---|
| 164867002 | old myocardial infarction |  | OldMI | 337 | 1168 | dx_mapping_unscored.csv |
| 164865005 | myocardial infarction | Myocardial infgraction in the front wall | Myocardial infraction in the lower wall | Myocardial infraction in the side wall | myocardial infraction in back wall | MI | 122 | 376 | dx_mapping_unscored.csv |
| 164861001 | myocardial ischemia |  | MIs | 101 | 384 | dx_mapping_unscored.csv |
| 413844008 | chronic myocardial ischemia |  | CMI | 45 | 161 | dx_mapping_unscored.csv |
| 164931005 | st elevation | ST tilt up | STE | 23 | 66 | dx_mapping_unscored.csv |
| 54329005 | anterior myocardial infarction |  | AnMI | 17 | 62 | dx_mapping_unscored.csv |
| 429622005 | st depression | ST drop down | STD | 11 | 57 | dx_mapping_unscored.csv |
| 413444003 | acute myocardial ischemia |  | AMIs | 1 | 1 | dx_mapping_unscored.csv |
| 704997005 | inferior ST segment depression |  | ISTD | 1 | 1 | dx_mapping_unscored.csv |

## Other ST codes for review (kw_st_other; NOT MI-related by themselves)

| code | name | alt_name | abbreviation | n_records | publisher_count_full_source |
|---|---|---|---|---|---|
| 428750005 | nonspecific st t abnormality | ST-T Change | NSSTTA | 384 | 1290 |
| 164930006 | st interval abnormal | ST extension | STIAb | 137 | 481 |

## All SNOMED codes (top 40 by records; full list in dx_counts.csv)

| code | name | abbreviation | n_records | publisher_count_full_source |
|---|---|---|---|---|
| 428750005 | nonspecific st t abnormality | NSSTTA | 384 | 1290 |
| 164867002 | old myocardial infarction | OldMI | 337 | 1168 |
| 164930006 | st interval abnormal | STIAb | 137 | 481 |
| 164865005 | myocardial infarction | MI | 122 | 376 |
| 426627000 | bradycardia | Brady | 102 | 271 |
| 164861001 | myocardial ischemia | MIs | 101 | 384 |
| 427084000 | sinus tachycardia | STach | 88 | 303 |
| 427172004 | premature ventricular contractions | PVC | 56 | 188 |
| 164873001 | left ventricular hypertrophy | LVH | 48 | 158 |
| 413844008 | chronic myocardial ischemia | CMI | 45 | 161 |
| 164889003 | atrial fibrillation | AF | 37 | 153 |
| 713427006 | complete right bundle branch block | CRBBB | 37 | 113 |
| 270492004 | 1st degree av block | IAVB | 33 | 106 |
| 713426002 | incomplete right bundle branch block | IRBBB | 24 | 86 |
| 164931005 | st elevation | STE | 23 | 66 |
| 63593006 | supraventricular premature beats | SVPB | 18 | 53 |
| 54329005 | anterior myocardial infarction | AnMI | 17 | 62 |
| 284470004 | premature atrial contraction | PAC | 17 | 73 |
| 251120003 | incomplete left bundle branch block | ILBBB | 15 | 42 |
| 195080001 | atrial fibrillation and flutter | AFAFL | 14 | 39 |
| 164909002 | left bundle branch block | LBBB | 14 | 38 |
| 164890007 | atrial flutter | AFL | 13 | 54 |
| 429622005 | st depression | STD | 11 | 57 |
| 446813000 | left atrial hypertrophy | LAH | 10 | 40 |
| 27885002 | complete heart block | CHB | 7 | 27 |
| 29320008 | atrioventricular junctional rhythm | AVJR | 5 | 6 |
| 446358003 | right atrial hypertrophy | RAH | 5 | 18 |
| 713422000 | atrial tachycardia | ATach | 5 | 15 |
| 17338001 | ventricular premature beats | VPB | 5 | 8 |
| 426995002 | junctional escape | JE | 4 | 4 |
| 65778007 | sinoatrial block | SAB | 3 | 9 |
| 89792004 | right ventricular hypertrophy | RVH | 3 | 20 |
| 426761007 | supraventricular tachycardia | SVT | 3 | 3 |
| 195060002 | ventricular pre excitation | VPEx | 3 | 6 |
| 251164006 | junctional premature complex | JPC | 2 | 2 |
| 426648003 | junctional tachycardia | JTach | 2 | 2 |
| 164896001 | ventricular fibrillation | VF | 2 | 10 |
| 75532003 | ventricular escape beat | VEsB | 2 | 3 |
| 413444003 | acute myocardial ischemia | AMIs | 1 | 1 |
| 370365005 | left ventricular strain | LVS | 1 | 1 |

## Input note

Input table lists the first 3 g*/RECORDS files and the map files; all 999 headers are logged in results/download_manifest.csv.
