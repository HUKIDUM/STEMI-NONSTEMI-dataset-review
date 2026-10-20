# PTB-XL metadata review (local observation)

- Dataset: `ptb_xl`, release 1.0.3 (records500)
- Script: `src/stemi/review/review_ptbxl.py`; generated 2026-10-20T11:39:15+00:00
- Local observation of the downloaded file(s) named below; not a release-level fact (data_contract E2, E3). Labels are described, not converted into training labels (L1, L2).

## Input files

| local_path | url | sha256 | download_utc | checksum_match |
|---|---|---|---|---|
| data/samples/ptb_xl/ptbxl_database.csv | https://physionet.org/files/ptb-xl/1.0.3/ptbxl_database.csv | 7600de9c1b27d181d850b3c6038a35d7c3ddb6bb33b702e3a20252a6859d216b | 2026-10-20T10:12:37+00:00 | yes |
| data/samples/ptb_xl/scp_statements.csv | https://physionet.org/files/ptb-xl/1.0.3/scp_statements.csv | ad05b0b1fcae83bb1230755ad9cfc7c96f303feddc08a4a9ad5bdc9ca63bac8f | 2026-10-20T10:12:37+00:00 | yes |

## Basic counts

| item | value |
|---|---|
| ECG rows in ptbxl_database.csv | 21799 |
| distinct ecg_id | 21799 |
| distinct patient_id | 18869 |
| ECGs per patient: min / median / max | 1 / 1 / 10 |
| patients with >1 ECG | 2111 |
| ECGs with empty scp_codes | 0 |
| codes in scp_statements.csv | 71 |
| codes used in scp_codes | 71 |
| codes used but not in scp_statements.csv | none |
| filename_hr all under records500/ | True |
| recording_date year min / max (as stored) | 1984 / 2001 |
| age min / median / max (as stored) | 2 / 62 / 300 |

## MI-related SCP codes (listed for review only; L2: not STEMI/NSTEMI labels)

Selection: scp_statements.csv diagnostic_class == 'MI', or 'infarct'/'injury' in the statement text. ECGs with any listed code: 5469; patients: 4670; with any listed code at likelihood 100: 2975.

| code | description | diagnostic_class | diagnostic_subclass | n_ecgs | n_patients | n_lik_100 | n_lik_50_99 | n_lik_1_49 | n_lik_0 | kw_infarct | kw_injury |
|---|---|---|---|---|---|---|---|---|---|---|---|
| IMI | inferior myocardial infarction | MI | IMI | 2676 | 2355 | 1022 | 692 | 962 | 0 | True | False |
| ASMI | anteroseptal myocardial infarction | MI | AMI | 2357 | 2033 | 1522 | 485 | 350 | 0 | True | False |
| ILMI | inferolateral myocardial infarction | MI | IMI | 478 | 416 | 331 | 85 | 62 | 0 | True | False |
| AMI | anterior myocardial infarction | MI | AMI | 353 | 348 | 116 | 97 | 140 | 0 | True | False |
| ALMI | anterolateral myocardial infarction | MI | AMI | 288 | 243 | 200 | 46 | 42 | 0 | True | False |
| INJAS | subendocardial injury in anteroseptal leads | MI | AMI | 214 | 196 | 196 | 16 | 2 | 0 | False | True |
| LMI | lateral myocardial infarction | MI | LMI | 201 | 185 | 57 | 65 | 79 | 0 | True | False |
| INJAL | subendocardial injury in anterolateral leads | MI | AMI | 145 | 136 | 133 | 10 | 2 | 0 | False | True |
| IPLMI | inferoposterolateral myocardial infarction | MI | IMI | 51 | 50 | 31 | 15 | 5 | 0 | True | False |
| IPMI | inferoposterior myocardial infarction | MI | IMI | 33 | 28 | 28 | 5 | 0 | 0 | True | False |
| INJIN | subendocardial injury in inferior leads | MI | IMI | 18 | 17 | 17 | 1 | 0 | 0 | False | True |
| INJLA | subendocardial injury in lateral leads | MI | AMI | 17 | 17 | 14 | 2 | 1 | 0 | False | True |
| PMI | posterior myocardial infarction | MI | PMI | 17 | 17 | 4 | 9 | 4 | 0 | True | False |
| INJIL | subendocardial injury in inferolateral leads | MI | IMI | 15 | 14 | 15 | 0 | 0 | 0 | False | True |

## Listed MI/injury codes x infarction stadium (see ptb_xl_mi_by_stadium.csv)

| code | infarction_stadium1 | infarction_stadium2 | n_ecgs |
|---|---|---|---|
| ANY_LISTED_MI_OR_INJURY_CODE | unknown | <missing> | 3372 |
| ANY_LISTED_MI_OR_INJURY_CODE | Stadium II-III | <missing> | 910 |
| ANY_LISTED_MI_OR_INJURY_CODE | Stadium III | <missing> | 899 |
| ANY_LISTED_MI_OR_INJURY_CODE | Stadium I | <missing> | 116 |
| ANY_LISTED_MI_OR_INJURY_CODE | Stadium II | <missing> | 66 |
| ANY_LISTED_MI_OR_INJURY_CODE | Stadium III | Stadium III | 50 |
| ANY_LISTED_MI_OR_INJURY_CODE | Stadium I | Stadium I | 19 |
| ANY_LISTED_MI_OR_INJURY_CODE | Stadium II | Stadium II | 16 |
| ANY_LISTED_MI_OR_INJURY_CODE | Stadium I | Stadium III | 8 |
| ANY_LISTED_MI_OR_INJURY_CODE | Stadium II | Stadium III | 6 |
| ANY_LISTED_MI_OR_INJURY_CODE | Stadium I-II | <missing> | 4 |
| ANY_LISTED_MI_OR_INJURY_CODE | Stadium I | Stadium II | 3 |

## Early-stadium listing (values ['Stadium I', 'Stadium I-II'] as stored; review only, not acute labels)

| selection | n_ecgs | n_patients |
|---|---|---|
| any listed MI/injury code | 5469 | 4670 |
| any listed code AND stadium1 or stadium2 in ['Stadium I', 'Stadium I-II'] | 150 | 128 |
| any listed code at likelihood 100 AND early stadium | 137 | 118 |
| early stadium WITHOUT any listed code | 21 | 13 |
| any INJ* code (INJAL, INJAS, INJIL, INJIN, INJLA) | 323 | 293 |
| any INJ* code AND early stadium | 5 | 5 |

## Labelling / device / site fields (see ptb_xl_field_counts.csv)

| field | value | n_ecgs |
|---|---|---|
| validated_by_human | True | 16056 |
| validated_by_human | False | 5743 |
| initial_autogenerated_report | False | 14986 |
| initial_autogenerated_report | True | 6813 |
| second_opinion | False | 21244 |
| second_opinion | True | 555 |
| device | CS100    3 | 6140 |
| device | CS-12 | 4048 |
| device | AT-6 C 5.5 | 3950 |
| device | CS-12   E | 2878 |
| device | AT-6     6 | 2273 |
| device | AT-60    3 | 966 |
| device | AT-6 C 5.8 | 824 |
| device | AT-6 C | 514 |
| device | AT-6 C 5.0 | 80 |
| device | AT-6 C 5.3 | 67 |
| device | AT-6 C 5.6 | 59 |

Distinct `site` values: 51; distinct `validated_by` values: 12.

## Headers (20 seeded-sample files; not a release-level fact, E2)

| file | record_name | n_sig | fs | n_samples | duration_s | lead_names | gains | baselines | units | fmts | adc_res | n_comments |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| records500/00000/00218_hr.hea | 00218_hr | 12 | 500.0 | 5000 | 10.0 | I|II|III|AVR|AVL|AVF|V1|V2|V3|V4|V5|V6 | 1000.0 | 0 | mV | 16 | 16 | 0 |
| records500/00000/00640_hr.hea | 00640_hr | 12 | 500.0 | 5000 | 10.0 | I|II|III|AVR|AVL|AVF|V1|V2|V3|V4|V5|V6 | 1000.0 | 0 | mV | 16 | 16 | 0 |
| records500/01000/01429_hr.hea | 01429_hr | 12 | 500.0 | 5000 | 10.0 | I|II|III|AVR|AVL|AVF|V1|V2|V3|V4|V5|V6 | 1000.0 | 0 | mV | 16 | 16 | 0 |
| records500/01000/01732_hr.hea | 01732_hr | 12 | 500.0 | 5000 | 10.0 | I|II|III|AVR|AVL|AVF|V1|V2|V3|V4|V5|V6 | 1000.0 | 0 | mV | 16 | 16 | 0 |
| records500/01000/01938_hr.hea | 01938_hr | 12 | 500.0 | 5000 | 10.0 | I|II|III|AVR|AVL|AVF|V1|V2|V3|V4|V5|V6 | 1000.0 | 0 | mV | 16 | 16 | 0 |
| records500/01000/01976_hr.hea | 01976_hr | 12 | 500.0 | 5000 | 10.0 | I|II|III|AVR|AVL|AVF|V1|V2|V3|V4|V5|V6 | 1000.0 | 0 | mV | 16 | 16 | 0 |
| records500/02000/02319_hr.hea | 02319_hr | 12 | 500.0 | 5000 | 10.0 | I|II|III|AVR|AVL|AVF|V1|V2|V3|V4|V5|V6 | 1000.0 | 0 | mV | 16 | 16 | 0 |
| records500/06000/06450_hr.hea | 06450_hr | 12 | 500.0 | 5000 | 10.0 | I|II|III|AVR|AVL|AVF|V1|V2|V3|V4|V5|V6 | 1000.0 | 0 | mV | 16 | 16 | 0 |
| records500/06000/06667_hr.hea | 06667_hr | 12 | 500.0 | 5000 | 10.0 | I|II|III|AVR|AVL|AVF|V1|V2|V3|V4|V5|V6 | 1000.0 | 0 | mV | 16 | 16 | 0 |
| records500/07000/07308_hr.hea | 07308_hr | 12 | 500.0 | 5000 | 10.0 | I|II|III|AVR|AVL|AVF|V1|V2|V3|V4|V5|V6 | 1000.0 | 0 | mV | 16 | 16 | 0 |
| records500/08000/08500_hr.hea | 08500_hr | 12 | 500.0 | 5000 | 10.0 | I|II|III|AVR|AVL|AVF|V1|V2|V3|V4|V5|V6 | 1000.0 | 0 | mV | 16 | 16 | 0 |
| records500/11000/11351_hr.hea | 11351_hr | 12 | 500.0 | 5000 | 10.0 | I|II|III|AVR|AVL|AVF|V1|V2|V3|V4|V5|V6 | 1000.0 | 0 | mV | 16 | 16 | 0 |
| records500/12000/12093_hr.hea | 12093_hr | 12 | 500.0 | 5000 | 10.0 | I|II|III|AVR|AVL|AVF|V1|V2|V3|V4|V5|V6 | 1000.0 | 0 | mV | 16 | 16 | 0 |
| records500/13000/13596_hr.hea | 13596_hr | 12 | 500.0 | 5000 | 10.0 | I|II|III|AVR|AVL|AVF|V1|V2|V3|V4|V5|V6 | 1000.0 | 0 | mV | 16 | 16 | 0 |
| records500/14000/14870_hr.hea | 14870_hr | 12 | 500.0 | 5000 | 10.0 | I|II|III|AVR|AVL|AVF|V1|V2|V3|V4|V5|V6 | 1000.0 | 0 | mV | 16 | 16 | 0 |
| records500/15000/15471_hr.hea | 15471_hr | 12 | 500.0 | 5000 | 10.0 | I|II|III|AVR|AVL|AVF|V1|V2|V3|V4|V5|V6 | 1000.0 | 0 | mV | 16 | 16 | 0 |
| records500/18000/18523_hr.hea | 18523_hr | 12 | 500.0 | 5000 | 10.0 | I|II|III|AVR|AVL|AVF|V1|V2|V3|V4|V5|V6 | 1000.0 | 0 | mV | 16 | 16 | 0 |
| records500/18000/18903_hr.hea | 18903_hr | 12 | 500.0 | 5000 | 10.0 | I|II|III|AVR|AVL|AVF|V1|V2|V3|V4|V5|V6 | 1000.0 | 0 | mV | 16 | 16 | 0 |
| records500/19000/19309_hr.hea | 19309_hr | 12 | 500.0 | 5000 | 10.0 | I|II|III|AVR|AVL|AVF|V1|V2|V3|V4|V5|V6 | 1000.0 | 0 | mV | 16 | 16 | 0 |
| records500/20000/20629_hr.hea | 20629_hr | 12 | 500.0 | 5000 | 10.0 | I|II|III|AVR|AVL|AVF|V1|V2|V3|V4|V5|V6 | 1000.0 | 0 | mV | 16 | 16 | 0 |
