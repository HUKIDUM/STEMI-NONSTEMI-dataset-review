# ECG Datasets for STEMI and NSTEMI Prediction: A Simple Review

| | |
|---|---|
| Status | **SKELETON.** No dataset facts are filled in yet. |
| Date | 2026-10-20 |
| Written by | documenter (team: planner, coder, team-lead) |
| Plan | `PLAN.md` (approved by the user on 2026-10-20) |

<!-- section: A4 -->

## 1. Summary (one page)

*Waiting for verified facts. This page will answer three questions:*

1. Which datasets are best for telling STEMI from NSTEMI, and why?
2. Which datasets are only good for "MI or no MI", for pretraining, or for testing?
3. Which datasets can be combined?

Words used in this report:

- **ECG** (electrocardiogram): a recording of the heart's electrical activity.
- **MI** (myocardial infarction): a heart attack. Part of the heart muscle dies because blood flow stops.
- **STEMI** (ST-elevation MI): a heart attack where the ECG shows a raised "ST segment" (one part of the ECG wave).
- **NSTEMI** (non-ST-elevation MI): a heart attack where the ECG does not show this raised ST segment.
- **Non-MI**: the patient did not have a heart attack.
- **Acute**: happening now (new), not an old heart attack from the past.
- **Label**: the answer attached to each ECG that a model learns from (for example "STEMI").

## 2. How this review was done

- **Goal.** We checked 11 ECG datasets. For each one, we asked 10 questions (see the table in section 3). We judged each dataset by one thing: can it help a model tell STEMI from NSTEMI, and both from non-MI? (`PLAN.md` §0)
- **Where the facts come from.** Three earlier reports (PDF files dated October 2026), the official dataset web pages, and the papers that describe each dataset. (`PLAN.md` §2)
- **What we downloaded.** Only small description files: tables about the ECGs and the short "header" file of each recording (a header is a small text file that says how the ECG was stored). We did **not** download the ECG signals themselves. (`PLAN.md` §3)
- **What we did not use.** Some data needs a special login and a signed agreement ("credentialed access"). The team did not use any of it. For MIMIC, the user will run a small counting script on their own computer, and that script only gives totals. (`STATUS.md`, user answer U1)
- **Counts.** All counts in this report come from the files we downloaded. They describe those files on the download date. They do not describe every copy of the dataset. (`PLAN.md` §0)
- **The "verified" rule.** Every fact in this report was checked against its source by the planner. Each fact shows its source in square brackets. If we could not find something, we write **"not found"** and say where we looked. We never guess. (`PLAN.md` §0; `results/verified_facts.md`)
- **Labels are described, not made.** This review does not create training labels. Two rules matter most:
  - If an ECG has no heart-attack code, that does **not** prove the patient had no heart attack.
  - A computer-written ECG report, or a general "MI" note, is **not** the same as a doctor's STEMI or NSTEMI diagnosis.

  (`data_contract.md` rules L1, L2, L3)

<!-- section: A4-L -->

## 3. Summary table: 11 datasets × 10 questions

Short answers only. Details and sources are in section 5.

| Dataset | 1. Labels | 2. Who labelled | 3. Collection (where, when, who) | 4. Setting | 5. Device (brand, leads, rate, length) | 6. STEMI vs NSTEMI? | 7. Best model use | 8. Combine with | 9. Access | 10. Size and license |
|---|---|---|---|---|---|---|---|---|---|---|
| PTB-XL | | | | | | | | | | |
| MIMIC-IV-ECG | | | | | | not checked yet: needs credentialed access; the user will run the count script | | | | |
| PTB Diagnostic | | | | | | | | | | |
| SPH (Shandong) | | | | | | | | | | |
| CPSC 2018 | | | | | | | | | | |
| CPSC-Extra | | | | | | | | | | |
| Georgia | | | | | | | | | | |
| Ningbo | | | | | | | | | | |
| Chapman-Shaoxing | | | | | | | | | | |
| CODE-15% | | | | | | | | | | |
| INCART | | | | | | | | | | |

<!-- section: A4 -->

## 4. Heart-attack labels in each dataset

*Waiting for verified facts.* For each dataset: which labels are about heart attacks, how many ECGs have them, whether they say "new" or "old", and whether STEMI and NSTEMI can be told apart.

| Dataset | Heart-attack labels | Number of ECGs | New or old shown? | STEMI vs NSTEMI possible? |
|---|---|---|---|---|
| PTB-XL | | | | |
| MIMIC-IV-ECG | | not checked yet: needs credentialed access; the user will run the count script | | not checked yet: needs credentialed access; the user will run the count script |
| PTB Diagnostic | | | | |
| SPH (Shandong) | | | | |
| CPSC 2018 | | | | |
| CPSC-Extra | | | | |
| Georgia | | | | |
| Ningbo | | | | |
| Chapman-Shaoxing | | | | |
| CODE-15% | | | | |
| INCART | | | | |

## 5. Each dataset in detail

Each part answers the same 10 questions. Each answer gives its source.

### 5.1 PTB-XL

*Waiting for verified facts.*

### 5.2 MIMIC-IV-ECG

*Waiting for verified facts.* STEMI vs NSTEMI: not checked yet: needs credentialed access; the user will run the count script.

### 5.3 PTB Diagnostic

*Waiting for verified facts.*

### 5.4 SPH (Shandong Provincial Hospital)

*Waiting for verified facts.*

### 5.5 CPSC 2018

*Waiting for verified facts.*

### 5.6 CPSC-Extra

*Waiting for verified facts.*

### 5.7 Georgia

*Waiting for verified facts.*

### 5.8 Ningbo

*Waiting for verified facts.*

### 5.9 Chapman-Shaoxing

*Waiting for verified facts.*

### 5.10 CODE-15%

*Waiting for verified facts.*

### 5.11 INCART

*Waiting for verified facts.*

## 6. Which datasets to use for which model

*Waiting for verified facts.*

| Model | Datasets to use | Why |
|---|---|---|
| STEMI vs NSTEMI | | |
| MI vs non-MI | | |
| Pretraining only (the model first learns general ECG patterns, without heart-attack labels) | | |
| External test only (data kept apart, used only to check the finished model) | | |
| Not useful for this project | | |

## 7. Datasets that can and cannot be combined

*Waiting for verified facts.* "Combine" means putting two datasets together to train one model.

Key: **Yes** = can be combined. **After checks** = only after named checks. **No** = should not be combined. Each cell gives the reason (same patients, different labels, different recording speed, length or leads).

| | PTB-XL | MIMIC | PTB-Diag | SPH | CPSC | CPSC-Ex | Georgia | Ningbo | Chapman | CODE-15 | INCART |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PTB-XL | – | | | | | | | | | | |
| MIMIC | | – | | | | | | | | | |
| PTB-Diag | | | – | | | | | | | | |
| SPH | | | | – | | | | | | | |
| CPSC | | | | | – | | | | | | |
| CPSC-Ex | | | | | | – | | | | | |
| Georgia | | | | | | | – | | | | |
| Ningbo | | | | | | | | – | | | |
| Chapman | | | | | | | | | – | | |
| CODE-15 | | | | | | | | | | – | |
| INCART | | | | | | | | | | | – |

## 8. Warnings

Datasets that could mislead a model. *Waiting for verified facts.*

- **Wrong setting:** *(waiting)*. Example of the problem: ECGs recorded at home or over many hours look different from a 10-second ECG taken in hospital.
- **Weak labels:** *(waiting)*. Example of the problem: labels written by a computer, or labels that do not say whether the heart attack is new or old.
- **Same patients or same ECGs in two places:** *(waiting)*. Example of the problem: if the same ECG is in both the training data and the test data, the model looks better than it really is.

## 9. What is not known yet

*Waiting for verified facts.* Each "not found" item will be listed here, with where we looked and who could answer it.

## 10. Sources

*Will list every source used: the three PDFs (with page numbers), official web pages (with the date checked) and papers (with DOI or PMC link).*

### Earlier reports (in the folder `19-oct-2026/`)

- **[CMP]** `ECG_Dataset_Comparison_Simple_Report.pdf` (report date 16 Oct 2026).
- **[MCR]** `ECG_Metadata_Compatibility_Report.pdf` (analysis date 10 Oct 2026).
- **[NB]** `MI_Metadata_Compatibility_Colab.ipynb - Colab.pdf` (notebook run on 10 Oct 2026).

### Web pages and papers

*(waiting)*

### Result files made by this team

*(waiting)* The files are in `results/`.
