# Findings: `code15` (CODE-15%, Zenodo record 4916206)

Author: coder, 2026-10-20. Status: **for planner verification**.

Source keys:
- **ZEN** = https://zenodo.org/records/4916206 (description) and https://zenodo.org/api/records/4916206 (license / access_right / file checksums), read 2026-10-20. The page text came through WebFetch (paraphrased, short quotes); please check it on the page.
- **PAPER** = Ribeiro et al. 2020, Nat Commun 11:1760, doi:10.1038/s41467-020-15432-4, https://pmc.ncbi.nlm.nih.gov/articles/PMC7145824/ (read 2026-10-20 through WebFetch). It describes the **full CODE** study data, not specifically the 15% subset.
- **OBS** = local observation of `data/samples/code15/exams.csv`, downloaded 2026-10-20 from https://zenodo.org/records/4916206/files/exams.csv (35,500,900 B; md5 matched the ZEN API checksum, `results/download_manifest.csv`). Made by `src/stemi/review/review_code15.py`.

| Key | Finding | Source |
|---|---|---|
| Q1 `labels` | Six boolean abnormality columns: `1dAVb`, `RBBB`, `LBBB`, `SB`, `AF`, `ST`, where **`ST` = sinus tachycardia, NOT ST elevation**. Plus `normal_ecg`, `death`, `timey`, `nn_predicted_age`. OBS True counts: 1dAVb 5,716; RBBB 9,672; LBBB 6,026; SB 5,605; ST 7,584; AF 7,033; normal_ecg 134,657; 173,347 exams have none of these True. | ZEN, column list ("1dAVb, RBBB, LBBB, SB, AF, ST … sinus tachycardia"); OBS `results/code15_label_counts.csv`, `results/code15_summary.md` |
| Q2 `labellers` | Full CODE: each exam had a Uni-G automatic analysis, Minnesota codes and a cardiologist's free-text report. Labels were extracted from the text and reconciled with the automatic classifiers by rules; about 34,512 unresolved exams were reviewed by medical students under a cardiologist's supervision. `normal_ecg` is "True if automatic annotation system say it is a normal ECG" (ZEN). Whether CODE-15% labels went through exactly this process is not stated on ZEN: **not found** for the subset. | PAPER, Methods (dataset / labelling); ZEN `normal_ecg` description |
| Q3 `collection` | Telehealth Network of Minas Gerais (TNMG), Brazil; CODE collected **2010–2016**; exams "performed mostly in primary care facilities". 345,779 exams / 233,770 patients (OBS = ZEN); 66,929 patients have >1 exam (max 38). | ZEN; PAPER, Methods; OBS `results/code15_summary.md` |
| Q4 `setting` | **Primary care** (mostly), via tele-ECG. | PAPER, Methods: "performed mostly in primary care facilities" |
| Q5 `device` | TEB ECGPC (Tecnologia Eletrônica Brasileira) and ErgoPC 13 (Micromed) in full CODE; original 300–600 Hz, 7–10 s. Released tracings: 400 Hz, 12 leads (DI, DII, DIII, AVR, AVL, AVF, V1–V6), stored as N × 4096 × 12 with zero-padding at both ends (7 s → 2,800 samples + 648 zeros each side). Amplitude units: **not found** on ZEN (contract C2.2: calibration unresolved). | PAPER, Methods; ZEN, tracing description |
| Q6 `stemi_nstemi` | **Neither.** No MI, ischaemia or ST-segment label (OBS: no column name matches `infarct|mi|stemi|ischem|isquem|injury|st_elev`; the only "ST" column is sinus tachycardia). PAPER: MI was not labelled or tested ("did not test the accuracy of the DNN in the diagnosis of other classes"). | OBS `results/code15_summary.md` "column names matching MI regex: none"; ZEN; PAPER, Discussion |
| Q7 `model_use` | ASSUMPTION (coder proposal): **pretraining only** (L11), or not useful for the MI task. It also needs an amplitude-calibration check and a 400 Hz → target-rate conversion. | Q6; contract L11, C2.2 |
| Q8 `combine` | Preliminary (final in S10): 400 Hz (resampling needed), 7–10 s with padding (padding mask needed, P2), Brazilian primary care, `patient_id` present (patient-level grouping possible). No label overlap with the MI task. No known record overlap with the other 10 sources. The CODE test set (zenodo 3625006) and the full CODE are related releases (contract O10c). | ZEN; PAPER; contract C2.2, P2, O10 |
| Q9 `access` | CODE-15%: **open** (ZEN `access_right` "open"; downloaded without login). Full CODE training data: restricted, "Requests to access the training data will be considered on an individual basis", for non-commercial research under data use agreements. | ZEN API; PAPER, Data availability |
| Q10 `size_license` | 345,779 exams / 233,770 patients; `exams.csv` 35.5 MB plus 18 `exams_part*.zip` (about 2.7 GB each; ZEN says about 46.3 GB of HDF5 in total); **CC BY 4.0**. | ZEN API `license.id` = "cc-by-4.0", `files[].size`; OBS |

## Notes for planner

1. `death` is missing (NaN) for 112,132 rows. ZEN says death/timey are filled only for each patient's first exam (OBS `results/code15_label_counts.csv`).
2. `trace_file` has 18 distinct values (exams_part0–17), with 5,779–20,000 exams per file (OBS).
