# CODE-15% exams.csv review (local observation)

- Dataset: `code15`, release Zenodo 4916206
- Script: `src/stemi/review/review_code15.py`; generated 2026-10-20T11:55:19+00:00
- Local observation of the downloaded file(s) named below; not a release-level fact (data_contract E2, E3). Labels are described, not converted into training labels (L1, L2).

## Input files

| local_path | url | sha256 | download_utc | checksum_match |
|---|---|---|---|---|
| data/samples/code15/exams.csv | https://zenodo.org/records/4916206/files/exams.csv | f9f82f4c07c1793e2285915c69f1113f5a7db8a0f2cf2f4b90474502f406bc35 | 2026-10-20T11:52:27+00:00 | yes |

## Basic counts

| item | value |
|---|---|
| columns | exam_id, age, is_male, nn_predicted_age, 1dAVb, RBBB, LBBB, SB, ST, AF, patient_id, death, timey, normal_ecg, trace_file |
| rows | 345779 |
| distinct exam_id | 345779 |
| distinct patient_id | 233770 |
| boolean columns | is_male, 1dAVb, RBBB, LBBB, SB, ST, AF, death, normal_ecg |
| column names matching MI regex | none |
| exams per patient: min / median / max | 1 / 1 / 38 |
| patients with >1 exam | 66929 |
| distinct trace_file | 18 |
| exams per trace_file min / max | 5779 / 20000 |
| exams with none of ['1dAVb', 'RBBB', 'LBBB', 'SB', 'ST', 'AF', 'normal_ecg'] True | 173347 |

## Boolean columns (labels and other flags)

| column | n_true | n_missing | n_patients_true | name_matches_mi_regex |
|---|---|---|---|---|
| is_male | 139203 | 0 | 94807 | False |
| 1dAVb | 5716 | 0 | 4701 | False |
| RBBB | 9672 | 0 | 6672 | False |
| LBBB | 6026 | 0 | 4193 | False |
| SB | 5605 | 0 | 4976 | False |
| ST | 7584 | 0 | 6894 | False |
| AF | 7033 | 0 | 4799 | False |
| death | 8341 | 112132 | 8341 | False |
| normal_ecg | 134657 | 0 | 109623 | False |
