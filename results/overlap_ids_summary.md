# Release overlap by ID (local observation)

- Dataset: `ptb_xl, ptb_diagnostic, cpsc_2018, cpsc_extra`, release native vs Challenge 2021 1.0.3
- Script: `src/stemi/review/overlap_ids.py`; generated 2026-10-20T17:44:21+00:00
- Local observation of the downloaded file(s) named below; not a release-level fact (data_contract E2, E3). Labels are described, not converted into training labels (L1, L2).

## Input files

| local_path | url | sha256 | download_utc | checksum_match |
|---|---|---|---|---|
| data/samples/ptb_xl/ptbxl_database.csv | https://physionet.org/files/ptb-xl/1.0.3/ptbxl_database.csv | 7600de9c1b27d181d850b3c6038a35d7c3ddb6bb33b702e3a20252a6859d216b | 2026-10-20T10:12:37+00:00 | yes |
| data/samples/ptb_diagnostic/RECORDS | https://physionet.org/files/ptbdb/1.0.0/RECORDS | 1bdcd205432b66e98389e095c8ea9f2f642f79265a1874929a9cb6de270852fe | 2026-10-20T11:48:15+00:00 | yes |
| data/samples/ptb_xl/challenge-2021/RECORDS | https://physionet.org/files/challenge-2021/1.0.3/RECORDS | b8c72c997b559aaedb1f9a64f2ca17e3806027007468065dd38c591fbe35df18 | 2026-10-20T17:39:54+00:00 | not available |
| data/samples/ptb_xl/challenge-2021/training/ptb-xl/g1/RECORDS | https://physionet.org/files/challenge-2021/1.0.3/training/ptb-xl/g1/RECORDS | 1720a25df0dcfa575f47b899325708344dfc8ceb6fb7866dc4659694ad92fb64 | 2026-10-20T17:39:57+00:00 | not available |
| data/samples/ptb_diagnostic/challenge-2021/RECORDS | https://physionet.org/files/challenge-2021/1.0.3/RECORDS | b8c72c997b559aaedb1f9a64f2ca17e3806027007468065dd38c591fbe35df18 | 2026-10-20T17:41:39+00:00 | not available |
| data/samples/ptb_diagnostic/challenge-2021/training/ptb/g1/RECORDS | https://physionet.org/files/challenge-2021/1.0.3/training/ptb/g1/RECORDS | c1c3352454a487f10209beed953d1370d4d7515e443c4d57c342451422162fc0 | 2026-10-20T17:41:41+00:00 | not available |

## ID checks

| check | result |
|---|---|
| ptb_xl: native ecg_id count | 21799 |
| ptb_xl: challenge record names | 21837 |
| ptb_xl: challenge distinct names | 21837 |
| ptb_xl: challenge name prefixes | HR |
| ptb_xl: challenge numeric range | 1–21837 |
| ptb_xl: native ecg_id range | 1–21837 |
| ptb_xl: numbers in both (IF HRn = ecg_id n; ASSUMPTION) | 21799 |
| ptb_xl: challenge numbers not in native 1.0.3 | 38 |
| ptb_xl: native ecg_id not in challenge | 0 |
| ptb_xl: challenge-only numbers (first 40) | 137, 139, 140, 141, 142, 143, 145, 456, 458, 459, 461, 462, 2506, 2511, 3795, 3798, 3800, 3801, 3832, 5817, 7777, 7779, 7782, 9821, 9825, 9888, 11810, 11814, 11815, 11817, 11838, 13791, 13793, 13796, 13797, 13799, 15742, 18150 |
| ptb_diagnostic: native records | 549 |
| ptb_diagnostic: native patient folders | 290 |
| ptb_diagnostic: challenge record names | 516 |
| ptb_diagnostic: challenge name prefixes | S |
| ptb_diagnostic: challenge numeric range | 1–549 |
| ptb_diagnostic: challenge names equal to a native record stem | 0 |
| ptb_diagnostic: numbers 1..len(native RECORDS) missing from challenge | 334, 339, 349, 356, 357, 359, 368, 376, 378, 379, 383, 396, 398, 399, 407, 408, 413, 417, 418, 419, 420, 422, 424, 430, 492, 516, 517, 520, 523, 524, 525, 531, 537 |
| ptb_diagnostic: those native records IF Sn = n-th line of native RECORDS (ASSUMPTION) | patient119/s0001_re, patient125/s0006_re, patient136/s0205_re, patient143/s0333lre, patient144/s0341lre, patient146/s0007_re, patient154/s0170_re, patient162/s0193_re, patient164/s0024are, patient164/s0024bre, patient167/s0200_re, patient176/s0188_re, patient178/s0011_re, patient179/s0176_re, patient181/s0204are, patient181/s0204bre, patient186/s0293lre, patient190/s0040_re, patient190/s0041_re, patient191/s0340lre, patient192/s0048_re, patient194/s0310lre, patient196/s0002_re, patient200/s0405lre, patient249/s0484_re, patient271/s0509_re, patient272/s0510_re, patient275/s0513_re, patient278/s0528_re, patient278/s0529_re, patient278/s0530_re, patient281/s0537_re, patient285/s0544_re |
| ptb_diagnostic: record-level mapping | not possible from RECORDS alone (name forms differ); counts only |
| cpsc_2018: g1 RECORDS names (sample only) | 1000; prefixes A; numbers 1–1000 |
| cpsc_extra: g1 RECORDS names (sample only) | 1000; prefixes Q; numbers 1–1033 |
| cpsc_2018 vs cpsc_extra | different name prefixes in the g1 samples; this does not show that the ECGs are distinct (O5, O9: signal-level duplicates not assessed) |

## Limits

IDs and counts only. No waveforms were compared, so signal-level duplicates are not assessed (O9). Name-to-ID mappings marked ASSUMPTION are untested until headers are read.
