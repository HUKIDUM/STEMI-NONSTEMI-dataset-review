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
| SPH (Shandong) | AHA report statements: 44 main codes plus add-on words (like "acute", "old") [LIU2022; OBS-SPH] | Cardiologist's final report; all re-checked by an experienced cardiologist [LIU2022] | Shandong Provincial Hospital, Jinan, China; Aug 2019 – Aug 2020; adults; 24,666 patients [LIU2022; OBS-SPH] | Not found [LIU2022] | MedEx MECG-200; 12 leads; 500 Hz; 10–60 s [LIU2022] | No. "MI" statements in 260 ECGs; only 7 say "acute" [OBS-SPH] | Not STEMI vs NSTEMI. Maybe test set for "MI statement or not" after review; pretraining. *Planner view, needs supervisor sign-off* | Same rate and leads; longer ECGs need cutting; has patient IDs; different label system. Full check later (S10) [LIU2022] | Open, no login [FIGSHARE-SPH] | 25,770 ECGs; 2.28 GB of signals; data CC0, paper CC BY 4.0 [FIGSHARE-SPH; LIU2022] |
| CPSC 2018 | | | | | | | | | | |
| CPSC-Extra | | | | | | | | | | |
| Georgia | | | | | | | | | | |
| Ningbo | | | | | | | | | | |
| Chapman-Shaoxing | | | | | | | | | | |
| CODE-15% | 6 yes/no rhythm and conduction labels ("ST" = sinus tachycardia, **not** ST elevation), plus "normal ECG" and death [ZEN-CODE15] | Full CODE: computer reports plus text from expert reports; unclear cases checked by medical students with a cardiologist. For this 15% part: not found [RIBEIRO2020; ZEN-CODE15] | Telehealth Network of Minas Gerais, Brazil; 2010–2016; 233,770 patients [ZEN-CODE15; RIBEIRO2020] | Full CODE: mostly primary care (local health centres) [RIBEIRO2020] | TEB ECGPC or Micromed ErgoPC 13; 12 leads; 400 Hz as shared; 7–10 s, padded with zeros [RIBEIRO2020; ZEN-CODE15] | Neither. No MI label at all [OBS-CODE15; ZEN-CODE15] | Pretraining only, or not useful. *Planner view, needs supervisor sign-off* | Needs a speed change (400 Hz) and a padding mask; has patient IDs; no MI labels. Full check later (S10) [ZEN-CODE15] | Open, no login [ZEN-CODE15] | 345,779 ECGs; 46.3 GB (all files); CC BY 4.0 [ZEN-CODE15] |
| INCART | | | | | | | | | | |

<!-- section: A4 -->

## 4. Heart-attack labels in each dataset

*Waiting for verified facts.* For each dataset: which labels are about heart attacks, how many ECGs have them, whether they say "new" or "old", and whether STEMI and NSTEMI can be told apart.

| Dataset | Heart-attack labels | Number of ECGs | New or old shown? | STEMI vs NSTEMI possible? |
|---|---|---|---|---|
| PTB-XL | 14 "MI" report codes (5 of them are "injury" codes) [OBS-PTBXL] | 5,469 ECGs from 4,670 patients [OBS-PTBXL] | Partly. 150 MI-coded ECGs have an "early" stage; 3,372 have stage "unknown" [OBS-PTBXL] | No. No code says STEMI or NSTEMI [OBS-PTBXL] |
| MIMIC-IV-ECG | | not checked yet: needs credentialed access; the user will run the count script | | not checked yet: needs credentialed access; the user will run the count script |
| PTB Diagnostic | | | | |
| SPH (Shandong) | 4 "MI" codes (anterior, inferior, anteroseptal, extensive anterior) [OBS-SPH; LIU2022] | 260 ECGs from 242 patients [OBS-SPH] | Yes, as report words: "acute" 7 ECGs, "recent" 12, "old" 233, none 8 [OBS-SPH] | No. No statement says STEMI or NSTEMI [OBS-SPH] |
| CPSC 2018 | | | | |
| CPSC-Extra | | | | |
| Georgia | | | | |
| Ningbo | | | | |
| Chapman-Shaoxing | | | | |
| CODE-15% | None. The "ST" column means sinus tachycardia (a fast heart rhythm that starts in the heart's normal pacemaker), not ST elevation [ZEN-CODE15] | 0 [OBS-CODE15] | No [OBS-CODE15] | No [OBS-CODE15; RIBEIRO2020] |
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

**In one line:** an open set of adult ECGs from one Chinese hospital, re-checked by a cardiologist. It has "MI" statements with "acute / recent / old" words, but only 7 ECGs say "acute", and none says STEMI or NSTEMI.

1. **Labels.** The labels are standard report statements from the AHA (American Heart Association) list. There are 44 main codes, grouped A to M, plus add-on codes that change their meaning (codes 308–367, for example "acute" or "old"). One statement is a main code plus optional add-ons joined by "+". Several statements are separated by ";" [OBS-SPH; LIU2022, Table 2]. The most common are: normal ECG (13,905 ECGs), slow heart rhythm (sinus bradycardia, 2,711), T-wave abnormality (2,218) and ST deviation (1,829) [OBS-SPH].
2. **Who labelled them.** "The responsible cardiologist made the final diagnosis in consideration of the patient health record." Then "an experienced cardiologist re-checked all original diagnostic statements and made corrections" [LIU2022]. The statements were in Chinese. They were turned into AHA codes with translation rules. Any ECG with a statement that could not be translated was left out [LIU2022]. The MedEx system measured ECG features, but only as a reference for the doctors [LIU2022].
3. **Collection.** Shandong Provincial Hospital, Jinan, China. August 2019 to August 2020. Adults only (age above 18). 25,770 ECGs from 24,666 patients, with at most 5 ECGs per patient [LIU2022; OBS-SPH]. Ages 18–95. 14,265 ECGs are from men and 11,505 from women [OBS-SPH]. The stored dates were moved by a random amount for each patient, so they are not the real collection dates [LIU2022]. Whether patients were in hospital or outpatients: not found [LIU2022].
4. **Setting.** **Not found.** We read the full paper. It does not mention inpatients, outpatients, emergency care or health check-ups [LIU2022].
5. **Device.** MedEx MECG-200. 500 Hz. 12 leads in the order I, II, III, aVR, aVL, aVF, V1–V6 [LIU2022]. The paper says "the record length is between 10 and 60 seconds" [LIU2022]. In the file, lengths are 10 to 56 seconds, and 18,842 ECGs are exactly 10 seconds [OBS-SPH].
6. **STEMI vs NSTEMI.** **No.** No statement says STEMI or NSTEMI [OBS-SPH]. Four "MI" codes exist: anterior (160), inferior (161), anteroseptal (165) and extensive anterior (166) MI (these name the part of the heart that is damaged). 260 ECGs from 242 patients have one [OBS-SPH]. Time words on these MI statements [OBS-SPH]:
   - "Acute" (code 330): 7 ECGs (7 patients).
   - "Recent" (331): 12 ECGs (9 patients).
   - "Old" (332): 233 ECGs (219 patients).
   - No time word: 8 ECGs.

   Most MI statements are "old": for example inferior + old 114, anteroseptal + old 75, anterior + old 47 [OBS-SPH; LIU2022, Table 2]. "ST deviation" with "elevation" appears in 37 ECGs (34 patients). Only 1 ECG has both an acute MI statement and ST elevation [OBS-SPH]. **The word "acute" here is part of the written report. It is not a confirmed new heart attack.** These are report statements, not checked diagnoses (`data_contract.md` L2, L3). **So SPH gives "MI statement or not" only. New (acute) MI is far too rare to learn from.**
7. **Best model use.** *This is the planner's view. The clinical supervisor still needs to agree.* Not usable for STEMI vs NSTEMI (only 7 acute MI statements). It could be an external test set (data kept apart, used only to check a finished model) for "MI statement or not", after doctors review the statements. It could also be used for pretraining (`data_contract.md` L1, L4, L11).
8. **Combining.** *(Partial. The full check comes in step S10.)* 500 Hz and 12 leads match the planned model input (`data_contract.md` C1.3). The ECGs are 10–56 seconds long, so a rule for cutting them to the model's length is needed (`data_contract.md` Q9). Each ECG has a patient number. The paper warns against putting "records from the same patient" in both training and testing, and gives code to split them [LIU2022]. The label system (AHA) is different from PTB-XL (SCP-ECG) and the Challenge sets (SNOMED), so labels must be matched first [LIU2022]. The paper does not mention any overlap with other datasets [LIU2022].
9. **Access.** Open download from figshare. No login needed [FIGSHARE-SPH; OBS-DOWNLOAD].
10. **Size and license.** 25,770 ECGs from 24,666 patients [OBS-SPH]. The signal file `records.tar.gz` is about 2.28 GB (we did not download it). `metadata.csv` is about 1 MB [FIGSHARE-SPH]. The **data** is CC0 (no rights kept, free for any use) on figshare [FIGSHARE-SPH]. The **paper** is CC BY 4.0 [LIU2022]. Both are true: they apply to different things.

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

**In one line:** a very large, open set of Brazilian tele-ECGs (ECGs sent to a distant centre to be read). It has no heart-attack label of any kind.

1. **Labels.** Six yes/no labels: `1dAVb`, `RBBB`, `LBBB`, `SB`, `AF` and `ST` [ZEN-CODE15]. These are heart rhythm and conduction problems (problems with how the electrical signal travels). **Careful: `ST` means "sinus tachycardia" (a fast heart rhythm that starts in the heart's normal pacemaker). It does NOT mean ST elevation** [ZEN-CODE15]. There are also `normal_ecg` (set by an automatic system), `death`, `timey` (for the first exam only) and an age guessed by a computer model [ZEN-CODE15]. Number of "yes" answers: 1dAVb 5,716; RBBB 9,672; LBBB 6,026; SB 5,605; ST 7,584; AF 7,033; normal_ecg 134,657 [OBS-CODE15]. 308,004 exams have none of the six labels. 173,347 have none of the six and are also not marked "normal" [OBS-CODE15].
2. **Who labelled them.** For the full CODE dataset (the larger set this 15% comes from), labels came from three places: automatic statements from the Uni-G program, Minnesota codes (a standard coding system for ECGs), and "text labels extracted from the expert text reports" [RIBEIRO2020]. 34,512 unclear exams were "manually reviewed by medical students … under the supervision of a certified cardiologist" [RIBEIRO2020]. `normal_ecg` comes from an automatic system [ZEN-CODE15]. Whether the 15% part was labelled in exactly the same way: **not found**. The dataset page does not say [ZEN-CODE15].
3. **Collection.** Telehealth Network of Minas Gerais (TNMG), Brazil. It covers "811 out of the 853 municipalities" of the state. 2010 to 2016 [ZEN-CODE15; RIBEIRO2020]. 345,779 exams from 233,770 patients. 66,929 patients have more than one exam (at most 38) [OBS-CODE15].
4. **Setting.** For the full CODE dataset: "performed mostly in primary care facilities" (local health centres, not hospitals) [RIBEIRO2020]. For the 15% part, the paper's statement about full CODE is the only information we found.
5. **Device.** Full CODE: TEB ECGPC (Tecnologia Eletrônica Brasileira) or Micromed ErgoPC 13 machines. 7–10 seconds, first recorded at 300 to 600 Hz [RIBEIRO2020]. The shared files are all at 400 Hz. Each ECG is stored as 4,096 samples × 12 leads, in the order DI, DII, DIII, AVR, AVL, AVF, V1–V6 [ZEN-CODE15]. Shorter ECGs are filled with zeros at both ends. For example, a 7-second ECG has 2,800 real samples and 648 zeros at each end [ZEN-CODE15]. The unit of the stored numbers (for example millivolts): **not found** on the dataset page [ZEN-CODE15].
6. **STEMI vs NSTEMI.** **Neither.** There is no MI label, no ischaemia (low blood flow to the heart muscle) label, and no ST-segment label. The `ST` column is sinus tachycardia [OBS-CODE15; ZEN-CODE15]. The paper says it "did not test the accuracy of the DNN in the diagnosis of other classes", and names MI as future work [RIBEIRO2020].
7. **Best model use.** *This is the planner's view. The clinical supervisor still needs to agree.* Pretraining only, or not useful for the heart-attack task (`data_contract.md` L11). Before use, someone must check the number scale (units) and change the speed from 400 Hz to the model's rate (`data_contract.md` C2.2).
8. **Combining.** *(Partial. The full check comes in step S10.)* 400 Hz, so the speed must be changed. 7–10 seconds with zero padding, so the model needs a "padding mask" that marks which samples are not real (`data_contract.md` P2) [ZEN-CODE15]. Each exam has a patient number [OBS-CODE15]. Full CODE: mostly primary care [RIBEIRO2020]. There are no MI labels to combine. Related releases exist (full CODE and the CODE test set). Check for shared ECGs before using them together (`data_contract.md` O10).
9. **Access.** CODE-15% is open, and we downloaded it without a login [ZEN-CODE15; OBS-DOWNLOAD]. The full CODE training data is **not** open: "Restrictions apply to the availability of the training set". It needs an individual request, is for non-commercial use only, and needs a data use agreement [RIBEIRO2020].
10. **Size and license.** 345,779 exams from 233,770 patients. `exams.csv` is 35.5 MB. The signals are in 18 zip files (17 of about 2.7 GB each, plus one of 782.6 MB). All files together are 46.3 GB. License: CC BY 4.0 [ZEN-CODE15].

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

## Appendix A. Other datasets worth checking (not reviewed in depth)

*Waiting for verified facts.* This part will briefly list a few other public datasets that may have STEMI or NSTEMI labels. They were **not** reviewed like the 11 datasets above. They are not in the tables in sections 3 and 4, in the advice in section 6, or in the table in section 7.

## 10. Sources

*Will list every source used: the three PDFs (with page numbers), official web pages (with the date checked) and papers (with DOI or PMC link).*

### Earlier reports (in the folder `19-oct-2026/`)

- **[CMP]** `ECG_Dataset_Comparison_Simple_Report.pdf` (report date 16 Oct 2026).
- **[MCR]** `ECG_Metadata_Compatibility_Report.pdf` (analysis date 10 Oct 2026).
- **[NB]** `MI_Metadata_Compatibility_Colab.ipynb - Colab.pdf` (notebook run on 10 Oct 2026).

### Web pages and papers

- **[PN-PTBXL]** PTB-XL, release 1.0.3, PhysioNet. https://physionet.org/content/ptb-xl/1.0.3/ (checked 2026-10-20).
- **[WAGNER2020]** Wagner P. et al. "PTB-XL, a large publicly available electrocardiography dataset." *Scientific Data*, 2020. https://pmc.ncbi.nlm.nih.gov/articles/PMC7248071/ (sections used: Methods > Data acquisition; Methods > Preprocessing; Data Records, Table 2; Table 11; Technical Validation > Quality Assessment for Annotation Data; Abstract).
- **[LIU2022]** Liu H. et al., 2022, *Scientific Data* (the SPH dataset paper). https://pmc.ncbi.nlm.nih.gov/articles/PMC9174207/ (sections used: Abstract; Methods > Data acquisition; Methods > Data processing; Data Records; Table 2; Usage Notes; Open Access statement).
- **[FIGSHARE-SPH]** SPH data on figshare, collection 5779802. https://doi.org/10.6084/m9.figshare.c.5779802.v1 ; file list and licenses from https://api.figshare.com/v2/collections/5779802/articles (data articles 17912441, 17912444, 17912507; checked 2026-10-20).
- **[ZEN-CODE15]** CODE-15% on Zenodo, record 4916206. https://zenodo.org/records/4916206 and https://zenodo.org/api/records/4916206 (checked 2026-10-20).
- **[RIBEIRO2020]** Ribeiro A.H. et al., 2020 (the CODE dataset paper). https://pmc.ncbi.nlm.nih.gov/articles/PMC7145824/ (sections used: Methods > Dataset acquisition; Methods > Training and validation set annotation; Discussion; Data availability).
- **[PN-CHALLENGE2021]** PhysioNet/Computing in Cardiology Challenge 2021, release 1.0.3. https://physionet.org/content/challenge-2021/1.0.3/ (checked 2026-10-20).

### Result files made by this team

All are in `results/`. Each one describes the files we downloaded on 2026-10-20, not every copy of the dataset.

- **[OBS-PTBXL]** PTB-XL counts: `ptb_xl_summary.md`, `ptb_xl_scp_counts.csv`, `ptb_xl_field_counts.csv`, `ptb_xl_mi_by_stadium.csv`, `ptb_xl_mi_early_stadium.csv`, `ptb_xl_headers.csv` (recounted by the planner).
- **[OBS-SPH]** SPH counts from `metadata.csv` and `code.csv`: `sph_summary.md`, `sph_code_counts.csv`, `sph_code_modifier_counts.csv`, `sph_mi_timing.csv` (recounted by the planner).
- **[OBS-CODE15]** CODE-15% counts from `exams.csv`: `code15_summary.md`, `code15_label_counts.csv` (recounted by the planner).
- **[OBS-DOWNLOAD]** `download_manifest.csv`: what was downloaded, from where, and its checksum.
- All checked facts: `verified_facts.md`.
