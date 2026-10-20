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
| PTB-XL | 71 SCP-ECG report codes; diagnosis codes have a wording-based "likelihood"; infarct stage (new/old), filled in mainly for MI-coded ECGs [PN-PTBXL; WAGNER2020; OBS-PTBXL] | Up to 2 cardiologists; about 31% of first reports were written by the ECG machine [PN-PTBXL; WAGNER2020] | PTB (Physikalisch-Technische Bundesanstalt); Oct 1989 – Jun 1996; 18,869 patients; country not stated on the dataset page [PN-PTBXL; WAGNER2020] | Not found (site names are hidden) [PN-PTBXL; WAGNER2020] | Schiller AG, 11 device types; 12 leads; 500 Hz (first recorded at 400 Hz); 10 s [WAGNER2020; PN-PTBXL] | No. Only "MI" report statements: 5,469 ECGs [OBS-PTBXL] | Not STEMI vs NSTEMI. Maybe MI vs non-MI after doctor review; pretraining. *Planner view, needs supervisor sign-off* | Same rate, length and leads as the planned model input; has patient IDs. Full check later (S10) [PN-PTBXL] | Open, no login [PN-PTBXL] | 21,799 ECGs; 3.0 GB; CC BY 4.0 [PN-PTBXL] |
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
| PTB-XL | 14 "MI" report codes (5 of them are "injury" codes) [OBS-PTBXL] | 5,469 ECGs from 4,670 patients [OBS-PTBXL] | Partly. 150 MI-coded ECGs have an "early" stage; 3,372 have stage "unknown" [OBS-PTBXL] | No. No code says STEMI or NSTEMI [OBS-PTBXL] |
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

**In one line:** a large, open set of 10-second clinical 12-lead ECGs. Its report codes come from cardiologists or from the ECG machine, and people checked most of the records. It has "MI" report statements, but nothing that says STEMI or NSTEMI.

1. **Labels.** Each ECG has codes from a standard list called SCP-ECG (a standard set of codes for ECG report statements). There are 71 codes. They describe the diagnosis, the shape of the wave, and the heart rhythm [PN-PTBXL]. Each code comes with a "likelihood" from 0 to 100 [OBS-PTBXL]. This number shows how sure **the wording of the report** sounds. It does not show how sure a doctor was. It was taken from key words in the report: for example "cannot rule out" = 15, "possible" = 50, "consistent with" = 100 [WAGNER2020, Table 4]. Only diagnosis codes have a likelihood. Shape and rhythm codes are set to 0, and so are diagnosis codes whose report gives no certainty word [WAGNER2020, Table 4]. Careful: the German words "Zustand nach" ("status post", meaning a past event) also give 100. **So likelihood 100 does not mean a new heart attack** [WAGNER2020, Table 4]. The codes fall into groups. One group is "MI" (14 codes). Other groups are ST/T changes (13 codes), conduction problems (11), enlarged heart (5), normal (1), and codes with no group (27) [OBS-PTBXL]. There is also an "infarct stage" field (whether a heart attack looks new or old). It is empty for 16,187 of the 21,799 ECGs. It is filled in mainly for ECGs with MI statements, and every ECG with an MI code has a value [OBS-PTBXL]. Other fields give the heart's electrical direction and a free-text report [OBS-PTBXL]. Every ECG has at least one code [OBS-PTBXL].
2. **Who labelled them.** "Up to two cardiologists" (heart doctors) [PN-PTBXL]. The first report was written by a cardiologist for 67.13% of ECGs. For 31.2%, the ECG machine wrote it automatically (figures from the first release) [WAGNER2020]. The second check was not independent. The second person checked the first person's work [WAGNER2020]. In release 1.0.3, the files mark 16,056 ECGs (73.65%) as checked by a person. The authors call this a cautious (low) estimate [WAGNER2020; OBS-PTBXL]. 6,813 ECGs (31.25%) are marked as having a machine-written first report. 555 (2.55%) had a second opinion [OBS-PTBXL].
3. **Collection.** The ECGs come from PTB (Physikalisch-Technische Bundesanstalt). They were recorded with Schiller AG machines between October 1989 and June 1996 [PN-PTBXL; WAGNER2020]. The country is not stated on the dataset page [PN-PTBXL]. The page calls them "clinical 12-lead ECGs" [PN-PTBXL]. Release 1.0.3 has 21,799 ECGs from 18,869 patients. 2,111 patients have more than one ECG (at most 10) [OBS-PTBXL]. 11,354 ECGs are from men and 10,445 from women. Age is shown as "300" for people aged 90 or older (293 ECGs) [OBS-PTBXL; WAGNER2020]. **Do not use the recording dates to find years.** The dates were moved by a random amount for each patient, and the stored years run from 1984 to 2001 [WAGNER2020; OBS-PTBXL].
4. **Setting.** **Not found.** We looked at the dataset page and the paper. They only say that the recording site ("hospital etc.") was hidden ("pseudonymised") [PN-PTBXL; WAGNER2020]. The file has 51 different site numbers [OBS-PTBXL]. Nothing says ambulance, emergency room, ward or clinic.
5. **Device.** Schiller AG machines, 11 device types [WAGNER2020]. The most common device names are "CS100 3" (6,140 ECGs), "CS-12" (4,048) and "AT-6 C 5.5" (3,950) [OBS-PTBXL]. The ECGs were first recorded at 400 Hz (400 measurements per second) [WAGNER2020]. They are shared at 500 Hz and also at 100 Hz. The 100 Hz files are the same ECGs, not extra ones [PN-PTBXL]. 12 leads (12 views of the heart), 10 seconds [PN-PTBXL]. We opened 20 header files as a sample. All 20 had the lead order I, II, III, AVR, AVL, AVF, V1–V6, 500 Hz, 5,000 samples, and units in millivolts. This is a small sample and may not hold for every file [OBS-PTBXL].
6. **STEMI vs NSTEMI.** **No.** No code says STEMI or NSTEMI [OBS-PTBXL]. There are 14 "MI" report statements. Five of them are "subendocardial injury" codes (damage to the inner layer of the heart wall) [OBS-PTBXL]. 5,469 ECGs from 4,670 patients have at least one of them. For 2,975 ECGs, the report wording gave likelihood 100 [OBS-PTBXL]. This can include "status post" (a past event), so it does not mean a new heart attack [WAGNER2020, Table 4]. Counts per code: IMI 2,676; ASMI 2,357; ILMI 478; AMI 353; ALMI 288; INJAS 214; LMI 201; INJAL 145; IPLMI 51; IPMI 33; INJIN 18; INJLA 17; PMI 17; INJIL 15 [OBS-PTBXL]. The infarct stage helps a little. Stage I means "acute, early" and Stage III means "old" [WAGNER2020]. 150 MI-coded ECGs (128 patients) are at Stage I or I–II. 3,372 MI-coded ECGs have stage "unknown" [OBS-PTBXL]. The 150 ECGs are **a list for clinical review**, not acute-MI labels. 28 ECGs have a general "ST elevation" code and 1,009 have "ST depression". These codes belong to the ST/T group, not to the MI group [OBS-PTBXL]. All of these are statements in an ECG report. They are not a confirmed diagnosis of a heart attack (`data_contract.md` L2, L3). **So PTB-XL gives "MI statement or not" only, not STEMI vs NSTEMI.**
7. **Best model use.** *This is the planner's view. The clinical supervisor still needs to agree.* Not a STEMI-vs-NSTEMI source. It could be an MI-vs-non-MI source, but only after doctors review the MI statements. An ECG with no MI code does not prove "no heart attack". Usable for pretraining (`data_contract.md` L1–L4, L11).
8. **Combining.** *(Partial. The full check comes in step S10.)* 500 Hz, 10 seconds and 12 standard leads. This matches the planned model input, so no change of speed is needed [PN-PTBXL; `data_contract.md` C1.3]. Each ECG has a patient number, so one patient can be kept in one group (training or testing). The data also comes already split into 10 groups ("folds") [OBS-PTBXL]. Count the 100 Hz copies once, not twice (`data_contract.md` O2). A copy of PTB-XL inside the 2021 PhysioNet Challenge has 21,837 recordings, which is the first-release count [PN-CHALLENGE2021]. Do not mix it with release 1.0.3 before checking which ECGs are the same (`data_contract.md` O8).
9. **Access.** Open. "Anyone can access the files, as long as they conform to the terms of the specified license" [PN-PTBXL]. We needed no login to download [OBS-DOWNLOAD].
10. **Size and license.** 21,799 ECGs from 18,869 patients (release 1.0.3); 3.0 GB unpacked; license CC BY 4.0 (free to use if you credit the authors); DOI 10.13026/kfzx-aw45; published 9 Nov 2022 [PN-PTBXL]. The paper describes the first release: 21,837 ECGs from 18,885 patients [WAGNER2020]. Do not mix the two counts (`data_contract.md` O8).

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

- **[PN-PTBXL]** PTB-XL, release 1.0.3, PhysioNet. https://physionet.org/content/ptb-xl/1.0.3/ (checked 2026-10-20).
- **[WAGNER2020]** Wagner P. et al. "PTB-XL, a large publicly available electrocardiography dataset." *Scientific Data*, 2020. https://pmc.ncbi.nlm.nih.gov/articles/PMC7248071/ (sections used: Methods > Data acquisition; Methods > Preprocessing; Data Records, Table 2; Table 11; Technical Validation > Quality Assessment for Annotation Data; Abstract).
- **[PN-CHALLENGE2021]** PhysioNet/Computing in Cardiology Challenge 2021, release 1.0.3. https://physionet.org/content/challenge-2021/1.0.3/ (checked 2026-10-20).

### Result files made by this team

All are in `results/`. Each one describes the files we downloaded on 2026-10-20, not every copy of the dataset.

- **[OBS-PTBXL]** PTB-XL counts: `ptb_xl_summary.md`, `ptb_xl_scp_counts.csv`, `ptb_xl_field_counts.csv`, `ptb_xl_mi_by_stadium.csv`, `ptb_xl_mi_early_stadium.csv`, `ptb_xl_headers.csv` (recounted by the planner).
- **[OBS-DOWNLOAD]** `download_manifest.csv`: what was downloaded, from where, and its checksum.
- All checked facts: `verified_facts.md`.
