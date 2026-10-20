# ECG Datasets for STEMI and NSTEMI Prediction: A Simple Review

| | |
|---|---|
| Status | **FINAL (2026-10-21).** All facts come from rows marked verified in `results/verified_facts.md`. MIMIC STEMI/NSTEMI counts are pending the user's script. |
| Date | 2026-10-21 |
| Written by | documenter (team: planner, coder, team-lead) |
| Plan | `PLAN.md` (approved by the user on 2026-10-20) |

<!-- section: A4 -->

## 1. Summary (one page)

**The short answer: with the open files, none of the 11 datasets can train a model to tell STEMI from NSTEMI.** No open file has a STEMI or NSTEMI label (section 4). Everything below marked *planner's view* is an assessment for the user and the clinical supervisor, not a decision.

**1. Which datasets are best for STEMI vs NSTEMI, and why?**

- **Only MIMIC-IV-ECG could do it**, and only by linking its ECGs to hospital diagnosis codes that need credentialed access [PN-MIMICECG; PN-MIMICECG-ICD]. Result: **not checked yet: needs credentialed access; the user will run the count script** (section 5.2). Even then, a discharge code describes the hospital stay, not the exact time of the ECG, so doctors must review it (*planner's view*, section 5.2 item 7).
- No other dataset has a STEMI or NSTEMI label, in the open files or in the label lists we checked (sections 4 and 5).

**2. What can the other datasets be used for?** (*planner's view; the supervisor still needs to agree*, section 6)

- **"MI statement or not", only after doctors review the labels:** PTB-XL (5,469 ECGs with MI statements), PTB Diagnostic (148 MI patients), SPH (260 ECGs), CPSC-Extra (mostly "old" MI). A missing MI code never means "no heart attack" (`data_contract.md` L1).
- **PTB Diagnostic is special:** it is the only one of the 11 datasets with documented heart-attack dates. 60 MI patients have an ECG 0–1 days after the recorded date [OBS-PTBDB]. This is a small list for doctors to review, not a set of confirmed new heart attacks.
- **External test (kept apart, only to check a finished model):** PTB Diagnostic and SPH, after review.
- **Pretraining (learning general ECG patterns first):** CODE-15%, Chapman-Shaoxing, Ningbo, CPSC 2018, Georgia, MIMIC-IV-ECG without labels, and INCART only as short cut-out pieces.
- **Not useful for training a heart-attack model:** INCART (30-minute Holter, only 2 acute-MI patients).

**3. Which datasets can be combined?** (section 7)

- **No pair is ready to combine yet.** 45 of the 55 pairs could be combined only after named checks. The other 10 (every pair with INCART) should not be combined for heart-attack training [CMB].
- The fewest checks (2) are needed for PTB-XL with Chapman-Shaoxing or Ningbo, and for 9 pairs among the Challenge datasets (listed in section 7). PTB-XL + MIMIC, the pair the earlier reports suggested first [CMP p.4], needs 3 checks: match leads by name, check the scale, and match two different label systems [CMB].
- **Never count the same ECGs twice:** the Challenge copies of PTB-XL and PTB Diagnostic, the ecg-arrhythmia copy of Chapman-Shaoxing + Ningbo, and the two INCART copies (section 8).

**Biggest warnings** (section 8): MIMIC and PTB-XL store leads in a different order; five datasets have no patient ID; many "acute" or "MI" labels are report words without timing; Ningbo's patients are much younger.

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
| PTB-XL | 71 SCP-ECG report codes; diagnosis codes have a wording-based "likelihood"; infarct stage (new/old), filled in mainly for MI-coded ECGs [PN-PTBXL; WAGNER2020; OBS-PTBXL] | Up to 2 cardiologists; about 31% of first reports were written by the ECG machine [PN-PTBXL; WAGNER2020] | PTB (Physikalisch-Technische Bundesanstalt); Oct 1989 – Jun 1996; 18,869 patients; country not stated on the dataset page [PN-PTBXL; WAGNER2020] | Not found (site names are hidden) [PN-PTBXL; WAGNER2020] | Schiller AG, 11 device types; 12 leads; 500 Hz (first recorded at 400 Hz); 10 s [WAGNER2020; PN-PTBXL] | No. Only "MI" report statements: 5,469 ECGs [OBS-PTBXL] | Not STEMI vs NSTEMI. Maybe MI vs non-MI after doctor review; pretraining. *Planner view, needs supervisor sign-off* | Same rate, length and leads as the planned model input; has patient IDs. See section 7 [PN-PTBXL] | Open, no login [PN-PTBXL] | 21,799 ECGs; 3.0 GB; CC BY 4.0 [PN-PTBXL] |
| MIMIC-IV-ECG | Open files: machine-written ECG reports only. Doctor reports: consortium members only. Diagnosis codes: credentialed only [PN-MIMICECG] | Open reports: the ECG machine. Most ECGs were also read by a cardiologist (report not open) [PN-MIMICECG] | Beth Israel Deaconess Medical Center, Boston, USA; 2008–2019; 161,352 patients [PN-MIMICECG; OBS-MIMIC] | Emergency department, hospital (including ICU) and outpatient centres; not given per ECG [PN-MIMICECG; OBS-MIMIC] | Burdick/Spacelabs, Philips, GE; 12 leads; 500 Hz; 10 s [PN-MIMICECG] | not checked yet: needs credentialed access; the user will run the count script | The only one that could give STEMI vs NSTEMI at large scale, **if** linked to diagnosis codes and reviewed; otherwise pretraining. *Planner view, needs supervisor sign-off* | Same rate, length and leads as the planned input, but **different lead order and scale** from PTB-XL; has patient IDs. See section 7 [OBS-MIMIC] | ECG files open, no login; diagnosis codes need credentialed access [PN-MIMICECG; PN-MIMICECG-ICD] | 800,035 ECGs; 90.4 GB; ODbL v1.0 [OBS-MIMIC; PN-MIMICECG] |
| PTB Diagnostic | Free-text clinical notes in each header: reason for admission, infarct place, infarction date, ECG date [OBS-PTBDB; PN-PTBDB] | Not found [PN-PTBDB] | University Clinic Benjamin Franklin, Berlin, Germany; years not found; 290 people [PN-PTBDB; OBS-PTBDB] | Hospital cardiology department; ward type not found [PN-PTBDB] | PTB prototype (not a commercial machine); 15 channels (12 standard + 3 extra); 1000 Hz; 32–120 s [PN-PTBDB; OBS-PTBDB] | No. MI (148 patients) vs healthy (52). Has documented time since infarction [OBS-PTBDB] | Possible external test set for new MI vs healthy, after clinical review; too small for STEMI vs NSTEMI. *Planner view, needs supervisor sign-off* | Needs a speed change (1000 Hz), 12 of 15 channels and cutting; patient = folder; a Challenge copy exists. See section 7 [PA2020] | Open, no login [PN-PTBDB] | 549 records; 1.7 GB; ODC Attribution License v1.0 [PN-PTBDB] |
| SPH (Shandong) | AHA report statements: 44 main codes plus add-on words (like "acute", "old") [LIU2022; OBS-SPH] | Cardiologist's final report; all re-checked by an experienced cardiologist [LIU2022] | Shandong Provincial Hospital, Jinan, China; Aug 2019 – Aug 2020; adults; 24,666 patients [LIU2022; OBS-SPH] | Not found [LIU2022] | MedEx MECG-200; 12 leads; 500 Hz; 10–60 s [LIU2022] | No. "MI" statements in 260 ECGs; only 7 say "acute" [OBS-SPH] | Not STEMI vs NSTEMI. Maybe test set for "MI statement or not" after review; pretraining. *Planner view, needs supervisor sign-off* | Same rate and leads; longer ECGs need cutting; has patient IDs; different label system. See section 7 [LIU2022] | Open, no login [FIGSHARE-SPH] | 25,770 ECGs; 2.28 GB of signals; data CC0, paper CC BY 4.0 [FIGSHARE-SPH; LIU2022] |
| CPSC 2018 | SNOMED CT codes (a large standard medical code list) in each header [OBS-CPSC; PN-CHALLENGE2021] | Not found for this dataset [PN-CHALLENGE2021; PA2020] | China Physiological Signal Challenge 2018, Nanjing, China; hospitals and years not found [PN-CHALLENGE2021] | Not found [PN-CHALLENGE2021; PA2020] | Device not found; 12 leads; 500 Hz; 6–144 s [PN-CHALLENGE2021] | Neither. No MI code. Has ST elevation and ST depression codes [DXMAP; OBS-CPSC] | Not an MI source; at most a set to review for ST changes; pretraining. *Planner view, needs supervisor sign-off* | Mostly longer than 10 s; **no patient ID**, but some patients have more than one recording; overlap with CPSC-Extra not checked. See section 7 [PA2020] | Open, no login [PN-CHALLENGE2021] | 6,877 recordings; whole Challenge release 12.6 GB; CC BY 4.0 [PN-CHALLENGE2021] |
| CPSC-Extra | SNOMED CT codes in each header [OBS-CPSCX; PN-CHALLENGE2021] | Not found for this dataset [PN-CHALLENGE2021; PA2020] | Unused data from CPSC 2018, China; hospitals, years and patients not found [PN-CHALLENGE2021; PA2020] | Not found [PN-CHALLENGE2021; PA2020] | Device not found; 12 leads; 500 Hz; about 10–98 s in a sample [OBS-CPSCX] | No. "MI" labels exist, but most say **old** MI [DXMAP; OBS-CPSCX] | Maybe "MI label or not" after doctor review; not STEMI vs NSTEMI; pretraining. *Planner view, needs supervisor sign-off* | Mostly longer than 10 s; no patient ID; same origin as CPSC 2018, overlap not checked. See section 7 | Open, no login [PN-CHALLENGE2021] | 3,453 recordings; CC BY 4.0 [PN-CHALLENGE2021; PA2020] |
| Georgia | SNOMED CT codes in each header [OBS-GEORGIA; PN-CHALLENGE2021] | Not found for this dataset [PN-CHALLENGE2021; PA2020] | Emory University, Atlanta, Georgia, USA; years not found; 15,742 patients (all parts) [PA2020; PN-CHALLENGE2021] | Not found [PN-CHALLENGE2021; PA2020] | Device not found; 12 leads; 500 Hz; 5–10 s [PN-CHALLENGE2021] | No. Only 7 "MI" labels; many ST and ischaemia labels [DXMAP] | Not an MI source; at most a set to review for ST changes; pretraining. *Planner view, needs supervisor sign-off* | 5-s recordings need padding; **no patient ID**, but some patients have more than one recording. See section 7 [PA2020] | Open, no login [PN-CHALLENGE2021] | 10,344 recordings (public part); CC BY 4.0 [PN-CHALLENGE2021] |
| Ningbo | SNOMED CT codes in each header; origin of the "acute MI" code unknown [OBS-NINGBO] | Ningbo-specific: not found. Shared page for Chapman + Ningbo: doctor, second doctor, senior doctor [PN-ECGARR] | Ningbo First Hospital, China; years not found; **much younger patients** in our sample (middle age 38) [PN-CHALLENGE2021; OBS-NINGBO] | Not found [PN-CHALLENGE2021; PN-ECGARR] | Stored in GE MUSE (storage system; machine not proven); 12 leads; 500 Hz; 10 s [PN-ECGARR; OBS-NINGBO] | No. 49 "acute MI" labels, but no timing and unknown origin [DXMAP; OBS-NINGBO] | Not STEMI vs NSTEMI; "acute MI" labels are a small list for review at most; good for pretraining. *Planner view, needs supervisor sign-off* | Same rate, length and leads as the planned input; no patient ID; the same ECGs are likely also in ecg-arrhythmia: never use both copies. See section 7 [PN-CHALLENGE2021; PN-ECGARR] | Open [PN-CHALLENGE2021; PN-ECGARR] | 34,905 recordings (Challenge folder); CC BY 4.0 [PN-CHALLENGE2021] |
| Chapman-Shaoxing | SNOMED CT codes in each header; MI wall locations merged into one code [OBS-CHAPMAN; ZH2020] | A doctor, checked by a second doctor; a senior doctor decided disagreements (best documented of the 5 Challenge sets) [ZH2020; PN-ECGARR] | Shaoxing People's Hospital, China, with Chapman University; years not found; 10,646 patients (original release) [ZH2020] | Not found (only "resting ECG") [ZH2020] | Stored in GE MUSE (storage system; machine not proven); 12 leads; 500 Hz; 10 s [ZH2020; OBS-CHAPMAN] | No. Only 40 MI labels, no timing [DXMAP] | Not an MI source; good for pretraining and rhythm. *Planner view, needs supervisor sign-off* | Same rate, length and leads as the planned input; no patient ID; the same ECGs are likely also in ecg-arrhythmia: never use both copies. See section 7 [PN-CHALLENGE2021; PN-ECGARR] | Open [PN-CHALLENGE2021; PN-ECGARR] | 10,247 recordings (Challenge folder); CC BY 4.0 [PN-CHALLENGE2021] |
| CODE-15% | 6 yes/no rhythm and conduction labels ("ST" = sinus tachycardia, **not** ST elevation), plus "normal ECG" and death [ZEN-CODE15] | Full CODE: computer reports plus text from expert reports; unclear cases checked by medical students with a cardiologist. For this 15% part: not found [RIBEIRO2020; ZEN-CODE15] | Telehealth Network of Minas Gerais, Brazil; 2010–2016; 233,770 patients [ZEN-CODE15; RIBEIRO2020] | Full CODE: mostly primary care (local health centres) [RIBEIRO2020] | TEB ECGPC or Micromed ErgoPC 13; 12 leads; 400 Hz as shared; 7–10 s, padded with zeros [RIBEIRO2020; ZEN-CODE15] | Neither. No MI label at all [OBS-CODE15; ZEN-CODE15] | Pretraining only, or not useful. *Planner view, needs supervisor sign-off* | Needs a speed change (400 Hz) and a padding mask; has patient IDs; no MI labels. See section 7 [ZEN-CODE15] | Open, no login [ZEN-CODE15] | 345,779 ECGs; 46.3 GB (all files); CC BY 4.0 [ZEN-CODE15] |
| INCART | Beat-by-beat marks; diagnosis text per patient; rhythm text per record [README-INCART; OBS-INCART] | Beat marks: computer, then corrected by people. Diagnoses: author not found [README-INCART] | St.-Petersburg Institute of Cardiological Technics, Russia; years not found; 32 patients tested for heart artery disease [README-INCART; PN-INCART] | Holter (long recording while the person goes about their day) [README-INCART] | Model not found; 12 leads; 257 Hz; 30 min [README-INCART; OBS-INCART] | Neither. "Acute MI" text: 2 patients only [OBS-INCART] | Not useful for MI tasks; at most pretraining on short pieces. *Planner view, needs supervisor sign-off* | Very different kind of recording; needs speed change and cutting; Challenge copy has 74 records, not 75. See section 7 [MCR p.4; PA2020] | Open, no login [PN-INCART] | 75 records; 794.5 MB; ODC Attribution License v1.0 [PN-INCART] |

<!-- section: A4 -->

## 4. Heart-attack labels in each dataset

For each dataset: which labels are about heart attacks, how many ECGs have them, whether they say "new" or "old", and whether STEMI and NSTEMI can be told apart.

| Dataset | Heart-attack labels | Number of ECGs | New or old shown? | STEMI vs NSTEMI possible? |
|---|---|---|---|---|
| PTB-XL | 14 "MI" report codes (5 of them are "injury" codes) [OBS-PTBXL] | 5,469 ECGs from 4,670 patients [OBS-PTBXL] | Partly. 150 MI-coded ECGs have an "early" stage; 3,372 have stage "unknown" [OBS-PTBXL] | No. No code says STEMI or NSTEMI [OBS-PTBXL] |
| MIMIC-IV-ECG | Open files: none checked (only machine-written reports, not downloaded). Diagnosis codes: credentialed only [PN-MIMICECG] | not checked yet: needs credentialed access; the user will run the count script | not checked yet: needs credentialed access; the user will run the count script | not checked yet: needs credentialed access; the user will run the count script |
| PTB Diagnostic | Reason for admission "Myocardial infarction"; infarct place; infarction date [OBS-PTBDB] | 368 records from 148 patients [OBS-PTBDB] | Yes, as documented time since infarction: 60 patients have an ECG 0–1 days after the infarction date [OBS-PTBDB] | No. No STEMI or NSTEMI label [OBS-PTBDB] |
| SPH (Shandong) | 4 "MI" codes (anterior, inferior, anteroseptal, extensive anterior) [OBS-SPH; LIU2022] | 260 ECGs from 242 patients [OBS-SPH] | Yes, as report words: "acute" 7 ECGs, "recent" 12, "old" 233, none 8 [OBS-SPH] | No. No statement says STEMI or NSTEMI [OBS-SPH] |
| CPSC 2018 | None. Only ST elevation and ST depression codes (not MI codes) [DXMAP] | 0 MI. ST elevation: 220 (publisher's count) [DXMAP] | No [DXMAP; OBS-CPSC] | No [DXMAP] |
| CPSC-Extra | Myocardial infarction; **old** MI; anterior MI [DXMAP] | Publisher's counts: MI 376, old MI 1,168, anterior MI 62 [DXMAP] | Partly: many are labelled "old"; none "acute" MI [DXMAP] | No [DXMAP] |
| Georgia | Myocardial infarction [DXMAP] | Publisher's count: 7 [DXMAP] | No [DXMAP] | No [DXMAP] |
| Ningbo | "Acute myocardial infarction"; myocardial infarction; anterior MI [DXMAP] | Publisher's counts: acute MI 49, MI 83, anterior MI 57 [DXMAP] | Only as a label word ("acute"). No timing field; origin of the label unknown [OBS-NINGBO] | No [DXMAP] |
| Chapman-Shaoxing | Myocardial infarction (one code; wall location lost) [OBS-CHAPMAN; ZH2020] | Publisher's count: 40 [DXMAP] | No [DXMAP] | No [DXMAP] |
| CODE-15% | None. The "ST" column means sinus tachycardia (a fast heart rhythm that starts in the heart's normal pacemaker), not ST elevation [ZEN-CODE15] | 0 [OBS-CODE15] | No [OBS-CODE15] | No [OBS-CODE15; RIBEIRO2020] |
| INCART | Diagnosis text "Acute MI" and "Earlier MI" [OBS-INCART] | Acute MI: 6 records (2 patients). Earlier MI: 9 records (4 patients) [OBS-INCART] | Yes, as diagnosis text ("acute" / "earlier") [OBS-INCART] | No [OBS-INCART] |

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
8. **Combining.** *(See also the table in section 7.)* 500 Hz, 10 seconds and 12 standard leads. This matches the planned model input, so no change of speed is needed [PN-PTBXL; `data_contract.md` C1.3]. Each ECG has a patient number, so one patient can be kept in one group (training or testing). The data also comes already split into 10 groups ("folds") [OBS-PTBXL]. Count the 100 Hz copies once, not twice (`data_contract.md` O2). A copy of PTB-XL inside the 2021 PhysioNet Challenge has 21,837 recordings, which is the first-release count [PN-CHALLENGE2021]. Do not mix it with release 1.0.3 before checking which ECGs are the same (`data_contract.md` O8).
9. **Access.** Open. "Anyone can access the files, as long as they conform to the terms of the specified license" [PN-PTBXL]. We needed no login to download [OBS-DOWNLOAD].
10. **Size and license.** 21,799 ECGs from 18,869 patients (release 1.0.3); 3.0 GB unpacked; license CC BY 4.0 (free to use if you credit the authors); DOI 10.13026/kfzx-aw45; published 9 Nov 2022 [PN-PTBXL]. The paper describes the first release: 21,837 ECGs from 18,885 patients [WAGNER2020]. Do not mix the two counts (`data_contract.md` O8).

### 5.2 MIMIC-IV-ECG

**In one line:** a very large set of ECGs from one Boston hospital, from the emergency department, hospital care (including intensive care) and outpatient centres. The open files have no doctor labels. STEMI vs NSTEMI could only come from diagnosis codes that need credentialed access, and that has **not been checked yet**.

1. **Labels.** The open files have **machine-written reports only**: "A text based cardiology report generated by the ECG machine", in the columns `report_0` to `report_17` of `machine_measurements.csv`, plus measurements made by the machine [OBS-MIMIC; PN-MIMICECG]. Reports written by doctors exist, but "only members who are part of our consortium can access the cardiologist reports" [PN-MIMICECG]. Diagnosis codes (ICD codes, used for hospital billing) are only in other modules that need credentialed access (MIMIC-IV hosp/ED, MIMIC-IV-ECG-ext-ICD) [PN-MIMICECG; PN-MIMICECG-ICD]. How many machine reports mention MI or ST changes: **not checked**. The file with these reports was not downloaded [OBS-MIMIC].
2. **Who labelled them.** The open reports were written by the ECG machine [OBS-MIMIC]. "Most ECG waveforms get read by a cardiologist and an associated report is generated from the reading", but those reports are not open [PN-MIMICECG]. In the credentialed ext-ICD module, the codes are emergency department and hospital discharge diagnosis codes (billing codes) [PN-MIMICECG-ICD].
3. **Collection.** Beth Israel Deaconess Medical Center (BIDMC), Boston, Massachusetts, USA [PN-MIMICECG]. ECGs "collected between 2008 - 2019 for subjects in MIMIC-IV" [PN-MIMICECG]. The page says "approximately 800,000 diagnostic electrocardiograms across nearly 160,000 unique patients" [PN-MIMICECG]. In the downloaded file `record_list.csv` we counted 800,035 ECGs from 161,352 patients. Each patient has 1 to 260 ECGs (middle value 2, average 4.96). 104,008 patients have more than one ECG [OBS-MIMIC]. "The date-time information was shifted to obscure the actual date and time", so the files cannot give real years [PN-MIMICECG].
4. **Setting.** **Known for the dataset as a whole:** "This includes ECGs from the BIDMC emergency department, hospital (including the ICU), and outpatient care centers" [PN-MIMICECG]. (ICU = intensive care unit.) But the open file does **not** say where each single ECG was taken [OBS-MIMIC]. The credentialed ext-ICD module has emergency-department and hospital flags [PN-MIMICECG-ICD].
5. **Device.** "Machines from various manufacturers including Burdick/Spacelabs, Philips, and General Electric". 12 leads, 10 seconds, 500 Hz [PN-MIMICECG]. The `cart_id` column is "an identifier specific to the ECG cart". It is not a machine model (`data_contract.md` C2.6) [OBS-MIMIC]. We opened 50 header files as a sample. All had 12 leads, 500 Hz, 5,000 samples, and a scale of 200 units per millivolt [OBS-MIMIC]. **The lead order was I, II, III, aVR, aVF, aVL, V1–V6. Here aVF comes before aVL, which is different from PTB-XL** [OBS-MIMIC]. This is a small sample and may not hold for every file.
6. **STEMI vs NSTEMI.** **not checked yet: needs credentialed access; the user will run the count script.** The open files cannot answer this. STEMI vs NSTEMI would need diagnosis codes from the credentialed modules [PN-MIMICECG; PN-MIMICECG-ICD]. The user will run a small script (`src/stemi/review/mimic_icd_count.py`) on their own computer, which gives totals only. The counts of machine-written MI or ST statements were also not checked. Even if counted, they would be machine text only, not a diagnosis (`data_contract.md` L2).
7. **Best model use.** *This is the planner's view. The clinical supervisor still needs to agree.* This is the only one of the 11 datasets that **could** give STEMI vs NSTEMI at a large scale. That needs two things: linking ECGs to the credentialed diagnosis codes, and a clinical review. Even then, care is needed: a discharge code describes the hospital stay, not the exact time of the ECG, and the clocks of different systems may not match. Without this linking, MIMIC-IV-ECG is for pretraining only (`data_contract.md` L1, L2, L11).
8. **Combining.** *(See also the table in section 7.)* 500 Hz, 10 seconds and 12 leads: this matches the planned model input (`data_contract.md` C1.3) [PN-MIMICECG]. **But the lead order is different from PTB-XL (aVF and aVL are swapped), and the scale is different (200 vs 1,000 units per millivolt)** [OBS-MIMIC; OBS-PTBXL]. So leads must be matched by name, and units must be checked (`data_contract.md` P4, C2.9). The patient key is `subject_id` [OBS-MIMIC]. The earlier report named PTB-XL + MIMIC as the first pair to look at [CMP p.4]. No shared source with PTB-XL is documented: they come from different places (PTB vs BIDMC). But "no shared patients" has not been proven. Also, "around 5% of the available diagnostic ECGs were withheld from this release so they can be used as a hidden test set" [PN-MIMICECG].
9. **Access.** The ECG module is open: "Anyone can access the files, as long as they conform to the terms of the specified license". We needed no login [PN-MIMICECG; OBS-DOWNLOAD]. Doctor reports: consortium members only [PN-MIMICECG]. Diagnosis codes (ext-ICD): credentialed access, a signed data use agreement and CITI training (a short course on research with people's data) [PN-MIMICECG-ICD].
10. **Size and license.** 800,035 ECGs from 161,352 patients (our count) [OBS-MIMIC]. 90.4 GB unpacked. License: Open Data Commons Open Database License v1.0 (ODbL) [PN-MIMICECG]. The ext-ICD module uses the PhysioNet Credentialed Health Data License 1.5.0 [PN-MIMICECG-ICD]. We downloaded `record_list.csv` (70,403,124 bytes). There was no publisher checksum to compare with, but a plausibility check passed [OBS-DOWNLOAD].

### 5.3 PTB Diagnostic

**In one line:** a small, open, older set of long ECGs from one hospital cardiology department in Berlin. It is the only one of the 11 datasets that records **when** the heart attack happened. It has no STEMI or NSTEMI label.

1. **Labels.** There are no codes. Each recording's header has free-text clinical notes. These include fields such as "Reason for admission", "Acute infarction (localization)" (where the heart attack is), "Former infarction (localization)", "Infarction date (acute)", "ECG date", "Catheterization date" (date of a heart artery test), narrowing of the main heart arteries, and "Lytic agent" (a clot-dissolving drug) [OBS-PTBDB]. Reasons for admission, as records / patients [OBS-PTBDB]:
   - Myocardial infarction: 368 / 148
   - Healthy control: 80 / 52
   - n/a: 27 / 22
   - Cardiomyopathy (heart muscle disease): 17 records
   - Bundle branch block: 17 records
   - Dysrhythmia (abnormal heart rhythm): 16 records
   - Hypertrophy (thickened heart muscle): 7 records
   - Valvular heart disease: 6 records
   - Myocarditis (inflamed heart muscle): 4 records
   - Others: 2 records or fewer each

   The 148 MI patients and 52 healthy people match the class table on the dataset page [PN-PTBDB; OBS-PTBDB].
2. **Who labelled them.** **Not found.** The dataset page says most records include "a detailed clinical summary", but not who wrote it [PN-PTBDB].
3. **Collection.** The ECGs were "collected from healthy volunteers and patients with different heart diseases by Professor Michael Oeff … at the Department of Cardiology of University Clinic Benjamin Franklin in Berlin, Germany". PTB put them together [PN-PTBDB]. Collection years: **not found**. The page does not state them [PN-PTBDB]. The dates in the headers are around 1990. The page does not say if they are real or moved, so we do not use them as collection years [PN-PTBDB; OBS-PTBDB]. Number of people: the files have 290 patient folders [OBS-PTBDB]. The page says "294 subjects" in one place and "549 records from 290 subjects" in another. The files support 290 [PN-PTBDB; OBS-PTBDB].
4. **Setting.** A hospital cardiology department, with heart patients and healthy volunteers [PN-PTBDB]. Whether ward, intensive care, emergency room or clinic: **not found** [PN-PTBDB].
5. **Device.** "A non-commercial, PTB prototype recorder" (a test machine, not one sold in shops). It stores 2,000 units per millivolt [PN-PTBDB]. All 549 headers have 15 channels: the 12 standard leads plus 3 extra "Frank" leads (vx, vy, vz: extra leads that record the heart's electrical direction in 3D). Lead names are in lower case [OBS-PTBDB]. 1000 Hz. The header has no unit field. The dataset page gives the scale (2,000 units per millivolt) [PN-PTBDB; OBS-PTBDB]. Length: 32 to 120 seconds in the files. The page does not state the length [OBS-PTBDB; PN-PTBDB].
6. **STEMI vs NSTEMI.** **No.** There is no STEMI or NSTEMI label [OBS-PTBDB]. It can give MI vs no MI: 148 MI patients (368 records) vs 52 healthy people (80 records), plus people with other heart diseases [OBS-PTBDB].

   **What is special here: documented time since infarction.** We took "ECG date" minus "Infarction date (acute)". The dates are read day first (day/month/year). We know this because in 374 of the 541 dated headers the first number is above 12, and the second number is never above 12 [OBS-PTBDB]. The time could be worked out for 343 of the 368 MI records [OBS-PTBDB]:

   | Days from infarction to ECG | MI records | MI patients (earliest ECG on or after the infarction date) |
   |---|---|---|
   | 0–1 | 61 | 60 |
   | 2–3 | 35 | 18 |
   | 4–7 | 68 | 20 |
   | 8–28 | 115 | 23 |
   | more than 28 | 63 | 2 |
   | ECG before the infarction date | 1 | – |
   | Could not be worked out | 25 | 25 |

   So 60 MI patients have an ECG 0–1 days after the recorded infarction date [OBS-PTBDB]. **These are a documented time since infarction. They are not reviewed acute-MI labels. Doctors must review them first.** The two infarction-date fields disagree in 3 records [OBS-PTBDB]. There is also a field for where the heart attack is (for example inferior, antero-septal, infero-lateral) [OBS-PTBDB]. The "Lytic agent" field says, as written: Streptokinase (60 patients), Urokinase (20), Gamma-TPA (15) [OBS-PTBDB]. Whether this field says anything about STEMI is a question for the clinical supervisor. This report does not use it as a label.
7. **Best model use.** *This is the planner's view. The clinical supervisor still needs to agree.* This is the only one of the 11 datasets with documented infarction dates. It gives a small review set: MI ECGs taken 0–1 days after the infarction (60 patients), plus 52 healthy people. After clinical review, it could be an external test set (data kept apart, used only to check a finished model) for "new MI vs healthy". It is too small, and has no STEMI/NSTEMI labels, so it cannot train a STEMI-vs-NSTEMI model (`data_contract.md` L4, L7).
8. **Combining.** *(See also the table in section 7.)* 1000 Hz, so it must be changed to 500 Hz (`data_contract.md` C2.3). 15 channels: keep the 12 standard ones, which all 549 records have by name [OBS-PTBDB]. 32–120 seconds, so a rule for cutting is needed. Patient = the folder [OBS-PTBDB]. A copy is inside the 2021 PhysioNet Challenge (the `ptb` folder). It has 516 recordings instead of 549, and the paper gives no reason [PA2020, Table 2]. Do not use both without checking which ECGs are the same (`data_contract.md` O10). The Challenge says it "did not change the original data or labels", except for approximate SNOMED CT codes, hidden age and sex, and amplitude resolution [PA2020, §2.1.2].
9. **Access.** Open: "Anyone can access the files, as long as they conform to the terms of the specified license." We needed no login [PN-PTBDB; OBS-DOWNLOAD].
10. **Size and license.** 549 records from 290 people (the page also says 294 in one place). 1.7 GB unpacked. License: ODC Attribution License v1.0 (free to use if you credit the source). DOI 10.13026/C28C71. Published 25 Sept 2004 [PN-PTBDB; OBS-PTBDB].

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
8. **Combining.** *(See also the table in section 7.)* 500 Hz and 12 leads match the planned model input (`data_contract.md` C1.3). The ECGs are 10–56 seconds long, so a rule for cutting them to the model's length is needed (`data_contract.md` Q9). Each ECG has a patient number. The paper warns against putting "records from the same patient" in both training and testing, and gives code to split them [LIU2022]. The label system (AHA) is different from PTB-XL (SCP-ECG) and the Challenge sets (SNOMED), so labels must be matched first [LIU2022]. The paper does not mention any overlap with other datasets [LIU2022].
9. **Access.** Open download from figshare. No login needed [FIGSHARE-SPH; OBS-DOWNLOAD].
10. **Size and license.** 25,770 ECGs from 24,666 patients [OBS-SPH]. The signal file `records.tar.gz` is about 2.28 GB (we did not download it). `metadata.csv` is about 1 MB [FIGSHARE-SPH]. The **data** is CC0 (no rights kept, free for any use) on figshare [FIGSHARE-SPH]. The **paper** is CC BY 4.0 [LIU2022]. Both are true: they apply to different things.

### About the five Challenge datasets (5.5 to 5.9)

CPSC 2018, CPSC-Extra, Georgia, Ningbo and Chapman-Shaoxing are all shared inside the 2021 PhysioNet Challenge (a public contest to build ECG models) [PN-CHALLENGE2021]. Things that are the same for all five:

- **Labels** are SNOMED CT codes (a large standard list of medical codes) in the `#Dx` line of each header [PN-CHALLENGE2021].
- **No STEMI or NSTEMI code** appears in the Challenge label files [DXMAP].
- **Label quality varies.** The Challenge paper says: "The quality of the label depended on the clinical or research practices, and the Challenge included labels that were machine-generated, over-read by a single cardiologist, and adjudicated by multiple cardiologists." It does not say which method was used for which dataset [PA2020, §2.1.2]. The Challenge page adds that "some of the data and labels are likely to have errors" [PN-CHALLENGE2021].
- **What the Challenge changed:** only "approximate SNOMED CT codes", hidden age and sex, and amplitude resolution. Otherwise it "did not change the original data or labels" [PA2020, §2.1.2].

**Two kinds of counts. Do not mix them up.**

- **Publisher's count:** taken from the Challenge label files (`dx_mapping_scored.csv` and `dx_mapping_unscored.csv`, our copy of 2026-10-20). The publisher does not say exactly what these numbers count [DXMAP].
- **Sample count:** what we counted in a sample of one folder only (999 headers). It is not a count for the whole dataset [OBS-CPSC; OBS-CPSCX; OBS-GEORGIA].

### 5.5 CPSC 2018

**In one line:** an open set of Chinese ECGs from a 2018 contest. It has no heart-attack codes at all, only ST elevation and ST depression codes.

1. **Labels.** SNOMED CT codes in each header. Each header also has the fields Age, Sex, Dx, Rx, Hx and Sx [OBS-CPSC; PN-CHALLENGE2021]. In a sample of one folder (999 headers; one listed file could not be found on the server), every recording had at least one code [OBS-CPSC].
2. **Who labelled them.** **Not found** for this dataset. The paper that describes it could not be opened (the publisher's page refused access) [PN-CHALLENGE2021; PA2020]. Only the general Challenge statement above applies [PA2020, §2.1.2].
3. **Collection.** From the China Physiological Signal Challenge 2018, held "in Nanjing, China" [PN-CHALLENGE2021]. Hospitals and years: **not found** [PN-CHALLENGE2021]. For all CPSC data (including a hidden test part): 9,458 patients and 13,256 recordings; average age 61.1; 53% male [PA2020, Tables 1–2]. In the sample folder: 521 male and 478 female; ages 7 to 92 [OBS-CPSC]. For CPSC and CPSC-Extra, the Challenge page says: "All ages over 89 are provided as 92". So "92" means "over 89" [PN-CHALLENGE2021].
4. **Setting.** **Not found** [PN-CHALLENGE2021; PA2020].
5. **Device.** Machine: **not found**. "Each recording is between 6 and 144 seconds long with a sampling frequency of 500 Hz" [PN-CHALLENGE2021]. In the sample folder: 12 leads (I, II, III, aVR, aVL, aVF, V1–V6), 500 Hz, units in millivolts, 9 to 118 seconds. 364 of the 999 are exactly 10 seconds [OBS-CPSC].
6. **STEMI vs NSTEMI.** **Neither.** There is no MI code [DXMAP; OBS-CPSC].
   - ST elevation: 220 (publisher's count) / 31 (sample count).
   - ST depression: 869 (publisher's count) / 114 (sample count).

   ST changes alone do not mean a heart attack (`data_contract.md` L2).
7. **Best model use.** *This is the planner's view. The clinical supervisor still needs to agree.* Not a source for MI, or for STEMI vs NSTEMI. The ST elevation and depression labels give, at most, a set to review for ST-change detection. Could be used for pretraining (`data_contract.md` L11).
8. **Combining.** *(See also the table in section 7.)* 500 Hz and 12 leads. Most recordings are longer than 10 seconds, so a rule for cutting is needed [OBS-CPSC]. **There is no patient ID in the headers** [OBS-CPSC]. Yet CPSC has more recordings than patients (13,256 vs 9,458), so some patients have more than one recording [PA2020, Table 1]. These cannot be grouped, so the same patient could end up in both training and testing (`data_contract.md` S7). Overlap with CPSC-Extra has not been checked (`data_contract.md` O5).
9. **Access.** Open: "Anyone can access the files, as long as they conform to the terms of the specified license" [PN-CHALLENGE2021].
10. **Size and license.** 6,877 recordings in the Challenge training folder. The whole Challenge release is 12.6 GB. License: CC BY 4.0 [PN-CHALLENGE2021]. Number of patients in the shared part: **not found**.

### 5.6 CPSC-Extra

**In one line:** extra, unused ECGs from the same Chinese 2018 contest. It has "MI" labels, but **most of them say "old" MI**, and none says STEMI or NSTEMI.

1. **Labels.** SNOMED CT codes in each header, with the fields Age, Sex, Dx, Rx, Hx and Sx [OBS-CPSCX; PN-CHALLENGE2021]. We read a sample of one folder (999 headers; one listed file could not be found on the server) [OBS-CPSCX].
2. **Who labelled them.** **Not found** for this dataset [PN-CHALLENGE2021; PA2020]. Only the general Challenge statement above applies [PA2020, §2.1.2].
3. **Collection.** "Unused data from CPSC 2018 (the CPSC-Extra Database)", China [PN-CHALLENGE2021]. Hospitals and years: **not found**. 3,453 recordings, average 15.9 seconds long, average age 63.7, 53% male [PA2020, Table 2]. Number of patients: **not found** [PA2020]. In the sample folder: 533 male and 466 female; ages −1 to 92. "−1" is how it is written in the file, and the publisher does not explain what it means [OBS-CPSCX]. For CPSC and CPSC-Extra, the Challenge page says: "All ages over 89 are provided as 92". So "92" means "over 89" [PN-CHALLENGE2021].
4. **Setting.** **Not found** [PN-CHALLENGE2021; PA2020].
5. **Device.** Machine: **not found**. In the sample folder: 12 leads, 500 Hz, units in millivolts, about 10 to 98 seconds. 400 of the 999 are exactly 10 seconds [OBS-CPSCX].
6. **STEMI vs NSTEMI.** **No.** Heart-related labels, as publisher's count / sample count [DXMAP; OBS-CPSCX]:

   | Label | Publisher's count | Sample count (999) |
   |---|---|---|
   | Myocardial infarction | 376 | 122 |
   | **Old** myocardial infarction | 1,168 | 337 |
   | Anterior myocardial infarction | 62 | 17 |
   | Myocardial ischaemia | 384 | 101 |
   | Chronic (long-lasting) myocardial ischaemia | 161 | 45 |
   | Acute myocardial ischaemia | 1 | 1 |
   | ST elevation | 66 | 23 |
   | ST depression | 57 | 11 |
   | Inferior ST depression | 1 | 1 |
   | ST interval abnormal | 481 | 137 |
   | Nonspecific ST-T abnormality | 1,290 | 384 |

   **Most MI labels say "old" MI (1,168 "old MI" vs 376 "MI").** There is no "acute MI" label [DXMAP]. These are report labels, not checked diagnoses (`data_contract.md` L2, L3). So this dataset gives "MI label or not" only, and mostly old MI.
7. **Best model use.** *This is the planner's view. The clinical supervisor still needs to agree.* After doctors review the labels, it could be a set for "MI label vs other" (`data_contract.md` L4). Not for STEMI vs NSTEMI. Could be used for pretraining.
8. **Combining.** *(See also the table in section 7.)* 500 Hz and 12 leads. Most recordings are longer than 10 seconds [OBS-CPSCX]. **No patient ID** [OBS-CPSCX]. It comes from the same CPSC 2018 contest as CPSC 2018, so the two must be checked for shared recordings before use together (`data_contract.md` O5). Their file names start with different letters (A… vs Q…), but that proves nothing.
9. **Access.** Open [PN-CHALLENGE2021].
10. **Size and license.** 3,453 recordings. License: CC BY 4.0 (the whole Challenge) [PN-CHALLENGE2021; PA2020]. Number of patients: **not found**.

### 5.7 Georgia

**In one line:** an open set of short ECGs from Emory University in the south-east of the USA. It has almost no MI labels (7), but many ST and ischaemia labels.

1. **Labels.** SNOMED CT codes in each header, with the fields Age, Sex, Dx and Rx. 996 of the 999 sample headers also have Hx [OBS-GEORGIA; PN-CHALLENGE2021]. We read a sample of one folder (999 headers; one listed file could not be found on the server) [OBS-GEORGIA].
2. **Who labelled them.** **Not found** for this dataset [PN-CHALLENGE2021; PA2020]. Only the general Challenge statement above applies [PA2020, §2.1.2].
3. **Collection.** "Georgia 12-lead ECG Challenge (G12EC) Database, Emory University, Atlanta, Georgia, USA", "representing a large population from the Southeastern United States" [PA2020, §2.1.1]. For all Georgia data (including hidden parts): 15,742 patients and 20,678 recordings; average age 60.5; 54% male [PA2020, Tables 1–2]. The Challenge page says "This source contains 20,672 ECGs", 6 fewer. This is not explained (see section 9) [PN-CHALLENGE2021]. Years: **not found**. In the sample folder: 564 male and 435 female; ages 20 to 89; age missing in 24 [OBS-GEORGIA].
4. **Setting.** **Not found** [PN-CHALLENGE2021; PA2020].
5. **Device.** Machine: **not found**. "Each recording is between 5 and 10 seconds long with a sampling frequency of 500 Hz" [PN-CHALLENGE2021]. In the sample folder: 12 leads, 500 Hz, units in millivolts. 989 recordings are 10 seconds and 10 are 5 seconds [OBS-GEORGIA].
6. **STEMI vs NSTEMI.** **No.** Heart-related labels, as publisher's count / sample count [DXMAP; OBS-GEORGIA]:

   | Label | Publisher's count | Sample count (999) |
   |---|---|---|
   | Myocardial infarction | 7 | 0 |
   | ST elevation | 134 | 20 |
   | ST depression | 38 | 5 |
   | Q-wave abnormal | 464 | 73 |
   | Lateral ischaemia | 903 | 73 |
   | Inferior ischaemia | 451 | 43 |
   | Anterior ischaemia | 281 | 39 |
   | Acute myocardial ischaemia | 1 | 0 |
   | ST interval abnormal | 992 | 60 |
   | Nonspecific ST-T abnormality | 1,883 | 149 |

   With only 7 MI labels, this is not a heart-attack dataset. ST and ischaemia labels do not mean a heart attack (`data_contract.md` L2).
7. **Best model use.** *This is the planner's view. The clinical supervisor still needs to agree.* Not an MI source (only 7 MI labels in the whole source). The ischaemia and ST labels give, at most, a set to review for ST-change detection. Could be used for pretraining.
8. **Combining.** *(See also the table in section 7.)* 500 Hz and 12 leads. 5 to 10 seconds, so the 5-second recordings need a padding rule [OBS-GEORGIA; PN-CHALLENGE2021]. **There is no patient ID in the headers** [OBS-GEORGIA]. Yet there are more recordings than patients (20,678 vs 15,742), so some patients have more than one recording [PA2020, Table 1]. These cannot be grouped (`data_contract.md` S7).
9. **Access.** Open [PN-CHALLENGE2021].
10. **Size and license.** 10,344 recordings in the public training folder. License: CC BY 4.0 (the whole Challenge) [PN-CHALLENGE2021].

### 5.8 Ningbo

**In one line:** a large, open set of 10-second ECGs from one Chinese hospital, with **much younger patients** than the other Challenge datasets (sample medians). It has 49 "acute MI" labels, but we do not know where they came from, and there is no timing.

1. **Labels.** SNOMED CT codes in each header, with the fields Age, Sex, Dx, Rx, Hx and Sx [OBS-NINGBO]. In a sample of one folder (999 headers; one listed file could not be found on the server) there were 64 different codes [OBS-NINGBO]. **Two heart-attack codes are not in the original label list:** "acute myocardial infarction" (57054005) and "anterior MI" (54329005). They are missing from the original release's code list, so we do not know which original Ningbo label they came from [OBS-NINGBO].
2. **Who labelled them.** **Not found for Ningbo alone.** The ecg-arrhythmia page covers Chapman-Shaoxing and Ningbo together. It says a licensed physician labelled the ECGs, a second licensed physician checked them, and a senior physician decided disagreements [PN-ECGARR]. We did not read the Ningbo paper, so we found no description for Ningbo alone.
3. **Collection.** Ningbo First Hospital, China ("Ningbo First Hospital (Ningbo) database") [PN-CHALLENGE2021; PN-ECGARR]. Years: **not found**. In the sample folder: 567 male, 430 female and 2 "Unknown"; ages 0 to 89; age missing for 2 [OBS-NINGBO]. **The middle (median) age in the sample is 38. In the samples of the other Challenge datasets it is 61 to 65.** So these patients are much younger [OBS-NINGBO].
4. **Setting.** **Not found** [PN-CHALLENGE2021; PN-ECGARR].
5. **Device.** "The data was stored into the GE MUSE ECG system" [PN-ECGARR]. GE MUSE is a system for storing ECGs. It does not prove which machine recorded them [NB p.15]. In the sample folder, all 999 had 12 leads, 500 Hz, 5,000 samples (10 seconds), units in millivolts, and the lead order I, II, III, aVR, aVL, aVF, V1–V6 [OBS-NINGBO].
6. **STEMI vs NSTEMI.** **No.** Heart-related labels, as publisher's count / sample count [DXMAP; OBS-NINGBO]:

   | Label | Publisher's count | Sample count (999) |
   |---|---|---|
   | **Acute** myocardial infarction | 49 | 1 |
   | Myocardial infarction | 83 | 4 |
   | Anterior myocardial infarction | 57 | 3 |
   | ST elevation | 0 | 0 |
   | ST depression | 1,266 | 31 |
   | Q-wave abnormal | 828 | 11 |
   | ST interval abnormal | 799 | 22 |

   Of the five Challenge datasets in this review, Ningbo is the only one with an "acute MI" label (the Challenge copy of INCART also has 6) [DXMAP]. But "acute" here is only a word in the label. There is no timing field, and we do not know which original label it came from (see item 1). **It is not a reviewed acute heart attack** (`data_contract.md` L2, L3). The one "acute MI" ECG in our sample also has the code "ST interval abnormal" [OBS-NINGBO]. There are **no** ST elevation labels at all [DXMAP].
7. **Best model use.** *This is the planner's view. The clinical supervisor still needs to agree.* Not a source for STEMI vs NSTEMI. The 49 "acute MI" labels are, at most, a small list for doctors to review. Because the rhythm labels were checked by doctors, it is a good source for pretraining. Its patients are much younger than in the other datasets.
8. **Combining.** *(See also the table in section 7.)* 500 Hz, 10 seconds and 12 leads: this matches the planned model input (`data_contract.md` C1.3) [OBS-NINGBO]. **No patient ID** in the headers [OBS-NINGBO]. **The same ECGs are probably also in ecg-arrhythmia.** That dataset has 45,152 ECGs, which is exactly Chapman-Shaoxing (10,247) + Ningbo (34,905) [PN-CHALLENGE2021; PN-ECGARR]. This is a count match only (`data_contract.md` O4). **Never use both copies together.**
9. **Access.** Open [PN-CHALLENGE2021]. The ecg-arrhythmia copy is also open, under CC BY 4.0 [PN-ECGARR].
10. **Size and license.** 34,905 recordings in the Challenge folder. License: CC BY 4.0 [PN-CHALLENGE2021].

### 5.9 Chapman-Shaoxing

**In one line:** an open set of 10-second resting ECGs from one Chinese hospital, with the best-documented doctor labelling of the five Challenge datasets. It has only 40 MI labels and no timing, so it is not a heart-attack dataset.

1. **Labels.** SNOMED CT codes in each header, with the fields Age, Sex, Dx, Rx, Hx and Sx [OBS-CHAPMAN]. In a sample of one folder (999 headers; one listed file could not be found on the server) there were 35 different codes, all with known names [OBS-CHAPMAN]. **The heart-attack location is lost.** The original release had separate labels for MI in general and for MI of the back wall, front wall, lower wall and side wall. They all became one SNOMED code (164865005) [OBS-CHAPMAN; ZH2020]. **ST labels were renamed.** In the original release, "ST elevation" was called "ST tilt up" and "ST depression" was called "ST drop down" [OBS-CHAPMAN; ZH2020]. The wording differs between the original and Challenge copies, and doctors should review what it means [OBS-CHAPMAN].
2. **Who labelled them.** "A licensed physician labeled the rhythm and other cardiac conditions". A second licensed physician checked the labels. When they disagreed, a senior physician made the final decision [ZH2020; PN-ECGARR]. This is the best-documented labelling of the five Challenge datasets.
3. **Collection.** Shaoxing People's Hospital (Shaoxing Hospital Zhejiang University School of Medicine), China, working with Chapman University [ZH2020; PN-ECGARR]. Years: **not found**. The original release had 10,646 patients (5,956 male, 4,690 female), aged 4 to 98, with "a 12-lead resting ECG" of 10 seconds for each person [ZH2020]. This suggests one ECG per patient, but the paper does not say so directly. In the sample folder: 593 male and 406 female; ages 4 to 89 [OBS-CHAPMAN].
4. **Setting.** **Not found.** The paper only says "12-lead resting ECG". It does not say inpatient, outpatient or health check-up [ZH2020].
5. **Device.** "The data were stored into the GE MUSE ECG system" [ZH2020]. GE MUSE is a system for storing ECGs. It does not prove which machine recorded them [NB p.15]. 500 Hz, 10 seconds [ZH2020]. In the sample folder, all 999 had 12 leads, 500 Hz, 5,000 samples, units in millivolts, and the lead order I, II, III, aVR, aVL, aVF, V1–V6 [OBS-CHAPMAN].
6. **STEMI vs NSTEMI.** **No.** Heart-related labels, as publisher's count / sample count [DXMAP; OBS-CHAPMAN]:

   | Label | Publisher's count | Sample count (999) |
   |---|---|---|
   | Myocardial infarction | 40 | 3 |
   | ST elevation (originally "ST tilt up") | 176 | 11 |
   | ST depression (originally "ST drop down") | 402 | 33 |
   | Q-wave abnormal | 235 | 18 |
   | Nonspecific ST-T abnormality | 1,158 | 98 |

   Very few MI labels, and none says whether the heart attack is new or old.
7. **Best model use.** *This is the planner's view. The clinical supervisor still needs to agree.* Not a source for MI, or for STEMI vs NSTEMI (only 40 MI labels). Because the labels were checked by doctors, it is a good source for pretraining and for heart rhythm.
8. **Combining.** *(See also the table in section 7.)* 500 Hz, 10 seconds and 12 leads: this matches the planned model input directly (`data_contract.md` C1.3) [ZH2020]. **No patient ID** in the headers [OBS-CHAPMAN]. **The same ECGs are probably also in another dataset.** The PhysioNet "ecg-arrhythmia" dataset has 45,152 ECGs, which is exactly Challenge Chapman-Shaoxing (10,247) + Ningbo (34,905) [PN-CHALLENGE2021; PN-ECGARR]. This is a count match only: no one compared the recordings one by one (`data_contract.md` O4). **Never use the Challenge copy and the ecg-arrhythmia copy together.** Also, the original release had 10,646 records but the Challenge folder has 10,247. The sources we read do not explain the difference (see section 9) [ZH2020; PN-CHALLENGE2021].
9. **Access.** Open [PN-CHALLENGE2021]. The ecg-arrhythmia copy is also open, under CC BY 4.0 [PN-ECGARR].
10. **Size and license.** 10,247 recordings in the Challenge folder. License: CC BY 4.0 [PN-CHALLENGE2021].

### 5.10 CODE-15%

**In one line:** a very large, open set of Brazilian tele-ECGs (ECGs sent to a distant centre to be read). It has no heart-attack label of any kind.

1. **Labels.** Six yes/no labels: `1dAVb`, `RBBB`, `LBBB`, `SB`, `AF` and `ST` [ZEN-CODE15]. These are heart rhythm and conduction problems (problems with how the electrical signal travels). **Careful: `ST` means "sinus tachycardia" (a fast heart rhythm that starts in the heart's normal pacemaker). It does NOT mean ST elevation** [ZEN-CODE15]. There are also `normal_ecg` (set by an automatic system), `death`, `timey` (for the first exam only) and an age guessed by a computer model [ZEN-CODE15]. Number of "yes" answers: 1dAVb 5,716; RBBB 9,672; LBBB 6,026; SB 5,605; ST 7,584; AF 7,033; normal_ecg 134,657 [OBS-CODE15]. 308,004 exams have none of the six labels. 173,347 have none of the six and are also not marked "normal" [OBS-CODE15].
2. **Who labelled them.** For the full CODE dataset (the larger set this 15% comes from), labels came from three places: automatic statements from the Uni-G program, Minnesota codes (a standard coding system for ECGs), and "text labels extracted from the expert text reports" [RIBEIRO2020]. 34,512 unclear exams were "manually reviewed by medical students … under the supervision of a certified cardiologist" [RIBEIRO2020]. `normal_ecg` comes from an automatic system [ZEN-CODE15]. Whether the 15% part was labelled in exactly the same way: **not found**. The dataset page does not say [ZEN-CODE15].
3. **Collection.** Telehealth Network of Minas Gerais (TNMG), Brazil. It covers "811 out of the 853 municipalities" of the state. 2010 to 2016 [ZEN-CODE15; RIBEIRO2020]. 345,779 exams from 233,770 patients. 66,929 patients have more than one exam (at most 38) [OBS-CODE15].
4. **Setting.** For the full CODE dataset: "performed mostly in primary care facilities" (local health centres, not hospitals) [RIBEIRO2020]. For the 15% part, the paper's statement about full CODE is the only information we found.
5. **Device.** Full CODE: TEB ECGPC (Tecnologia Eletrônica Brasileira) or Micromed ErgoPC 13 machines. 7–10 seconds, first recorded at 300 to 600 Hz [RIBEIRO2020]. The shared files are all at 400 Hz. Each ECG is stored as 4,096 samples × 12 leads, in the order DI, DII, DIII, AVR, AVL, AVF, V1–V6 [ZEN-CODE15]. Shorter ECGs are filled with zeros at both ends. For example, a 7-second ECG has 2,800 real samples and 648 zeros at each end [ZEN-CODE15]. The unit of the stored numbers (for example millivolts): **not found** on the dataset page [ZEN-CODE15].
6. **STEMI vs NSTEMI.** **Neither.** There is no MI label, no ischaemia (low blood flow to the heart muscle) label, and no ST-segment label. The `ST` column is sinus tachycardia [OBS-CODE15; ZEN-CODE15]. The paper says it "did not test the accuracy of the DNN in the diagnosis of other classes", and names MI as future work [RIBEIRO2020].
7. **Best model use.** *This is the planner's view. The clinical supervisor still needs to agree.* Pretraining only, or not useful for the heart-attack task (`data_contract.md` L11). Before use, someone must check the number scale (units) and change the speed from 400 Hz to the model's rate (`data_contract.md` C2.2).
8. **Combining.** *(See also the table in section 7.)* 400 Hz, so the speed must be changed. 7–10 seconds with zero padding, so the model needs a "padding mask" that marks which samples are not real (`data_contract.md` P2) [ZEN-CODE15]. Each exam has a patient number [OBS-CODE15]. Full CODE: mostly primary care [RIBEIRO2020]. There are no MI labels to combine. Related releases exist (full CODE and the CODE test set). Check for shared ECGs before using them together (`data_contract.md` O10).
9. **Access.** CODE-15% is open, and we downloaded it without a login [ZEN-CODE15; OBS-DOWNLOAD]. The full CODE training data is **not** open: "Restrictions apply to the availability of the training set". It needs an individual request, is for non-commercial use only, and needs a data use agreement [RIBEIRO2020].
10. **Size and license.** 345,779 exams from 233,770 patients. `exams.csv` is 35.5 MB. The signals are in 18 zip files (17 of about 2.7 GB each, plus one of 782.6 MB). All files together are 46.3 GB. License: CC BY 4.0 [ZEN-CODE15].

### 5.11 INCART

**In one line:** a small, open set of 30-minute Holter recordings (long recordings made while the person goes about their day) from 32 patients in Russia. Only 2 patients have "acute MI" in their diagnosis text. This is a very different kind of recording from a 10-second resting ECG.

1. **Labels.** There are three kinds [README-INCART; OBS-INCART]:
   - Beat marks: a mark on each heartbeat, "over 175,000 beat annotations in all". These are stored in `.atr` files, which we did not download.
   - Diagnosis text for each patient, in `files-patients-diagnoses.txt` and in the first comment of each header (age, sex, diagnoses).
   - Rhythm and wave-shape text for each record, in `record-descriptions.txt` and the header comments. For example, record I03 says "ST elevation, PVCs" (PVCs = extra early heartbeats).
2. **Who labelled them.** Beat marks were "produced by an automatic algorithm and then corrected manually". However, their "locations have not been manually corrected" [README-INCART]. About the patient diagnoses, the README says: "Diagnoses were confirmed by enzyme check, coronary angiography, electrophysiological study, pressure monitoring where necessary." (These are a blood test, an X-ray test of the heart arteries, a test of the heart's electrical system, and pressure measurement.) Note the words "where necessary": this does **not** say that every diagnosis was confirmed by every test [README-INCART]. Who wrote the diagnoses: **not found**. "Additional verification was done by Sergey Ivanov and Alexei Rivin (Incart)" [README-INCART].
3. **Collection.** The data came from the St.-Petersburg Institute of Cardiological Technics (Incart), Saint Petersburg, Russia [README-INCART; PN-INCART]. 32 patients "undergoing tests for coronary artery disease" (disease of the heart arteries): 17 men and 15 women, aged 18–80 (average 58). None had a pacemaker [README-INCART]. Records were chosen on purpose, mostly ones "with ECGs consistent with ischemia, coronary artery disease, conduction abnormalities, and arrhythmias" [README-INCART]. So the records are a selected group, not a random sample of patients [README-INCART]. Years: **not found** [README-INCART; PN-INCART].
4. **Setting.** Holter: "75 annotated recordings extracted from 32 Holter records" [README-INCART]. Whether patients were in hospital or outpatients: **not found** [README-INCART].
5. **Device.** 12 standard leads, 257 Hz, 30 minutes [README-INCART]. All 75 headers show 12 signals, 257 Hz and 1,800 seconds, with leads in the order I, II, III, AVR, AVL, AVF, V1–V6 [OBS-INCART]. The scale differs between recordings: the headers show 12 different values, from 240 to 1,063 units per millivolt. The README says "250 to 1100", which does not quite match the headers [README-INCART; OBS-INCART]. The header has no unit field [OBS-INCART]. Machine brand and model: **not found** [README-INCART; PN-INCART].
6. **STEMI vs NSTEMI.** **Neither** [OBS-INCART].
   - "Acute MI" in the diagnosis text: 2 patients (patient 2: records I03–I05; patient 27: records I62–I64) = 6 records.
   - "Earlier MI": 4 patients (11, 21, 24, 32) = 9 records.
   - The record text "ST elevation" appears in I03, I59, I60 and I62. I59 and I60 belong to patient 26, who has no diagnosis text.

   These are short diagnosis texts, not reviewed labels. Two patients are far too few to learn from.
7. **Best model use.** *This is the planner's view. The clinical supervisor still needs to agree.* Not useful for STEMI vs NSTEMI, or for MI vs no MI: only 2 acute-MI patients, 30-minute Holter, 257 Hz. At most, it could be used for pretraining on short cut-out pieces. Whether INCART is in scope at all is still an open question (`data_contract.md` L11, Q8; [MCR p.8]).
8. **Combining.** *(See also the table in section 7.)* 257 Hz, so the speed must be changed. 30-minute Holter, so it must be cut into short pieces [OBS-INCART]. It is a different kind of recording from 10-second resting ECGs. All 10 "hard" dataset pairs in the earlier report involve INCART [MCR p.4]. Patient key: "patient N" (32 patients, 1 to 4 records each) [OBS-INCART]. The 2021 PhysioNet Challenge copy has 74 records instead of 75 [PA2020, Table 2]. **Never mix the two copies** (`data_contract.md` O3). Which record is missing: not checked.
9. **Access.** Open: "Anyone can access the files…". We needed no login [PN-INCART; OBS-DOWNLOAD].
10. **Size and license.** 75 records from 32 patients. 794.5 MB unpacked. License: ODC Attribution License v1.0 (free to use if you credit the source). DOI 10.13026/C2V88N. Published 1 May 2008 [PN-INCART].

## 6. Which datasets to use for which model

*This whole section is the planner's assessment for the user and the clinical supervisor. It is not a decision* [REC].

**First: no open dataset of the 11 can train a STEMI-vs-NSTEMI model.** None has STEMI or NSTEMI labels in its open files. The only route is MIMIC-IV-ECG, through the credentialed diagnosis codes. That count is **not checked yet: needs credentialed access; the user will run the count script** [REC; PN-MIMICECG-ICD].

| Model | Datasets | Why |
|---|---|---|
| STEMI vs NSTEMI | **MIMIC-IV-ECG only, if** linked to credentialed diagnosis codes and reviewed | No other dataset has STEMI or NSTEMI labels (section 4). Discharge codes describe the hospital stay, not the ECG time (section 5.2) |
| MI vs non-MI (report-statement level, **only after clinical review**) | PTB-XL (5,469 MI-statement ECGs; 150 early stage), PTB Diagnostic (148 MI patients with infarction dates; 52 healthy), SPH (260; 7 "acute"), CPSC-Extra (MI 376 / old MI 1,168) | These have MI statements. A missing MI code does **not** mean "no heart attack" (`data_contract.md` L1) |
| External test only (data kept apart, used only to check the finished model) | PTB Diagnostic (documented time since infarction vs healthy people), SPH (a different hospital and label system), both after review | Different sources from the training data give a fairer test |
| Pretraining (the model first learns general ECG patterns, without heart-attack labels) | CODE-15%, Chapman-Shaoxing, Ningbo, CPSC 2018, Georgia, MIMIC-IV-ECG (without labels), INCART (short cut-out pieces only) | Many ECGs, but no usable heart-attack labels |
| Not useful for a supervised heart-attack model | INCART | 30-minute Holter, 257 Hz, only 2 acute-MI patients (section 5.11) |

All of this needs the supervisor's agreement on what counts as a "new" heart attack and what counts as "no heart attack" (section 9).

<!-- section: A4-L -->

## 7. Datasets that can and cannot be combined

"Combine" means putting two datasets together to train one model. **"After checks" does not mean approved.** No pair is approved for training a combined model yet (`data_contract.md` C2.10, C2.11). The table only says what must be checked first [CMB].

Each cell shows the number of checks needed, then which checks (letters a–g below). **No** = should not be combined for heart-attack training. Result: 45 pairs "after checks", 10 pairs "No" (every pair with INCART), 0 pairs ready as they are [CMB].

| | PTB-XL | MIMIC | PTB-Diag | SPH | CPSC | CPSC-Ex | Georgia | Ningbo | Chapman | CODE-15 | INCART |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **PTB-XL** | – | 3 (c,d,f) | 5 (a,b,c,d,f) | 3 (b,d,f) | 3 (b,e,f) | 3 (b,e,f) | 3 (b,e,f) | 2 (e,f) | 2 (e,f) | 5 (a,b,c,d,f) | **No** |
| **MIMIC** | 3 (c,d,f) | – | 5 (a,b,c,d,f) | 4 (b,c,d,f) | 5 (b,c,d,e,f) | 5 (b,c,d,e,f) | 5 (b,c,d,e,f) | 4 (c,d,e,f) | 4 (c,d,e,f) | 5 (a,b,c,d,f) | **No** |
| **PTB-Diag** | 5 (a,b,c,d,f) | 5 (a,b,c,d,f) | – | 5 (a,b,c,d,f) | 6 (a,b,c,d,e,f) | 6 (a,b,c,d,e,f) | 6 (a,b,c,d,e,f) | 6 (a,b,c,d,e,f) | 6 (a,b,c,d,e,f) | 5 (a,b,c,d,f) | **No** |
| **SPH** | 3 (b,d,f) | 4 (b,c,d,f) | 5 (a,b,c,d,f) | – | 4 (b,d,e,f) | 4 (b,d,e,f) | 4 (b,d,e,f) | 4 (b,d,e,f) | 4 (b,d,e,f) | 5 (a,b,c,d,f) | **No** |
| **CPSC** | 3 (b,e,f) | 5 (b,c,d,e,f) | 6 (a,b,c,d,e,f) | 4 (b,d,e,f) | – | 3 (b,e,g) | 2 (b,e) | 2 (b,e) | 2 (b,e) | 6 (a,b,c,d,e,f) | **No** |
| **CPSC-Ex** | 3 (b,e,f) | 5 (b,c,d,e,f) | 6 (a,b,c,d,e,f) | 4 (b,d,e,f) | 3 (b,e,g) | – | 2 (b,e) | 2 (b,e) | 2 (b,e) | 6 (a,b,c,d,e,f) | **No** |
| **Georgia** | 3 (b,e,f) | 5 (b,c,d,e,f) | 6 (a,b,c,d,e,f) | 4 (b,d,e,f) | 2 (b,e) | 2 (b,e) | – | 2 (b,e) | 2 (b,e) | 6 (a,b,c,d,e,f) | **No** |
| **Ningbo** | 2 (e,f) | 4 (c,d,e,f) | 6 (a,b,c,d,e,f) | 4 (b,d,e,f) | 2 (b,e) | 2 (b,e) | 2 (b,e) | – | 2 (e,g) | 6 (a,b,c,d,e,f) | **No** |
| **Chapman** | 2 (e,f) | 4 (c,d,e,f) | 6 (a,b,c,d,e,f) | 4 (b,d,e,f) | 2 (b,e) | 2 (b,e) | 2 (b,e) | 2 (e,g) | – | 6 (a,b,c,d,e,f) | **No** |
| **CODE-15** | 5 (a,b,c,d,f) | 5 (a,b,c,d,f) | 5 (a,b,c,d,f) | 5 (a,b,c,d,f) | 6 (a,b,c,d,e,f) | 6 (a,b,c,d,e,f) | 6 (a,b,c,d,e,f) | 6 (a,b,c,d,e,f) | 6 (a,b,c,d,e,f) | – | **No** |
| **INCART** | **No** | **No** | **No** | **No** | **No** | **No** | **No** | **No** | **No** | **No** | – |

**What the letters mean** [CMB]:

- **a. Change the speed:** one dataset is not recorded at 500 Hz (PTB Diagnostic 1000 Hz, CODE-15% 400 Hz).
- **b. Length rule:** recordings are not all 10 seconds, so they must be cut or padded the same way.
- **c. Match leads by name:** the lead order or lead names differ (MIMIC aVF before aVL; PTB Diagnostic 15 channels with lower-case names; CODE-15% names DI, DII, DIII).
- **d. Check the scale:** units per millivolt differ, or are unknown (SPH and CODE-15% scale unknown; the planner counts "unknown" as needing a check).
- **e. No patient ID:** one patient's recordings cannot be kept together, so this dataset can be used for training only (`data_contract.md` S7).
- **f. Different label systems:** for example SCP-ECG vs SNOMED CT vs AHA vs free text. Labels must be matched first.
- **g. Shared recordings possible:** CPSC 2018 + CPSC-Extra (same origin, `data_contract.md` O5) and Chapman-Shaoxing + Ningbo (same export; never add ecg-arrhythmia on top, O4).
- **No:** INCART is 30-minute Holter at 257 Hz, a different kind of recording. At most it can be cut into pieces for pretraining [MCR p.4].

**Pairs that need the fewest checks (2)** [CMB]:

- PTB-XL + Chapman-Shaoxing, PTB-XL + Ningbo: no patient ID on the Challenge side (e); different labels (f).
- CPSC 2018, CPSC-Extra or Georgia with Georgia, Chapman-Shaoxing or Ningbo: length rule (b); no patient ID (e).
- Chapman-Shaoxing + Ningbo: no patient ID (e); same export, so check for shared recordings (g).

**The first pair from the earlier reports, PTB-XL + MIMIC-IV-ECG** [CMP p.4]: 3 checks. Match leads by name (MIMIC has aVF before aVL), check the scale (1,000 vs 200 units per millivolt), and match the label systems (SCP-ECG statements vs machine text or credentialed diagnosis codes) [CMB; OBS-PTBXL; OBS-MIMIC].

**Copies that are not in the table.** These are other copies of the same ECGs. They must never be combined with the original:

- The 2021 Challenge copy of **PTB-XL** (21,837 recordings): every native PTB-XL ID number is also in it. Treat it as the same ECGs (ID check; that the numbers match one to one is an assumption) [OBS-OVERLAP].
- The 2021 Challenge copy of **PTB Diagnostic** (516 of 549): treat it as the same ECGs (ID check; matching by position is an assumption) [OBS-OVERLAP].
- **ecg-arrhythmia** (45,152) = Chapman-Shaoxing + Ningbo (count match only) [PN-ECGARR; PN-CHALLENGE2021].
- The 2021 Challenge copy of **INCART** (74 records vs 75) [PA2020, Table 2].
- **MIMIC-IV-ECG-ext-ICD** gives labels for the **same** ECGs as MIMIC-IV-ECG. It is not a separate dataset [EXTRA-DERIVED].

<!-- section: A4 -->

## 8. Warnings

Datasets that could mislead a model.

- **Different lead order or scale:** In our samples (50 MIMIC and 20 PTB-XL headers), MIMIC-IV-ECG stores the leads in the order I, II, III, aVR, **aVF, aVL**, V1–V6, while PTB-XL uses I, II, III, AVR, **AVL, AVF**, V1–V6. The scale is also different in these samples (200 vs 1,000 units per millivolt) [OBS-MIMIC; OBS-PTBXL]. These are samples, so other files could differ. If leads are matched by position instead of by name, two leads are silently swapped and the data is quietly corrupted. The model would still train, so nobody would notice. Always match leads by name and check units (`data_contract.md` P4, C2.9).
- **Different kind of patients:** Middle (median) age in our samples of one folder each: CPSC 2018 64, CPSC-Extra 65, Georgia 63, Chapman-Shaoxing 61, **Ningbo 38** [OBS-CPSC; OBS-CPSCX; OBS-GEORGIA; OBS-CHAPMAN; OBS-NINGBO]. *Planner's note:* if datasets with different age mixes are combined, a model may partly learn age differences rather than heart disease, so check the age mix before combining.
- **Wrong setting:** ECGs recorded over many hours, or in a different place, look different from a 10-second ECG taken in hospital.
  - **INCART** is 30-minute Holter recordings at 257 Hz. All 10 "hard" pairs in the earlier report involve INCART [README-INCART; MCR p.4].
  - **CODE-15%** comes from tele-ECG, and the full CODE dataset was recorded "mostly in primary care facilities" [RIBEIRO2020].
  - For most datasets the setting was **not found** (section 9). Only MIMIC-IV-ECG states it for the dataset as a whole, and even there it is not given per ECG [PN-MIMICECG; OBS-MIMIC].
- **Weak labels:** labels written by a computer, or labels that do not say whether the heart attack is new or old.
  - **Machine-written reports:** the open MIMIC-IV-ECG reports are written by the ECG machine [PN-MIMICECG]. About 31% of PTB-XL first reports were written by the machine [WAGNER2020]. CODE-15%'s `normal_ecg` comes from an automatic system [ZEN-CODE15].
  - **PTB-XL likelihood 100 does not mean new:** it measures report wording, and "status post" (a past event) also gives 100 [WAGNER2020, Table 4].
  - **"Acute" as a word, without timing:** SPH has 7 MI statements with "acute" [OBS-SPH]. Ningbo has 49 "acute MI" labels whose original label is unknown [DXMAP; OBS-NINGBO]. Neither is a reviewed new heart attack.
  - **Mostly old heart attacks:** CPSC-Extra has 1,168 "old MI" labels vs 376 "MI" [DXMAP].
  - **Lost detail:** in Chapman-Shaoxing, all heart-attack locations were merged into one code [OBS-CHAPMAN].
  - **Label quality varies** between the Challenge datasets, and "some of the data and labels are likely to have errors" [PA2020, §2.1.2; PN-CHALLENGE2021].
- **Same patients or same ECGs in two places:** Example of the problem: if the same ECG is in both the training data and the test data, the model looks better than it really is.
  - **CPSC 2018 and Georgia have no patient ID, but some patients have more than one recording** (CPSC: 13,256 recordings from 9,458 patients; Georgia: 20,678 recordings from 15,742 patients). So recordings from one patient cannot be kept together. The same person could end up in both training and testing [PA2020, Table 1; OBS-CPSC; OBS-GEORGIA]. CPSC-Extra also has no patient ID, and its number of patients was not found [OBS-CPSCX].
  - **Ningbo, Chapman-Shaoxing and CPSC-Extra** also have no patient ID in their headers [OBS-NINGBO; OBS-CHAPMAN; OBS-CPSCX].
  - **Copies of the same ECGs:** the Challenge copies of PTB-XL and PTB Diagnostic (ID check; one-to-one matching is an assumption), ecg-arrhythmia vs Chapman-Shaoxing + Ningbo (count match), and the two INCART copies (74 vs 75). See section 7 [OBS-OVERLAP; PN-ECGARR; PA2020].
  - **CPSC 2018 and CPSC-Extra** come from the same contest. Their different file-name letters (A… vs Q…) do not prove the recordings are different. No one has compared them [OBS-OVERLAP].
  - **PTB-XL 100 Hz files** are the same ECGs as the 500 Hz files. Count them once [PN-PTBXL].
  - **No one has compared the signals themselves** between any datasets, so hidden copies cannot be ruled out (`data_contract.md` O9).

## 9. What is not known yet

Each item says where we looked. Section 5 gives the details for each dataset.

**Facts we could not find**

| What | Not found for | Where we looked |
|---|---|---|
| Setting (emergency room, ward, clinic…) | PTB-XL, SPH, CPSC 2018, CPSC-Extra, Georgia, Ningbo, Chapman-Shaoxing. Partly: PTB Diagnostic (ward type), INCART (in- or outpatient), CODE-15% (only stated for full CODE), MIMIC-IV-ECG (not per ECG) | Dataset pages, papers, Challenge page [PN-PTBXL; WAGNER2020; LIU2022; PN-CHALLENGE2021; PA2020; PN-ECGARR; ZH2020; PN-PTBDB; README-INCART; RIBEIRO2020; OBS-MIMIC] |
| Who wrote the labels | PTB Diagnostic, CPSC 2018, CPSC-Extra, Georgia, Ningbo (alone), INCART (diagnoses), CODE-15% (the 15% part) | Dataset pages, Challenge pages and papers. The CPSC 2018 paper page refused access [PN-PTBDB; PN-CHALLENGE2021; PA2020; PN-ECGARR; README-INCART; ZEN-CODE15] |
| Collection years | PTB Diagnostic, CPSC 2018, CPSC-Extra, Georgia, Ningbo, Chapman-Shaoxing, INCART | Dataset pages and papers [PN-PTBDB; PN-CHALLENGE2021; PA2020; ZH2020; README-INCART; PN-INCART] |
| ECG machine model | CPSC 2018, CPSC-Extra, Georgia, INCART. Chapman-Shaoxing and Ningbo name only a storage system (GE MUSE) | Dataset pages and papers [PN-CHALLENGE2021; PA2020; README-INCART; ZH2020; PN-ECGARR] |
| Number of patients | CPSC-Extra; CPSC 2018 (shared part) | Challenge page and paper [PN-CHALLENGE2021; PA2020] |
| Scale (units) of the numbers | CODE-15% (not stated); SPH (no header was read) | [ZEN-CODE15; CMB] |
| Country | PTB-XL (not stated on the dataset page) | [PN-PTBXL] |
| Counts of machine MI/ST statements | MIMIC-IV-ECG (file not downloaded) | [OBS-MIMIC] |

**Questions for the user and the clinical supervisor**

- **MIMIC diagnosis-code count.** The user will run `src/stemi/review/mimic_icd_count.py` with their own credentialed access. Until then: not checked yet: needs credentialed access; the user will run the count script (`STATUS.md`, U1).
- **Which diagnosis codes mean STEMI, and which mean NSTEMI?** The supervisor must sign off this list before any count is used as a label.
- **What counts as "acute" (new)?** For example, how many days between the heart attack and the ECG (`data_contract.md` Q2). This decides how to use PTB Diagnostic's dates and the "acute" words in SPH and Ningbo.
- **What counts as proof of "no heart attack"?** A missing code is not enough (`data_contract.md` L1, Q4).
- **PTB Diagnostic "Lytic agent" field:** does it tell us anything about STEMI? This report does not use it as a label (section 5.3).
- **Datasets without patient IDs:** may they be used for training only, with recordings as the unit (`data_contract.md` Q6, S7)?
- **INCART:** is it in scope at all (`data_contract.md` Q8)?
- **Other datasets** in Appendix A: is it worth asking for access to any of them?



**Conflicts inside the publishers' own files**

- **INCART, number of patients with "transient ischemic attack (angina pectoris)".** The README says 5 patients. The file `files-patients-diagnoses.txt` lists 4 (patients 3, 7, 8 and 18 = 7 records). We could not resolve this. Only the publisher could [README-INCART; OBS-INCART].
- **Georgia, number of ECGs.** The Challenge page says "This source contains 20,672 ECGs". The Challenge paper gives 20,678 recordings. The 6-recording difference is not explained [PN-CHALLENGE2021; PA2020, Tables 1–2].
- **Chapman-Shaoxing, number of records.** The original release had 10,646 records. The Challenge folder has 10,247. The sources we read do not explain the difference [ZH2020; PN-CHALLENGE2021].
- **ecg-arrhythmia: patients or ECGs?** The ecg-arrhythmia page calls its 45,152 items "patients" in one place and "ECGs" in another. The number of different patients is not established [PN-ECGARR].

## Appendix A. Other datasets worth checking (not reviewed in depth)

These datasets were found in a short extra search. They were **not** reviewed like the 11 datasets above. They are not in the tables in sections 3 and 4, in the advice in section 6, or in the table in section 7. Only facts the planner checked are given.

- **wECGdb (Zenodo 15235775, published 18 Apr 2025).** "An ECG database acquired using a wrist-worn device from patients with acute myocardial infarction and controls". 92 people in 3 groups: healthy; acute MI ("patients diagnosed with either STEMI or NSTEMI, with ECGs taken within 24 hours of percutaneous coronary intervention", which is a procedure to open a blocked heart artery); and other heart disease with "infarction-like changes in the ECG". From "the inpatient wards of the Cardiology Department at Vilnius University Hospital Santaros Klinikos, Lithuania". A wrist device recorded lead I plus one non-standard chest lead at 500 Hz. A standard 12-lead ECG (Euroholter 12view, Lumed) was recorded at 200 Hz and changed to 500 Hz. **Careful:** the ECGs were taken after the artery was opened, not when the patient arrived. Who confirmed the diagnosis, and whether each record says STEMI or NSTEMI: **not found** (files not opened). Open; CC BY 4.0; about 1.0 GB [ZEN-WECG].
- **STAFF III (PhysioNet staffiii 1.0.0).** "Standard 12-lead ECG recordings from 104 patients" during 152 planned balloon blockages of a heart artery (LAD 58, RCA 59, LCX 32, left main 3). "Only patients receiving elective PTCA … were included" (planned treatment, no emergencies). "Based on ECG criteria, 35 patients had previous myocardial infarction." Charleston Area Medical Center, West Virginia, USA, 1995–96; 1000 Hz; limb leads placed in a different way (Mason-Likar); 3.2 GB; open; ODC Attribution v1.0. It shows short, planned low blood flow, **not** real heart attacks, and has no STEMI or NSTEMI labels [PN-STAFF3].
- **Prehospital "OMI" ECGs (Riek et al., ECG-SMART-NET, arXiv 2405.09567).** ECGs from three ambulance services (Pittsburgh, Pennsylvania, and two in North Carolina). 11,309 ambulance ECGs from adults with non-injury chest pain; the analysed set is 10,393 ECGs from 7,397 patients (7.2% OMI). OMI means occlusion myocardial infarction: a blocked heart artery, defined in the paper by blood-flow grade on angiography. Devices: HeartStart MRX (Philips) and LIFEPAK 15. "OMI labels were created using angiographically defined culprit lesions" (from an X-ray test of the heart arteries). **OMI vs no OMI is not the same as STEMI vs NSTEMI.** Data availability: **not found** in the paper; treat it as not public [RIEK].
- **HEEDB (Harvard-Emory ECG Database).** "A large collection of 12-lead electrocardiography (ECG) recordings". Controlled access with a data user agreement ("BDSP Restricted Health Data License 1.0.0"). Size, label types and whether it has STEMI or NSTEMI labels: **not found** (the pages we tried did not open) [AWS-HEEDB].
- **University of Michigan pre/post-STEMI ECGs (Deep Blue, DOI 10.7302/gk9v-ka27).** **Could not be checked:** the page blocked automated reading. No facts are given here. The user can open it in a browser.
- **Derived from the 11:** MIMIC-IV-ECG-ext-ICD gives diagnosis codes for the **same** ECGs as MIMIC-IV-ECG (credentialed) [EXTRA-DERIVED]. PTB-XL+: not checked.

## 10. Sources

Every fact in the report cites one of these sources in square brackets. PDF pages are written like [MCR p.4].

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
- **[PN-PTBDB]** PTB Diagnostic ECG Database, release 1.0.0, PhysioNet. https://physionet.org/content/ptbdb/1.0.0/ (checked 2026-10-20).
- **[PA2020]** Perez Alday E.A. et al., 2020. "Classification of 12-lead ECGs: the PhysioNet/Computing in Cardiology Challenge 2020", *Physiological Measurement*. https://pmc.ncbi.nlm.nih.gov/articles/PMC8015789/ (sections used: Table 2; §2.1.2).
- **[PN-INCART]** St Petersburg INCART 12-lead Arrhythmia Database, release 1.0.0, PhysioNet. https://physionet.org/content/incartdb/1.0.0/ (checked 2026-10-20).
- **[README-INCART]** The publisher's README file from the INCART release 1.0.0 file set (downloaded 2026-10-20; quoted word for word).
- **[PN-MIMICECG]** MIMIC-IV-ECG: Diagnostic Electrocardiogram Matched Subset, release 1.0, PhysioNet. https://physionet.org/content/mimic-iv-ecg/1.0/ (checked 2026-10-21).
- **[PN-MIMICECG-ICD]** MIMIC-IV-ECG-ext-ICD (diagnosis labels for MIMIC-IV-ECG), release 1.0.1, PhysioNet (credentialed; only the public page was read). https://physionet.org/content/mimic-iv-ecg-ext-icd-labels/1.0.1/
- **[ZH2020]** Zheng J. et al., 2020. "A 12-lead electrocardiogram database for arrhythmia research covering more than 10,000 patients", *Scientific Data* (the Chapman-Shaoxing dataset paper). https://pmc.ncbi.nlm.nih.gov/articles/PMC7016169/
- **[PN-ECGARR]** A large scale 12-lead electrocardiogram database for arrhythmia study ("ecg-arrhythmia"), release 1.0.0, PhysioNet. https://physionet.org/content/ecg-arrhythmia/1.0.0/ (checked 2026-10-20).
- **[ZEN-WECG]** wECGdb on Zenodo. https://zenodo.org/records/15235775 and https://zenodo.org/api/records/15235775
- **[PN-STAFF3]** STAFF III Database, release 1.0.0, PhysioNet. https://physionet.org/content/staffiii/1.0.0/
- **[RIEK]** Riek et al., ECG-SMART-NET. https://arxiv.org/abs/2405.09567 (abstract and Methods).
- **[AWS-HEEDB]** Harvard-Emory ECG Database, AWS Open Data Registry. https://registry.opendata.aws/bdsp-heedb/
- **[EXTRA-DERIVED]** MIMIC-IV-ECG-ext-ICD public page (as [PN-MIMICECG-ICD]), used for the "derived datasets" note.
- **[PN-CHALLENGE2021]** PhysioNet/Computing in Cardiology Challenge 2021, release 1.0.3. https://physionet.org/content/challenge-2021/1.0.3/ (checked 2026-10-20), and the Challenge web page https://moody-challenge.physionet.org/2021/.
- **[DXMAP]** The Challenge 2021 label files `dx_mapping_scored.csv` and `dx_mapping_unscored.csv` (from the Challenge evaluation code; our copy downloaded 2026-10-20, checksum in `download_manifest.csv`; these files can change). They give a count per label for each source. What the counts count is **not defined** by the publisher. Counts are in `results/challenge_dx_mapping_counts.csv` (recounted by the planner).

### Result files made by this team

All are in `results/`. Each one describes the files we downloaded on 2026-10-20, not every copy of the dataset.

- **[OBS-PTBXL]** PTB-XL counts: `ptb_xl_summary.md`, `ptb_xl_scp_counts.csv`, `ptb_xl_field_counts.csv`, `ptb_xl_mi_by_stadium.csv`, `ptb_xl_mi_early_stadium.csv`, `ptb_xl_headers.csv` (recounted by the planner).
- **[OBS-SPH]** SPH counts from `metadata.csv` and `code.csv`: `sph_summary.md`, `sph_code_counts.csv`, `sph_code_modifier_counts.csv`, `sph_mi_timing.csv` (recounted by the planner).
- **[OBS-CODE15]** CODE-15% counts from `exams.csv`: `code15_summary.md`, `code15_label_counts.csv` (recounted by the planner).
- **[OBS-PTBDB]** PTB Diagnostic counts from all 549 headers and the `RECORDS` / `CONTROLS` lists: `ptb_diagnostic_summary.md`, `ptb_diagnostic_comment_counts.csv`, `ptb_diagnostic_records.csv`, `ptb_diagnostic_mi_timing.csv`, `ptb_diagnostic_mi_patient_timing.csv`, `ptb_diagnostic_mi_lytic_agent.csv` (recounted by the planner).
- **[OBS-INCART]** INCART checks of all 75 headers, `files-patients-diagnoses.txt` and `record-descriptions.txt`: `incart_summary.md`, `incart_headers.csv` (checked by the planner).
- **[OBS-CPSC]**, **[OBS-CPSCX]**, **[OBS-GEORGIA]**, **[OBS-CHAPMAN]**, **[OBS-NINGBO]** Counts from a sample of one folder (`g1`, 999 headers) for each dataset: `challenge_<dataset>_summary.md`, `challenge_<dataset>_dx_counts.csv`, `challenge_<dataset>_headers.csv`, `challenge_<dataset>_comment_keys.csv`, where `<dataset>` is `cpsc_2018`, `cpsc_extra`, `georgia`, `chapman_shaoxing` or `ningbo` (recounted by the planner). [OBS-CHAPMAN] and [OBS-NINGBO] also cover the original release's `ConditionNames_SNOMED-CT.csv`.
- **[OBS-MIMIC]** MIMIC-IV-ECG counts from `record_list.csv`, `machine_measurements_data_dictionary.csv` and a sample of 50 headers: `mimic_iv_ecg_summary.md`, `mimic_iv_ecg_headers.csv` (recounted by the planner); download check in `download_plausibility.csv`.
- **[OBS-OVERLAP]** ID-level overlap checks: `overlap_ids.csv`, `overlap_ids_summary.md` (Challenge PTB-XL and PTB copies; CPSC file names) (checked by the planner).
- **[CMB]** The combine table: `combine_matrix.csv`, `combine_matrix_summary.md` (55 pairs, made by a script from verified rows under rules a–g set by the planner; the planner spot-checked 7 pairs).
- **[REC]** The planner's per-model assessment (row "S10 recommend" in `verified_facts.md`).
- **[OBS-DOWNLOAD]** `download_manifest.csv`: what was downloaded, from where, and its checksum.
- All checked facts: `verified_facts.md`.
