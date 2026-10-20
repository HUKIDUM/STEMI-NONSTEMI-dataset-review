# ECG Datasets for STEMI vs NSTEMI Prediction: A Source-Checked Review

[![tests](https://github.com/HUKIDUM/STEMI-NONSTEMI-dataset-review/actions/workflows/tests.yml/badge.svg)](https://github.com/HUKIDUM/STEMI-NONSTEMI-dataset-review/actions/workflows/tests.yml)
[![Code license: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Report license: CC BY 4.0](https://img.shields.io/badge/report-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

A data-analysis-stage review for research on AI prediction of **acute STEMI vs NSTEMI vs non-MI** from 12-lead ECGs.
It answers three questions for 11 public ECG datasets:

1. Which datasets can be used, and for which model?
2. Which datasets can be combined, and which must not be?
3. What could mislead a model (weak labels, wrong setting, duplicated patients)?

Every fact in the report is traced to a source (PDF page, official dataset page, paper, or a count reproduced from downloaded metadata) and was independently re-checked before use.

**📄 Main result: [`docs/dataset_report.pdf`](docs/dataset_report.pdf)** (43 pages, plain English) · [Markdown version](docs/dataset_report.md)

---

## Key findings

> **No open dataset among the 11 has a STEMI or NSTEMI label.** The only possible route found is MIMIC-IV-ECG linked to credentialed MIMIC-IV hospital diagnosis codes, which is *not checked yet* (a count script is provided for credentialed users).

| Possible use (assessment for clinical review, not a decision) | Datasets |
|---|---|
| STEMI vs NSTEMI | None from open files; MIMIC-IV-ECG + credentialed ICD codes is the only route |
| MI statement vs no MI statement, after clinician review | PTB-XL, PTB Diagnostic, SPH, CPSC-Extra |
| External test (kept apart) | PTB Diagnostic, SPH |
| Pretraining | CODE-15%, Chapman-Shaoxing, Ningbo, CPSC 2018, Georgia, MIMIC-IV-ECG (unlabelled) |
| Not useful for supervised MI training | INCART (30-min Holter, 257 Hz) |

- **Acute / timing information is rare:** PTB Diagnostic is the only dataset with documented infarction dates (60 MI patients have an ECG 0–1 days after). PTB-XL marks 150 MI-coded ECGs as an early infarct stage; SPH has 7 "acute" MI statements; Ningbo has 49 "acute MI" labels of unknown origin.
- **Combining:** 0 of 55 dataset pairs can be pooled as-is; 45 need named checks (resampling, length policy, lead mapping by name, units, patient IDs, label mapping, overlap); 10 (every pair with INCART) should not be pooled for MI training.
- **Traps found:** MIMIC-IV-ECG stores aVF before aVL and uses a different scale than PTB-XL (in our samples); CODE-15%'s `ST` column means sinus tachycardia; in the Chapman/Ningbo label list "AF" means atrial *flutter*; the Challenge 2021 copies of PTB-XL and PTB Diagnostic duplicate the original releases; five Challenge datasets have repeat patients but no patient ID.

## Datasets reviewed

| Dataset | Release reviewed | License | Source |
|---|---|---|---|
| PTB-XL | 1.0.3 | CC BY 4.0 | [PhysioNet](https://physionet.org/content/ptb-xl/1.0.3/) |
| MIMIC-IV-ECG | 1.0 | ODbL 1.0 | [PhysioNet](https://physionet.org/content/mimic-iv-ecg/1.0/) |
| PTB Diagnostic ECG Database | 1.0.0 | ODC-By 1.0 | [PhysioNet](https://physionet.org/content/ptbdb/1.0.0/) |
| SPH (Shandong Provincial Hospital) | figshare collection 5779802 v1 | CC0 (data) | [figshare](https://doi.org/10.6084/m9.figshare.c.5779802.v1) |
| CODE-15% | Zenodo 4916206 | CC BY 4.0 | [Zenodo](https://zenodo.org/records/4916206) |
| CPSC 2018, CPSC-Extra, Georgia, Ningbo, Chapman-Shaoxing | PhysioNet/CinC Challenge 2021, 1.0.3 | CC BY 4.0 | [PhysioNet](https://physionet.org/content/challenge-2021/1.0.3/) |
| INCART 12-lead Arrhythmia Database | 1.0.0 | ODC-By 1.0 | [PhysioNet](https://physionet.org/content/incartdb/1.0.0/) |

No ECG waveforms are included in this repository, and no credentialed data was ever downloaded or stored. Only small metadata/header samples were used locally (`data/samples/`, git-ignored); every download is logged in [`results/download_manifest.csv`](results/download_manifest.csv). Please cite the original datasets (see the report's *Sources* section) if you use these results.

## Repository layout

```
docs/
  dataset_report.pdf / .md   Main report (plain English)
  report_build/              Scripts that build the PDF and label tables
  agent_team.md              How the review was carried out
  project/                   Data contract, research plan, approved review plan, earlier task notes
19-oct-2026/                 The three earlier analysis reports the review builds on
src/stemi/review/            Review code: safe metadata fetcher, WFDB header parser,
                             one review script per dataset, overlap check, label inventory,
                             combination matrix, MIMIC ICD count script
src/stemi/                   Earlier pipeline code (registry, inventory, label mapping, synthetic demo)
tests/                       169 tests on synthetic fixtures (no real data needed)
results/                     Evidence: verified facts, per-dataset findings and counts,
                             label inventories, common-label crosswalk, combination matrix
STATUS.md                    Project status log (read first when resuming work)
```

Most useful evidence files:

- [`results/verified_facts.md`](results/verified_facts.md): every fact used in the report, with source and verification status
- [`results/dataset_summary.csv`](results/dataset_summary.csv): one row per dataset
- [`results/combine_matrix.csv`](results/combine_matrix.csv): which pairs can be combined and which checks they need
- [`results/label_crosswalk_common.csv`](results/label_crosswalk_common.csv): 21 common labels (normal, AF, LBBB, RBBB, LVH, MI, ST elevation, …) across the 11 datasets

## Getting started

Requires Python ≥ 3.11.

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/python -m pytest
```

The tests use synthetic fixtures only, so they run without any dataset download.

### MIMIC-IV STEMI/NSTEMI count (credentialed users only)

`src/stemi/review/mimic_icd_count.py` prints **aggregate counts only** (counts under 10 are suppressed; no IDs or dates) of ICD-10 I21/I22 and ICD-9 410 codes for MIMIC-IV-ECG records linked to hospital admissions. Run it yourself on files you downloaded under your own PhysioNet credentialing and data use agreement; do not share the input files.

```bash
.venv/bin/python -I src/stemi/review/mimic_icd_count.py \
  --diagnoses <hosp/diagnoses_icd.csv.gz> --admissions <hosp/admissions.csv.gz> \
  --records <mimic-iv-ecg/record_list.csv> --versions "MIMIC-IV <x.y>; MIMIC-IV-ECG 1.0"
```

## Limitations

- This is a documentary and metadata review. No model was trained and no ECG signals were analysed.
- Cross-dataset label matching (`results/label_crosswalk_common.csv`) is the authors' mapping by meaning, not a publisher mapping, and needs clinical review.
- Counts for the five Challenge datasets are the publisher's per-code counts plus a one-folder sample (~1,000 headers each), not full re-counts.
- Overlap between datasets was checked by record IDs and counts only; no signal-level duplicate detection was done.
- Open decisions for the clinical supervisor (STEMI/NSTEMI code list, definition of "acute", evidence for non-MI, splitting datasets without patient IDs) are listed in section 9 of the report.

## How this was made

The review was carried out by an AI agent team (Claude Code: a planner/checker, a coder and a documenter, coordinated by a lead agent), with the researcher approving the plan, every download and every scope decision. Every finding was re-checked by the planner against its source before the documenter could use it. See [`docs/agent_team.md`](docs/agent_team.md).

## License

- Code: [MIT](LICENSE)
- Report and documentation (`docs/`, `results/`): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- The datasets themselves remain under their own licenses (table above).
