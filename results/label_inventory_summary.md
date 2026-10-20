# Label inventory summary (local observation of the downloaded files)

- Script: `src/stemi/review/label_inventory.py`; one CSV per dataset: `results/label_inventory_<dataset>.csv`.
- Labels are listed as written; nothing is mapped or converted here (L1, L2).
- Challenge sources: `count` = publisher's count as listed in dx_mapping (meaning not defined by the publisher); `extra_count` = g1 sample (999 headers).

| dataset_id | label_kind | distinct_labels | labels_with_count_gt_0 | count_type | extra_count_type |
|---|---|---|---|---|---|
| ptb_xl | SCP statement (diagnostic) | 40 | 40 | records (ECGs with the code at any likelihood) | records at likelihood 100 |
| ptb_xl | SCP statement (form) | 15 | 15 | records (ECGs with the code at any likelihood) | records at likelihood 100 |
| ptb_xl | SCP statement (rhythm) | 12 | 12 | records (ECGs with the code at any likelihood) | records at likelihood 100 |
| ptb_xl | SCP statement (diagnostic/form) | 4 | 4 | records (ECGs with the code at any likelihood) | records at likelihood 100 |
| mimic_iv_ecg | machine report statements | 1 | not checked | not checked | - |
| ptb_diagnostic | header comment: Reason for admission | 15 | 15 | records | - |
| ptb_diagnostic | header comment: Acute infarction (localization) | 16 | 16 | records | - |
| ptb_diagnostic | header comment: Former infarction (localization) | 18 | 18 | records | - |
| sph | AHA primary statement | 44 | 44 | records | - |
| sph | AHA statement + modifier | 25 | 25 | records | - |
| cpsc_2018 | SNOMED CT code (dx_mapping_scored.csv) | 30 | 6 | publisher's count as listed | sample (g1, 999) |
| cpsc_2018 | SNOMED CT code (dx_mapping_unscored.csv) | 103 | 3 | publisher's count as listed | sample (g1, 999) |
| cpsc_extra | SNOMED CT code (dx_mapping_scored.csv) | 30 | 23 | publisher's count as listed | sample (g1, 999) |
| cpsc_extra | SNOMED CT code (dx_mapping_unscored.csv) | 103 | 49 | publisher's count as listed | sample (g1, 999) |
| georgia | SNOMED CT code (dx_mapping_scored.csv) | 30 | 25 | publisher's count as listed | sample (g1, 999) |
| georgia | SNOMED CT code (dx_mapping_unscored.csv) | 103 | 42 | publisher's count as listed | sample (g1, 999) |
| chapman_shaoxing | SNOMED CT code (dx_mapping_scored.csv) | 30 | 19 | publisher's count as listed | sample (g1, 999) |
| chapman_shaoxing | SNOMED CT code (dx_mapping_unscored.csv) | 103 | 35 | publisher's count as listed | sample (g1, 999) |
| ningbo | SNOMED CT code (dx_mapping_scored.csv) | 30 | 28 | publisher's count as listed | sample (g1, 999) |
| ningbo | SNOMED CT code (dx_mapping_unscored.csv) | 103 | 52 | publisher's count as listed | sample (g1, 999) |
| code15 | boolean label column | 7 | 7 | records (exams) | - |
| incart | patient diagnosis (raw text) | 7 | 7 | records | - |
| incart | patient diagnosis term (raw text split on commas) | 3 | 3 | records | - |
| incart | record description term | 56 | 56 | records | - |
