# ECG Datasets for STEMI and NSTEMI Prediction: A Simple Review

| | |
|---|---|
| Status | **FINAL (2026-10-21).** All facts come from rows marked verified in `results/verified_facts.md`. MIMIC STEMI/NSTEMI counts are pending the user's script. |
| Date | 2026-10-21 |
| Written by | documenter (team: planner, coder, team-lead) |
| Plan | `docs/project/PLAN.md` (approved by the user on 2026-10-20) |

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

<!-- section: A4-L -->

## 4b. Which labels each dataset has

This table shows labels that several datasets share. Each label is explained in brackets in plain words [XWALK].

**This table is a team mapping for the clinical supervisor to review.** The team matched labels from different code systems by meaning. A match here is not an official mapping from the publishers [XWALK].

| Label (plain English) | PTB-XL | MIMIC | PTB-Diag | SPH | CPSC | CPSC-Ex | Georgia | Ningbo | Chapman | CODE-15 | INCART |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Normal ECG (the ECG shows no problem) | 9,514 | not checked | not present | 13,905 | not present | not present | not present | not present | not present | 134,657 | not present |
| Sinus rhythm (the normal heartbeat, started by the heart's own pacemaker) | 16,748 | not checked | not present | not present | 918 | 4 | 1,752 | 6,299 | 1,826 | not present | not present |
| Sinus bradycardia (a slow heartbeat that starts in the heart's normal pacemaker) | 637 | not checked | not present | 2,711 | 0 (listed, count 0) | 45 | 1,677 | 12,670 | 3,889 | 5,605 | not present |
| Sinus tachycardia (a fast heartbeat that starts in the heart's normal pacemaker) | 826 | not checked | not present | 725 | 0 (listed, count 0) | 303 | 1,261 | 5,687 | 1,568 | 7,584 | not present |
| Atrial fibrillation (the upper heart chambers beat in a fast, irregular, chaotic way) | 1,514 | not checked | not present | 675 | 1,221 | 153 | 570 | 0 (listed, count 0) | 1,780 | 7,033 | 2 |
| Atrial flutter (the upper heart chambers beat fast in a regular, circling pattern) | 73 | not checked | not present | 99 | 0 (listed, count 0) | 54 | 186 | 7,615 | 445 | not present | not present |
| 1st-degree AV block (the signal from the upper to the lower heart chambers is slowed) | 793 | not checked | not present | not present | 722 | 106 | 769 | 893 | 247 | 5,716 | not present |
| LBBB (left bundle branch block: a delay in the heart's electrical wiring on the left side) | 536 | not checked | not present | 84 | 236 | 38 | 231 | 248 | 205 | 6,026 | not present |
| RBBB, complete (right bundle branch block: a delay in the heart's electrical wiring on the right side) | 541 | not checked | not present | 710 | 1,857 | 114 | 570 | 1,291 | 454 | 9,672 | 2 |
| RBBB, incomplete (a partial delay in the wiring on the right side) | 1,118 | not checked | not present | 1,259 | 0 (listed, count 0) | 86 | 407 | 246 | 0 (listed, count 0) | not present | not present |
| LAFB (left anterior fascicular block: a delay in one front branch of the left-side wiring) | 1,623 | not checked | not present | 154 | 0 (listed, count 0) | 0 (listed, count 0) | 180 | 380 | 0 (listed, count 0) | not present | not present |
| PAC (premature atrial contraction: an extra, early beat from the upper chambers) | 398 | not checked | not present | 539 | 616 | 126 | 640 | 1,063 | 258 | not present | 3 |
| PVC (premature ventricular contraction: an extra, early beat from the lower chambers) | 1,143 | not checked | not present | 1,067 | 0 (listed, count 0) | 196 | 357 | 1,091 | 294 | not present | 50 |
| LVH (left ventricular hypertrophy: the wall of the main pumping chamber is thickened) | 2,132 | not checked | not present | 209 | 0 (listed, count 0) | 158 | 1,232 | 632 | 15 | not present | 11 |
| Long QT (the heart takes longer than usual to recharge between beats) | 117 | not checked | not present | 24 | 0 (listed, count 0) | 4 | 1,391 | 337 | 57 | not present | not present |
| MI, any (any heart-attack label, new or old) | 5,469 | not checked | 368 | 260 | 0 (listed, count 0) | 1,606 | 7 | 189 | 40 | not present | 15 |
| Old MI (a heart attack in the past) | not present | not checked | 85 | 233 | 0 (listed, count 0) | 1,168 | 0 (listed, count 0) | 0 (listed, count 0) | 0 (listed, count 0) | not present | 9 |
| ST elevation (the ST segment of the ECG wave is raised) | 28 | not checked | not present | 37 | 220 | 66 | 134 | 0 (listed, count 0) | 176 | not present | 4 |
| ST depression (the ST segment of the ECG wave is lowered) | 1,009 | not checked | not present | 1,024 | 869 | 58 | 38 | 1,266 | 402 | not present | 4 |
| Ischaemia, any (low blood flow to the heart muscle) | 2,467 | not checked | not present | not present | 0 (listed, count 0) | 546 | 1,636 | 0 (listed, count 0) | 0 (listed, count 0) | not present | not present |
| T-wave abnormality (the T wave, the last part of each beat on the ECG, has an unusual shape) | 35 | not checked | not present | 2,218 | 0 (listed, count 0) | 22 | 2,306 | 5,167 | 1,876 | not present | not present |

**How to read the cells** [XWALK]:

- **A number** = how many have this label. PTB-XL, SPH, PTB Diagnostic and INCART: ECG records. CODE-15%: exams. The five Challenge datasets: publisher's count as listed. Where several codes are added up, the sum may count one recording twice.
- **0 (listed, count 0)** = the label is in the dataset's label list, but its count is 0.
- **not present** = the label is not in the dataset's label list at all.
- **not checked** = we could not check. For MIMIC-IV-ECG: not checked: label file not downloaded.

**Notes** [XWALK]:

- CODE-15% `ST` means sinus tachycardia, not ST elevation. Its `normal_ecg` flag comes from an automatic system.
- Chapman-Shaoxing and Ningbo: the LBBB code may also include fascicular blocks (blocks in smaller branches of the left wiring).
- PTB-XL "ST elevation" is the code "non-specific ST elevation" (28 ECGs).
- **Atrial fibrillation vs atrial flutter (warning).** Ningbo has 0 atrial fibrillation but 7,615 atrial flutter, both in the publisher's file and in our sample (0 and 97). So this is not a mapping error. Chapman-Shaoxing has 1,780 atrial fibrillation and 445 atrial flutter (sample 177 and 46) [AFCHK]. Careful with names: in the original label list, the short form "AF" means atrial **flutter**, and "AFIB" means atrial fibrillation [AFCHK]. *Planner's note:* Ningbo's pattern (no atrial fibrillation, many atrial flutter) is unusual and may reflect how the source labelled rhythms; a model could learn a dataset-specific labelling habit. A clinician should review this before Ningbo rhythm labels are used.
- Chapman-Shaoxing and Ningbo: all heart-attack wall locations (front, back, lower, side) map to one MI code, so the location is lost (section 5.9) [XWALK].
- PTB-XL has no "old MI" label. Its separate stage field shows 963 MI-coded ECGs (923 patients) at Stadium III ("old").
- INCART counts come partly from diagnoses given per patient, not per recording.
- "MI, any" includes old heart attacks. These are report labels, not checked diagnoses (`data_contract.md` L2).

The full label list for each dataset is in Appendix B.

<!-- section: A4 -->

## 4c. How each label was made

A label can be made in different ways: by a computer, by one doctor reading the ECG, by a doctor who also saw the health record, or by billing staff after the patient went home. It matters which one. A label made from the whole hospital stay may not describe the moment the ECG was taken. This section shows, for each dataset, the steps from the ECG to the label in our files [PROV; PATH].

How to read the chains below:

- **→** means "then".
- **[OUR FILE]** marks the step our label file comes from.
- **not found** means no source we read describes that step.

### Pathways, step by step

**PTB-XL** [WAGNER2020; PROV; PATH]

1. ECG recorded (Schiller AG machines, Oct 1989 – Jun 1996). The setting is **not found**: the site names are hidden.
2. → A first report, written by a cardiologist (67.13%) or by the ECG machine (31.2%).
3. → Sometimes checked by a cardiologist. Sometimes a second opinion was added (not independent).
4. → **Later, when the dataset was made:** the report text was turned into SCP-ECG codes with a "likelihood". The heart axis and the infarct stage were also taken from the report text. Who did this step, and whether by hand or by computer: **not found**. **[OUR FILE]** (`scp_codes` and the stage columns).
5. Time from ECG to label: **not documented** (the dates were shifted on purpose).

In plain words: every ECG that no person checked had a machine-written first report, but 1,070 machine-written reports were later checked by a person [PROV-XTAB]. Whether the readers saw any health record beyond the ECG: **not found** [WAGNER2020].

**MIMIC-IV-ECG** [PN-MIMICECG; PN-MIMICED; PN-MIMICIV; PN-MIMICECG-ICD; PATH]

1. ECG recorded in the emergency department (ED), the hospital (including intensive care), or outpatient centres. The open files do not say which one for each ECG.
2. Then the ECG can lead to several different labels:
   - (a) **At recording:** the ECG machine writes a report. (Not downloaded.)
   - (b) **Cardiologist reading:** "Most ECG waveforms get read by a cardiologist". These reports are for consortium members only.
   - (c) **ED stay → ED discharge codes:** "These diagnoses are determined by trained coders after discharge from the emergency department". They "are used for billing purposes" and "are exclusively related to the patient's emergency department stay".
   - (d) **Hospital stay → hospital billing codes.** Who assigns them and when: **not stated** on the MIMIC-IV page (it lists them under "hospital billing information").
   - (e) **Linked in 2024 (Ext-ICD):** each ECG's time is matched to an ED stay or a hospital stay, and that stay's discharge codes are attached. **[OUR FILE would be here]**: the user has this table locally (`records_w_diag_icd10.csv`). The team has **not opened it** (credentialed).
3. **Intensive care (ICU) is only a place where ECGs were recorded. It is not a labelling step.** The MIMIC-IV intensive-care module has no diagnosis table, and Ext-ICD uses ED and hospital discharge codes only. So a chain like "ED → ICU → label" is not supported.
4. Our open file (`record_list.csv`) has **no labels**.
5. Time from ECG to label: **not documented**. The only rule is that the ECG was taken "within the stay". ED codes come after ED discharge, and hospital codes describe the whole stay.

**PTB Diagnostic** [PN-PTBDB; PROV; PATH]

1. ECG recorded at the Department of Cardiology, University Clinic Benjamin Franklin, Berlin (patients and healthy volunteers). Ward type: **not found**.
2. → A clinical summary in the header: reason for admission, heart artery test (catheterization), treatment and so on. Who wrote it and when: **not found**. **[OUR FILE]** (header comments).
3. Basis: the clinical work-up, not an ECG reading.
4. Time from ECG to label: **documented**: "ECG date" minus "Infarction date (acute)". For 60 MI patients, the earliest ECG was 0–1 days after the infarction date (section 5.3).

**SPH** [LIU2022; PROV; PATH]

1. ECG recorded at Shandong Provincial Hospital, Jinan (Aug 2019 – Aug 2020), MedEx MECG-200. Setting: **not found**.
2. → The MedEx system measured ECG features, as a reference.
3. → "The responsible cardiologist made the final diagnosis in consideration of the patient health record" (in Chinese).
4. → **Later, for the dataset:** "An experienced cardiologist re-checked all original diagnostic statements and made corrections".
5. → Translated into AHA codes by rules. Records that could not be translated were left out. **[OUR FILE]** (`AHA_Code` in `metadata.csv`).
6. Time from ECG to label: **not documented** (dates shifted).

**CODE-15%** [RIBEIRO2020; ZEN-CODE15; PROV; PATH]

1. ECG recorded "mostly in primary care facilities" on a tele-ECG machine. The tracing is sent "to the TNMG analysis center" together with the patient's clinical history.
2. → "One cardiologist from the TNMG experienced team analyzes the exam" and writes a report.
3. → **Later, for the study:** text labels were taken from these reports and combined with two computer systems (Uni-G and Minnesota codes) by rules. 34,512 unclear exams were "manually reviewed by medical students … under the supervision of a certified cardiologist". **[OUR FILE]** (`exams.csv` columns). This is the method for the full CODE dataset. For the 15% part: **not found**.
4. `normal_ecg` is set by an automatic system.
5. Time from ECG to label: **not documented**.

**Chapman-Shaoxing and Ningbo** [ZH2020; PN-ECGARR; PA2020; PROV; PATH]

1. "12-lead resting ECG", 10 seconds, 500 Hz, stored in the GE MUSE system. Setting: **not found**.
2. → "A licensed physician labeled the rhythm and other cardiac conditions".
3. → A second licensed physician checked the labels.
4. → A senior physician decided when they disagreed.
5. → **Later, for the 2021 Challenge:** mapped to SNOMED CT ("approximate SNOMED CT codes"). **[OUR FILE]** (header `#Dx` and publisher's counts). For Ningbo, the original label behind "acute MI" and "anterior MI" is unknown.
6. Whether the doctors saw more than the ECG: **not found**. Time from ECG to label: **not documented**.

**CPSC 2018, CPSC-Extra and Georgia** [PN-CHALLENGE2021; PA2020; PROV; PATH]

1. ECG recorded: CPSC in China (the contest was in Nanjing); Georgia at Emory University, Atlanta. Settings: **not found**.
2. → Original labelling steps: **not found**. We looked at the Challenge pages, the Challenge paper, and the CPSC 2018 paper, which could not be opened.
3. → **Later, for the 2021 Challenge:** mapped to SNOMED CT (approximate codes). **[OUR FILE]** (header `#Dx` and publisher's counts).
4. Time from ECG to label: **not found**.

**INCART** [README-INCART; PROV; PATH]

1. Holter recordings: "75 annotated recordings extracted from 32 Holter records" of patients "undergoing tests for coronary artery disease".
2. → Patient diagnoses (such as "Acute MI") were "confirmed by enzyme check, coronary angiography, electrophysiological study, pressure monitoring where necessary". Who made them, and when: **not found**. **[OUR FILE]** (`files-patients-diagnoses.txt`, header comments).
3. → Beat marks were "produced by an automatic algorithm and then corrected manually".
4. → Record descriptions (such as "ST elevation"). Author: **not found**.
5. Time from the heart attack to the recording: **not found**.

### Summary table

| Dataset | Who labelled | Basis of the label | Our file comes from | Time from ECG to label |
|---|---|---|---|---|
| PTB-XL | Cardiologist or ECG machine; often checked by a cardiologist | The ECG report; whether more was seen: not found | Report text turned into codes when the dataset was made | Not documented |
| MIMIC-IV-ECG | Machine (open); cardiologist (not open); billing coders (credentialed) | Machine/cardiologist: the ECG. Codes: the whole ED or hospital stay | Open file: no labels. Ext-ICD (stay discharge codes): not opened | Not documented; only "within the stay" |
| PTB Diagnostic | Not found | Clinical work-up | Header clinical summary | **Documented** (ECG date − infarction date) |
| SPH | Cardiologist, then re-checked by an experienced cardiologist | ECG + patient health record | Re-checked statements translated to AHA codes | Not documented |
| CODE-15% | Cardiologist report + computer systems; unclear cases by medical students with a cardiologist (full CODE) | The ECG + the clinical history sent with it (tele-ECG report) | Study labels from the reports (15% part: not stated) | Not documented |
| Chapman-Shaoxing, Ningbo | Physician, checked by a second physician; senior physician for disagreements | Not found | Challenge 2021 SNOMED mapping | Not documented |
| CPSC 2018, CPSC-Extra, Georgia | Not found | Not found | Challenge 2021 SNOMED mapping | Not found |
| INCART | Diagnoses: not found; beat marks: computer, corrected by people | Clinical work-up (per patient) | Patient diagnosis file | Not found |

Some classes are made differently within a dataset: CODE-15% `normal_ecg` is set by an automatic system, while its 6 other columns come from reports; PTB-XL's heart axis "was automatically extracted from the ECG report"; PTB-XL's likelihood is taken from report words, for diagnosis codes only; INCART's beat marks (computer, then corrected by people) are made differently from its patient diagnoses [PROV; ZEN-CODE15; WAGNER2020; README-INCART]. Apart from these named differences, no source describes a different method for individual label classes, so each class inherits its dataset's method [PROV].

### Per-class table

For each label class: how many there are, and which file step they come from. Who labelled them, on what basis and with what time gap is the same for all classes of a dataset, so see the pathways above. Only the exceptions are noted [LPROV].

The classes are the 21 from section 4b plus **Q wave** (a downward wave at the start of the QRS complex, the main spike of a heartbeat). Q wave is a **team mapping**: PTB-XL code `QWAVE` and Challenge code `164917005` [LPROV].

**PTB-XL** (our file: SCP codes converted from the report text). Count = ECGs. "Checked by a person" = `validated_by_human`; "Machine first report" = `initial_autogenerated_report` [LPROV].

| Class | Source code(s) | ECGs | Checked by a person | Machine first report |
|---|---|---|---|---|
| Normal ECG | `NORM` | 9,514 | 7,836 | 2,173 |
| Sinus rhythm | `SR` | 16,748 | 12,456 | 5,118 |
| Sinus bradycardia | `SBRAD` | 637 | 506 | 157 |
| Sinus tachycardia | `STACH` | 826 | 685 | 203 |
| Atrial fibrillation | `AFIB` | 1,514 | 994 | 579 |
| Atrial flutter | `AFLT` | 73 | 54 | 20 |
| 1st-degree AV block | `1AVB` | 793 | 562 | 271 |
| LBBB | `CLBBB` | 536 | 292 | 271 |
| RBBB (complete) | `CRBBB` | 541 | 375 | 196 |
| RBBB (incomplete) | `IRBBB` | 1,118 | 906 | 252 |
| LAFB | `LAFB` | 1,623 | 1,249 | 466 |
| PAC (atrial premature) | `PAC` | 398 | 394 | 5 |
| PVC (ventricular premature) | `PVC` | 1,143 | 751 | 430 |
| LVH | `LVH` | 2,132 | 1,441 | 752 |
| Long QT | `LNGQT` | 117 | 73 | 49 |
| MI (any) | `IMI+ASMI+ILMI+AMI+ALMI+INJAS+LMI+INJAL+IPLMI+IPMI+INJIN+INJLA+PMI+INJIL` | 5,469 | 3,477 | 2,281 |
| ST elevation | `STE_` | 28 | 28 | 0 |
| ST depression | `STD_` | 1,009 | 1,009 | 0 |
| Ischaemia (any) | `ISC_+ISCAL+ISCIN+ISCIL+ISCAS+ISCLA+ISCAN` | 2,467 | 1,590 | 975 |
| T-wave abnormality | `TAB_` | 35 | 35 | 0 |
| Q wave | `QWAVE` | 548 | 548 | 0 |

**SPH** (our file: AHA codes after translation)

| Class | Source code(s) | ECGs |
|---|---|---|
| Normal ECG | `1` | 13,905 |
| Sinus bradycardia | `22` | 2,711 |
| Sinus tachycardia | `21` | 725 |
| Atrial fibrillation | `50` | 675 |
| Atrial flutter | `51` | 99 |
| LBBB | `104` | 84 |
| RBBB (complete) | `106` | 710 |
| RBBB (incomplete) | `105` | 1,259 |
| LAFB | `101` | 154 |
| PAC (atrial premature) | `30` | 539 |
| PVC (ventricular premature) | `60` | 1,067 |
| LVH | `142` | 209 |
| Long QT | `148` | 24 |
| MI (any) | `160+161+165+166` | 260 |
| Old MI | `160+332+161+332+165+332+166+332` | 233 |
| ST elevation | `145+363` | 37 |
| ST depression | `145+362` | 1,024 |
| T-wave abnormality | `147` | 2,218 |

**PTB Diagnostic** (our file: header clinical summary)

| Class | Source code(s) | Records |
|---|---|---|
| MI (any) | `Reason for admission in Myocardial infarction` | 368 |
| Old MI | `Former infarction (localization) not_in no/n/a/unknown/<key missing in header>` | 85 |

**CODE-15%** (our file: study labels in `exams.csv`). Count = exams. Exception: `normal_ecg` is set by an automatic system; the other columns come from the report-based method [LPROV].

| Class | Source column | Exams | Made by |
|---|---|---|---|
| Normal ECG | `normal_ecg` | 134,657 | automatic system |
| Sinus bradycardia | `SB` | 5,605 | report-based method (full CODE) |
| Sinus tachycardia | `ST` | 7,584 | report-based method (full CODE) |
| Atrial fibrillation | `AF` | 7,033 | report-based method (full CODE) |
| 1st-degree AV block | `1dAVb` | 5,716 | report-based method (full CODE) |
| LBBB | `LBBB` | 6,026 | report-based method (full CODE) |
| RBBB (complete) | `RBBB` | 9,672 | report-based method (full CODE) |

**INCART** (count = records). Exception: some classes come from the **record descriptions** (author not found), others from the **patient diagnoses** (made after a clinical work-up; who made them: not found) [LPROV].

| Class | Source text | Records | Our file |
|---|---|---|---|
| Atrial fibrillation | rec: atrial fibrillation | 2 | record descriptions |
| RBBB (complete) | rec: right bundle branch block | 2 | record descriptions |
| PAC (atrial premature) | rec: APCs | 3 | record descriptions |
| PVC (ventricular premature) | rec_contains: PVC | 50 | record descriptions |
| LVH | dx_term: left ventricular hypertrophy | 11 | patient diagnoses |
| MI (any) | dx: Acute MI \| dx: Earlier MI | 15 | patient diagnoses |
| Old MI | dx: Earlier MI | 9 | patient diagnoses |
| ST elevation | rec: ST elevation | 4 | record descriptions |
| ST depression | rec: ST depression | 4 | record descriptions |

**The five Challenge datasets** (our file: the 2021 Challenge SNOMED mapping). Count = publisher's count as listed; sums of several codes may count one recording twice [LPROV].

| Class | SNOMED code(s) | CPSC | CPSC-Ex | Georgia | Ningbo | Chapman |
|---|---|---|---|---|---|---|
| Sinus rhythm | `426783006` | 918 | 4 | 1,752 | 6,299 | 1,826 |
| Sinus bradycardia | `426177001` | 0 (listed, count 0) | 45 | 1,677 | 12,670 | 3,889 |
| Sinus tachycardia | `427084000` | 0 (listed, count 0) | 303 | 1,261 | 5,687 | 1,568 |
| Atrial fibrillation | `164889003` | 1,221 | 153 | 570 | 0 (listed, count 0) | 1,780 |
| Atrial flutter | `164890007` | 0 (listed, count 0) | 54 | 186 | 7,615 | 445 |
| 1st-degree AV block | `270492004` | 722 | 106 | 769 | 893 | 247 |
| LBBB | `164909002+733534002` | 236 | 38 | 231 | 248 | 205 |
| RBBB (complete) | `59118001+713427006` | 1,857 | 114 | 570 | 1,291 | 454 |
| RBBB (incomplete) | `713426002` | 0 (listed, count 0) | 86 | 407 | 246 | 0 (listed, count 0) |
| LAFB | `445118002` | 0 (listed, count 0) | 0 (listed, count 0) | 180 | 380 | 0 (listed, count 0) |
| PAC (atrial premature) | `284470004+63593006` | 616 | 126 | 640 | 1,063 | 258 |
| PVC (ventricular premature) | `427172004+17338001` | 0 (listed, count 0) | 196 | 357 | 1,091 | 294 |
| LVH | `164873001` | 0 (listed, count 0) | 158 | 1,232 | 632 | 15 |
| Long QT | `111975006` | 0 (listed, count 0) | 4 | 1,391 | 337 | 57 |
| MI (any) | `164865005+57054005+54329005+164867002` | 0 (listed, count 0) | 1,606 | 7 | 189 | 40 |
| Old MI | `164867002` | 0 (listed, count 0) | 1,168 | 0 (listed, count 0) | 0 (listed, count 0) | 0 (listed, count 0) |
| ST elevation | `164931005` | 220 | 66 | 134 | 0 (listed, count 0) | 176 |
| ST depression | `429622005+704997005` | 869 | 58 | 38 | 1,266 | 402 |
| Ischaemia (any) | `164861001+413444003+413844008+426434006+425419005+425623009` | 0 (listed, count 0) | 546 | 1,636 | 0 (listed, count 0) | 0 (listed, count 0) |
| T-wave abnormality | `164934002` | 0 (listed, count 0) | 22 | 2,306 | 5,167 | 1,876 |
| Q wave | `164917005` | 0 (listed, count 0) | 1 | 464 | 828 | 235 |

**MIMIC-IV-ECG** (our file: none opened). The ICD code groups are the team's assumption (marked ASSUMPTION) and need the supervisor's sign-off (section 9) [LPROV].

| Class (as named in our results table) | Source | Count |
|---|---|---|
| STEMI (I21.0–I21.3; ASSUMPTION) | `I21.0–I21.3` | pending user-run count (credentialed) |
| NSTEMI (I21.4; ASSUMPTION) | `I21.4` | pending user-run count (credentialed) |
| unspecified/other MI (I21.9, I21.A*; ASSUMPTION) | `I21.9, I21.A*` | pending user-run count (credentialed) |
| subsequent MI (I22*; ASSUMPTION) | `I22*` | pending user-run count (credentialed) |
| old MI (I25.2; ASSUMPTION) | `I25.2` | pending user-run count (credentialed) |
| any I21/I22 (I21*, I22*; ASSUMPTION) | `I21*, I22*` | pending user-run count (credentialed) |
| machine report statements (all classes) | `report_0..report_17` | not checked |

## 4d. Label coding systems

Each dataset writes its labels in a "coding system": a fixed list of codes. Different systems can give different names to the same thing. This matters most for heart attacks, because the codes that say "STEMI" or "NSTEMI" differ between countries.

### Which system each dataset uses

| Dataset | Label system | Standard / version |
|---|---|---|
| PTB-XL | SCP-ECG statements | "Conforming to the SCP-ECG standard", Standard ISO 11073-91064:2009. The paper also mentions older "SCP-ECG v0.4 (Annex B)" statements. The label table also gives AHA, aECG, CDISC and DICOM columns [WAGNER2020; S14A] |
| SPH | AHA standard statements | The AHA/ACC/HRS recommendations: Mason, Hancock, Gettes, Circulation 2007;115:1325–1332, doi:10.1161/CIRCULATIONAHA.106.180201 (part number: not given) [LIU2022; S14A] |
| CPSC 2018, CPSC-Extra, Georgia, Ningbo, Chapman-Shaoxing | SNOMED CT | "Approximate SNOMED CT codes" mapped from the original labels. Which SNOMED CT release: **not found** [PN-CHALLENGE2021; PA2020; S14A] |
| CODE-15% | Yes/no columns | Full CODE labels came from the Uni-G program, Minnesota codes and cardiologist reports. Versions of Uni-G and Minnesota code: **not found** [RIBEIRO2020; S14A] |
| PTB Diagnostic | Free text (clinical summary) | No code system [S14A] |
| INCART | Free-text diagnoses + beat marks | Beat marks follow "the standard PhysioBank beat annotation definitions" [README-INCART; S14A] |
| MIMIC-IV-ECG (open files) | Machine-written free text | No code system [S14A] |
| MIMIC-IV-ECG-Ext-ICD (credentialed) | ICD-10-CM (the US version of ICD-10) | Older ICD-9-CM codes were converted with the Python package "icd-mappings". ICD-10-CM release year: **not stated** on the page [PN-MIMICECG-ICD; S14A] |

### Heart-attack codes in three versions of ICD-10

ICD-10 is the international list of disease codes. It exists in several versions:

- **WHO ICD-10** (the international version, 2019 edition) [WHO-ICD10-2019];
- **ICD-10-CM** (the US version, used by MIMIC). Code titles are from the US National Library of Medicine code list, which does not state its edition year. The rules are confirmed by the official FY 2025 coding guidelines [NLM-CM-API; CMS-CM-FY2025];
- **ICD-10-TM** (the Thai version, 2016 edition, Volume 1) [THCC-TM-2016].

"Transmural" means the damage goes through the whole heart wall. "Subendocardial" means only the inner layer is damaged.

| Code | WHO ICD-10 (2019) | ICD-10-CM (US) | ICD-10-TM (Thailand, 2016) |
|---|---|---|---|
| I21.0 | Acute transmural MI of anterior wall | Group only (see I21.01–I21.09); used for type 1 STEMI | Acute transmural MI of anterior wall (as WHO) |
| I21.01 | does not exist | STEMI involving left main coronary artery | does not exist |
| I21.02 | does not exist | STEMI involving left anterior descending coronary artery | does not exist |
| I21.09 | does not exist | STEMI involving other coronary artery of anterior wall | does not exist |
| I21.1 | Acute transmural MI of inferior wall | Group only (see I21.11–I21.19); used for type 1 STEMI | Acute transmural MI of inferior wall (as WHO) |
| I21.11 | does not exist | STEMI involving right coronary artery | does not exist |
| I21.19 | does not exist | STEMI involving other coronary artery of inferior wall | does not exist |
| I21.2 | Acute transmural MI of other sites | Group only (see I21.21–I21.29); used for type 1 STEMI | Acute transmural MI of other sites (as WHO) |
| I21.21 | does not exist | STEMI involving left circumflex coronary artery | does not exist |
| I21.29 | does not exist | STEMI involving other sites | does not exist |
| I21.3 | Acute transmural MI of unspecified site | "ST elevation (STEMI) myocardial infarction of unspecified site" | Acute transmural MI of unspecified site (as WHO) |
| I21.4 | "Acute subendocardial myocardial infarction". Includes "Myocardial infarction with non-ST elevation" | "Non-ST elevation (NSTEMI) myocardial infarction" (type 1 NSTEMI and nontransmural MI) | "Acute subendocardial myocardial infarction". Includes "Myocardial infarction with non-ST elevation" |
| I21.9 | "Acute myocardial infarction, unspecified" | The default for an unspecified acute MI or unspecified type | "Acute myocardial infarction, unspecified" |
| I21.A1 | does not exist | "Myocardial infarction type 2" | does not exist |
| I21.A9 | does not exist | "Other myocardial infarction type" (types 3, 4a, 4b, 4c, 5) | does not exist |
| I21.B | does not exist | "Myocardial infarction with coronary microvascular dysfunction" | does not exist |
| I22.0 | Subsequent MI, anterior wall | Subsequent STEMI, anterior wall | Subsequent myocardial infarction of anterior wall |
| I22.1 | Subsequent MI, inferior wall | Subsequent STEMI, inferior wall | Subsequent myocardial infarction of inferior wall |
| I22.2 | does not exist | "Subsequent non-ST elevation (NSTEMI) myocardial infarction" | does not exist |
| I22.8 | Subsequent MI, other sites | Subsequent STEMI, other sites | Subsequent myocardial infarction of other sites |
| I22.9 | Subsequent MI, unspecified site | Subsequent STEMI, unspecified site | Subsequent myocardial infarction of unspecified site |
| I25.2 | "Old myocardial infarction" (healed, or past MI with no symptoms now) | "Old myocardial infarction" | "Old myocardial infarction" (same inclusion terms as WHO) |
| **4-week rule** | I21 = MI "specified as acute or with a stated duration of 4 weeks (28 days) or less from onset". For hospital data, this means the time from onset to admission | I21 is used while the MI is "equal to, or less than, four weeks old"; old or healed MI not needing care → I25.2 | Same inclusion text as WHO |

DNE = does not exist in that version [WHO-ICD10-2019; NLM-CM-API; CMS-CM-FY2025; THCC-TM-2016; S14C].

Notes:

- **The word "STEMI" is not in the WHO or Thai titles.** They say "transmural" and "subendocardial". Only the US version says "STEMI" and "NSTEMI" [WHO-ICD10-2019; THCC-TM-2016; NLM-CM-API].
- **US rules that the other versions do not have** (CM guideline only):
  - A type 2 MI that is described as STEMI or NSTEMI gets **only** I21.A1. I21.01–I21.4 are for type 1 MI only.
  - An NSTEMI that becomes a STEMI is coded STEMI. A STEMI that turns into an NSTEMI after clot-dissolving treatment is still coded STEMI.
  - I22 is used only when both heart attacks are type 1 or unspecified, within 4 weeks [CMS-CM-FY2025].
- **Thai version:** for I21, I22 and I25.2, the 2016 edition has the same structure as WHO. We searched the whole of Volume 1: there are no I21.A, I21.B, 5-character I21 or I22 codes and no I22.2, and the words "STEMI" and "NSTEMI" do not occur [THCC-TM-2016]. The Thai coding guidelines (Volume 5), which say how coders should use these codes for MI: **not checked**.
- The year each US-only code was introduced: **not checked** [S14C].

### What this means when combining MIMIC with Thai hospital data

- The Thai codes follow the WHO structure (for I21, I22 and I25.2 in the 2016 edition). The US codes used by MIMIC are more detailed [THCC-TM-2016; S14C].
- In the US version, I21.0–I21.3 are called STEMI and I21.4 is called NSTEMI. In the WHO and Thai versions the same codes are called "transmural" and "subendocardial", although Thai and WHO I21.4 includes "MI with non-ST elevation" [S14C].
- The US-only codes (I21.01–I21.29, I21.A1, I21.A9, I21.B, I22.2) have no Thai equivalent [S14C].
- In the US, a type 2 MI described as STEMI or NSTEMI goes to I21.A1, not to I21.0–I21.4 [CMS-CM-FY2025].

*Planner's note:* so a mapping between MIMIC (US codes, with old ICD-9 codes converted) and Thai hospital data (Thai codes) is **not one to one**. US I21.A1, I21.A9 and I21.B have no Thai equivalent. The Thai "transmural" vs "subendocardial" titles only approximate STEMI vs NSTEMI. The supervisor must agree this mapping before any combined labels are used (section 9) [S14C].

## 5. Each dataset in detail

Each part answers the same 10 questions. Each answer gives its source.

### 5.1 PTB-XL

**In one line:** a large, open set of 10-second clinical 12-lead ECGs. Its report codes come from cardiologists or from the ECG machine, and people checked most of the records. It has "MI" report statements, but nothing that says STEMI or NSTEMI.

1. **Labels.** Each ECG has codes from a standard list called SCP-ECG (a standard set of codes for ECG report statements). There are 71 codes. They describe the diagnosis, the shape of the wave, and the heart rhythm [PN-PTBXL]. Each code comes with a "likelihood" from 0 to 100 [OBS-PTBXL]. This number shows how sure **the wording of the report** sounds. It does not show how sure a doctor was. It was taken from key words in the report: for example "cannot rule out" = 15, "possible" = 50, "consistent with" = 100 [WAGNER2020, Table 4]. Only diagnosis codes have a likelihood. Shape and rhythm codes are set to 0, and so are diagnosis codes whose report gives no certainty word [WAGNER2020, Table 4]. Careful: the German words "Zustand nach" ("status post", meaning a past event) also give 100. **So likelihood 100 does not mean a new heart attack** [WAGNER2020, Table 4]. The codes fall into groups. One group is "MI" (14 codes). Other groups are ST/T changes (13 codes), conduction problems (11), enlarged heart (5), normal (1), and codes with no group (27) [OBS-PTBXL]. There is also an "infarct stage" field (whether a heart attack looks new or old). It is empty for 16,187 of the 21,799 ECGs. It is filled in mainly for ECGs with MI statements, and every ECG with an MI code has a value [OBS-PTBXL]. Other fields give the heart's electrical direction and a free-text report [OBS-PTBXL]. Every ECG has at least one code [OBS-PTBXL].
2. **Who labelled them.** "Up to two cardiologists" (heart doctors) [PN-PTBXL]. The first report was written by a cardiologist for 67.13% of ECGs. For 31.2%, the ECG machine wrote it automatically (figures from the first release) [WAGNER2020]. The second check was not independent. The second person checked the first person's work [WAGNER2020]. In release 1.0.3, the files mark 16,056 ECGs (73.65%) as checked by a person. The authors call this a cautious (low) estimate [WAGNER2020; OBS-PTBXL]. 6,813 ECGs (31.25%) are marked as having a machine-written first report. 555 (2.55%) had a second opinion [OBS-PTBXL].
3. **Collection.** The ECGs come from PTB (Physikalisch-Technische Bundesanstalt). They were recorded with Schiller AG machines between October 1989 and June 1996 [PN-PTBXL; WAGNER2020]. The country is not stated on the dataset page [PN-PTBXL]. The page calls them "clinical 12-lead ECGs" [PN-PTBXL]. Release 1.0.3 has 21,799 ECGs from 18,869 patients. 2,111 patients have more than one ECG (at most 10) [OBS-PTBXL]. 11,354 ECGs are from men and 10,445 from women. Age is shown as "300" for people aged 90 or older (293 ECGs) [OBS-PTBXL; WAGNER2020]. **Do not use the recording dates to find years.** The dates were moved by a random amount for each patient, and the stored years run from 1984 to 2001 [WAGNER2020; OBS-PTBXL].
4. **Setting.** **Not found.** We looked at the dataset page and the paper. They only say that the recording site ("hospital etc.") was hidden ("pseudonymised") [PN-PTBXL; WAGNER2020]. The file has 51 different site numbers [OBS-PTBXL]. Nothing says ambulance, emergency room, ward or clinic.
5. **Device.** Schiller AG machines, 11 device types [WAGNER2020]. The most common device names are "CS100 3" (6,140 ECGs), "CS-12" (4,048) and "AT-6 C 5.5" (3,950) [OBS-PTBXL]. The ECGs were first recorded at 400 Hz (400 measurements per second) [WAGNER2020]. They are shared at 500 Hz and also at 100 Hz. The 100 Hz files are the same ECGs, not extra ones [PN-PTBXL]. 12 leads (12 views of the heart), 10 seconds [PN-PTBXL]. We opened 20 header files as a sample. All 20 had the lead order I, II, III, AVR, AVL, AVF, V1–V6, 500 Hz, 5,000 samples, and units in millivolts. This is a small sample and may not hold for every file [OBS-PTBXL].
6. **STEMI vs NSTEMI.** **No.** No code says STEMI or NSTEMI [OBS-PTBXL]. There are 14 "MI" report statements. Five of them are "subendocardial injury" codes (damage to the inner layer of the heart wall) [OBS-PTBXL]. 5,469 ECGs from 4,670 patients have at least one of them. For 2,975 ECGs, the report wording gave likelihood 100 [OBS-PTBXL]. This can include "status post" (a past event), so it does not mean a new heart attack [WAGNER2020, Table 4]. Counts per code: IMI 2,676; ASMI 2,357; ILMI 478; AMI 353; ALMI 288; INJAS 214; LMI 201; INJAL 145; IPLMI 51; IPMI 33; INJIN 18; INJLA 17; PMI 17; INJIL 15 [OBS-PTBXL]. The infarct stage helps a little. Stage I means "acute, early" and Stage III means "old" [WAGNER2020]. 150 MI-coded ECGs (128 patients) are at Stage I or I–II. 3,372 MI-coded ECGs have stage "unknown" [OBS-PTBXL]. The 150 ECGs are **a list for clinical review**, not acute-MI labels. 28 ECGs have a general "ST elevation" code and 1,009 have "ST depression". These two codes describe the wave shape only (PTB-XL calls them "form" statements). They have no diagnostic group, and they are not in the MI group [OBS-PTBXL]. All of these are statements in an ECG report. They are not a confirmed diagnosis of a heart attack (`data_contract.md` L2, L3). **So PTB-XL gives "MI statement or not" only, not STEMI vs NSTEMI.**
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
  - **Atrial flutter vs fibrillation in Ningbo:** 0 atrial fibrillation but 7,615 atrial flutter, in the publisher's file and in our sample. In the original label list, "AF" means atrial flutter and "AFIB" means atrial fibrillation [AFCHK]. *Planner's note:* Ningbo's pattern (no atrial fibrillation, many atrial flutter) is unusual and may reflect how the source labelled rhythms; a model could learn a dataset-specific labelling habit. A clinician should review this before Ningbo rhythm labels are used.
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
- **Which diagnosis codes mean STEMI, and which mean NSTEMI?** The supervisor must sign off this list before any count is used as a label. The team's proposed groups are listed in section 4c (I21.0–I21.3 as STEMI, I21.4 as NSTEMI, marked ASSUMPTION).
- **Agree a WHO/TM ↔ CM mapping for MI codes (section 4d).** This is needed before MIMIC labels (US codes) are combined with Thai hospital data (Thai codes).
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

## Appendix B. Full label list for each dataset

One table per dataset, sorted from the highest count down. Labels are shown exactly as the publisher wrote them. The rules from section 4b apply: "not present" and "not checked" mean different things, and Challenge counts are the publisher's count as listed [INV].

### B.1 PTB-XL

All 71 SCP-ECG statements. Count = ECGs with the code at any likelihood. Class = the diagnostic class in `scp_statements.csv` (blank for shape and rhythm codes) [INV].

| Label as written | Code | Kind | Class | ECGs |
|---|---|---|---|---|
| sinus rhythm | `SR` | rhythm |  | 16,748 |
| normal ECG | `NORM` | diagnostic | NORM | 9,514 |
| abnormal QRS | `ABQRS` | form |  | 3,327 |
| inferior myocardial infarction | `IMI` | diagnostic | MI | 2,676 |
| anteroseptal myocardial infarction | `ASMI` | diagnostic | MI | 2,357 |
| left ventricular hypertrophy | `LVH` | diagnostic | HYP | 2,132 |
| non-diagnostic T abnormalities | `NDT` | diagnostic/form | STTC | 1,825 |
| left anterior fascicular block | `LAFB` | diagnostic | CD | 1,623 |
| atrial fibrillation | `AFIB` | rhythm |  | 1,514 |
| non-specific ischemic | `ISC_` | diagnostic | STTC | 1,272 |
| ventricular premature complex | `PVC` | form |  | 1,143 |
| incomplete right bundle branch block | `IRBBB` | diagnostic | CD | 1,118 |
| non-specific ST depression | `STD_` | form |  | 1,009 |
| voltage criteria (QRS) for left ventricular hypertrophy | `VCLVH` | form |  | 875 |
| sinus tachycardia | `STACH` | rhythm |  | 826 |
| first degree AV block | `1AVB` | diagnostic | CD | 793 |
| non-specific intraventricular conduction disturbance (block) | `IVCD` | diagnostic | CD | 787 |
| sinus arrhythmia | `SARRH` | rhythm |  | 772 |
| non-specific ST changes | `NST_` | diagnostic/form | STTC | 767 |
| ischemic in anterolateral leads | `ISCAL` | diagnostic | STTC | 659 |
| sinus bradycardia | `SBRAD` | rhythm |  | 637 |
| Q waves present | `QWAVE` | form |  | 548 |
| complete right bundle branch block | `CRBBB` | diagnostic | CD | 541 |
| complete left bundle branch block | `CLBBB` | diagnostic | CD | 536 |
| inferolateral myocardial infarction | `ILMI` | diagnostic | MI | 478 |
| low amplitude T-waves | `LOWT` | form |  | 438 |
| left atrial overload/enlargement | `LAO/LAE` | diagnostic | HYP | 426 |
| non-specific T-wave changes | `NT_` | form |  | 423 |
| atrial premature complex | `PAC` | form |  | 398 |
| anterior myocardial infarction | `AMI` | diagnostic | MI | 353 |
| prolonged PR interval | `LPR` | form |  | 340 |
| inverted T-waves | `INVT` | form |  | 294 |
| normal functioning artificial pacemaker | `PACE` | rhythm |  | 294 |
| anterolateral myocardial infarction | `ALMI` | diagnostic | MI | 288 |
| ischemic in inferior leads | `ISCIN` | diagnostic | STTC | 218 |
| subendocardial injury in anteroseptal leads | `INJAS` | diagnostic | MI | 214 |
| lateral myocardial infarction | `LMI` | diagnostic | MI | 201 |
| low QRS voltages in the frontal and horizontal leads | `LVOLT` | form |  | 182 |
| digitalis-effect | `DIG` | diagnostic/form | STTC | 181 |
| ischemic in inferolateral leads | `ISCIL` | diagnostic | STTC | 179 |
| left posterior fascicular block | `LPFB` | diagnostic | CD | 177 |
| ischemic in anteroseptal leads | `ISCAS` | diagnostic | STTC | 169 |
| supraventricular arrhythmia | `SVARR` | rhythm |  | 157 |
| subendocardial injury in anterolateral leads | `INJAL` | diagnostic | MI | 145 |
| ischemic in lateral leads | `ISCLA` | diagnostic | STTC | 140 |
| right ventricular hypertrophy | `RVH` | diagnostic | HYP | 126 |
| long QT-interval | `LNGQT` | diagnostic/form | STTC | 117 |
| ST-T changes compatible with ventricular aneurysm | `ANEUR` | diagnostic | STTC | 104 |
| right atrial overload/enlargement | `RAO/RAE` | diagnostic | HYP | 99 |
| electrolytic disturbance or drug (former EDIS) | `EL` | diagnostic | STTC | 96 |
| bigeminal pattern (unknown origin, SV or Ventricular) | `BIGU` | rhythm |  | 82 |
| Wolf-Parkinson-White syndrome | `WPW` | diagnostic | CD | 79 |
| incomplete left bundle branch block | `ILBBB` | diagnostic | CD | 77 |
| atrial flutter | `AFLT` | rhythm |  | 73 |
| high QRS voltage | `HVOLT` | form |  | 62 |
| inferoposterolateral myocardial infarction | `IPLMI` | diagnostic | MI | 51 |
| ischemic in anterior leads | `ISCAN` | diagnostic | STTC | 44 |
| T-wave abnormality | `TAB_` | form |  | 35 |
| inferoposterior myocardial infarction | `IPMI` | diagnostic | MI | 33 |
| septal hypertrophy | `SEHYP` | diagnostic | HYP | 29 |
| non-specific ST elevation | `STE_` | form |  | 28 |
| supraventricular tachycardia | `SVTAC` | rhythm |  | 27 |
| paroxysmal supraventricular tachycardia | `PSVT` | rhythm |  | 24 |
| trigeminal pattern (unknown origin, SV or Ventricular) | `TRIGU` | rhythm |  | 20 |
| subendocardial injury in inferior leads | `INJIN` | diagnostic | MI | 18 |
| posterior myocardial infarction | `PMI` | diagnostic | MI | 17 |
| subendocardial injury in lateral leads | `INJLA` | diagnostic | MI | 17 |
| third degree AV block | `3AVB` | diagnostic | CD | 16 |
| subendocardial injury in inferolateral leads | `INJIL` | diagnostic | MI | 15 |
| second degree AV block | `2AVB` | diagnostic | CD | 14 |
| premature complex(es) | `PRC(S)` | form |  | 10 |

### B.2 MIMIC-IV-ECG

Not checked: label file not downloaded. The machine report file was not approved for download, and the diagnosis codes need credentialed access [INV].

### B.3 PTB Diagnostic

Free text from the header comments, exactly as written (spelling kept). Count = records; patients in the last column [INV].

**Reason for admission**

| Text as written | Records | Patients |
|---|---|---|
| Myocardial infarction | 368 | 148 |
| Healthy control | 80 | 52 |
| n/a | 27 | 22 |
| Bundle branch block | 17 | 15 |
| Cardiomyopathy | 17 | 15 |
| Dysrhythmia | 16 | 14 |
| Hypertrophy | 7 | 7 |
| Valvular heart disease | 6 | 6 |
| Myocarditis | 4 | 4 |
| Stable angina | 2 | 2 |
| Heart failure (NYHA 2) | 1 | 1 |
| Heart failure (NYHA 3) | 1 | 1 |
| Heart failure (NYHA 4) | 1 | 1 |
| Palpitation | 1 | 1 |
| Unstable angina | 1 | 1 |

**Acute infarction (localization)**

| Text as written | Records | Patients |
|---|---|---|
| no | 175 | 140 |
| inferior | 89 | 30 |
| antero-septal | 77 | 27 |
| infero-lateral | 53 | 22 |
| anterior | 47 | 17 |
| antero-lateral | 43 | 16 |
| n/a | 27 | 22 |
| infero-postero-lateral | 16 | 7 |
| postero-lateral | 5 | 2 |
| posterior | 4 | 1 |
| infero-latera | 3 | 1 |
| infero-poster-lateral | 3 | 1 |
| lateral | 3 | 1 |
| antero-septo-lateral | 2 | 1 |
| infero-posterior | 1 | 1 |
| unknown | 1 | 1 |

**Former infarction (localization)**

| Text as written | Records | Patients |
|---|---|---|
| no | 423 | 209 |
| anterior | 27 | 14 |
| n/a | 27 | 22 |
| inferior | 23 | 13 |
| unknown | 14 | 13 |
| antero-lateral | 6 | 3 |
| infero-posterior | 5 | 3 |
| antero-septal | 4 | 1 |
| infero-lateral | 4 | 2 |
| postero-lateral | 4 | 1 |
| inferior ? | 3 | 1 |
| anterior (1), inferior (2) | 2 | 2 |
| inferior (1+2) | 2 | 1 |
| anterior (1), anterior (2) | 1 | 1 |
| anterior ? | 1 | 1 |
| antero-septal ? | 1 | 1 |
| infero-posterior (1), inferior (2) | 1 | 1 |
| infero-postero-lateral | 1 | 1 |


### B.4 SPH

AHA statement codes. Count = ECG records; patients in the last column [INV].

**Main codes (44)**

| Label as written | Code | ECGs | Patients |
|---|---|---|---|
| Normal ECG | `1` | 13,905 | 13,498 |
| Sinus bradycardia | `22` | 2,711 | 2,640 |
| T-wave abnormality | `147` | 2,218 | 2,155 |
| ST deviation | `145` | 1,829 | 1,783 |
| Sinus arrhythmia | `23` | 1,553 | 1,527 |
| Incomplete right bundle-branch block | `105` | 1,259 | 1,238 |
| Ventricular premature complex(es) | `60` | 1,067 | 1,032 |
| ST deviation with T-wave change | `146` | 1,063 | 1,042 |
| Sinus tachycardia | `21` | 725 | 705 |
| Right bundle-branch block | `106` | 710 | 658 |
| Atrial fibrillation | `50` | 675 | 634 |
| Atrial premature complex(es) | `30` | 539 | 525 |
| Low voltage | `125` | 322 | 307 |
| Prolonged PR interval | `82` | 238 | 233 |
| Left ventricular hypertrophy | `142` | 209 | 201 |
| Right-axis deviation | `120` | 161 | 158 |
| Left anterior fascicular block | `101` | 154 | 149 |
| Left-axis deviation | `121` | 138 | 136 |
| Inferior MI | `161` | 120 | 117 |
| Atrial flutter | `51` | 99 | 88 |
| Anteroseptal MI | `165` | 91 | 82 |
| ST-T change due to ventricular hypertrophy | `153` | 88 | 86 |
| Left bundle-branch block | `104` | 84 | 79 |
| Junctional premature complex(es) | `36` | 64 | 63 |
| Anterior MI | `160` | 52 | 47 |
| AV block, varying conduction | `86` | 47 | 47 |
| 2:1 AV block | `85` | 35 | 32 |
| Early repolarization | `155` | 32 | 32 |
| Ventricular preexcitation | `108` | 27 | 27 |
| Prolonged QT interval | `148` | 24 | 23 |
| AV block, complete (third-degree) | `88` | 22 | 20 |
| Junctional escape complex(es) | `37` | 20 | 19 |
| Left atrial enlargement | `140` | 19 | 19 |
| Junctional tachycardia | `54` | 13 | 13 |
| Short PR interval | `80` | 11 | 11 |
| Second-degree AV block, Mobitz type I (Wenckebach) | `83` | 9 | 9 |
| TU fusion | `152` | 9 | 9 |
| Extensive anterior MI | `166` | 7 | 7 |
| Left posterior fascicular block | `102` | 6 | 6 |
| Right ventricular hypertrophy | `143` | 6 | 6 |
| Atrial premature complexes, nonconducted | `31` | 4 | 4 |
| AV block, advanced (high-grade) | `87` | 3 | 3 |
| AV conduction ratio N:D | `81` | 3 | 3 |
| Second-degree AV block, Mobitz type II | `84` | 3 | 3 |

**Main code + add-on code pairs (25)**

| Label as written | Code | ECGs | Patients |
|---|---|---|---|
| ST deviation + Depression | `145+362` | 1,024 | 1,012 |
| Ventricular premature complex(es) + Frequent | `60+310` | 277 | 271 |
| Ventricular premature complex(es) + Occasional | `60+308` | 271 | 266 |
| Atrial fibrillation + With a rapid ventricular response | `50+346` | 210 | 205 |
| T-wave abnormality + Inversion | `147+367` | 176 | 174 |
| Atrial premature complex(es) + Occasional | `30+308` | 153 | 148 |
| Atrial premature complex(es) + Frequent | `30+310` | 125 | 124 |
| Inferior MI + Old | `161+332` | 114 | 111 |
| Anteroseptal MI + Old | `165+332` | 75 | 70 |
| Ventricular premature complex(es) + In a bigeminal pattern | `60+341` | 70 | 68 |
| Anterior MI + Old | `160+332` | 47 | 42 |
| Ventricular premature complex(es) + In a trigeminal pattern | `60+342` | 38 | 37 |
| ST deviation + Elevation | `145+363` | 37 | 34 |
| Atrial premature complex(es) + In a bigeminal pattern | `30+341` | 31 | 31 |
| Atrial premature complex(es) + With aberrancy | `30+349` | 16 | 16 |
| Atrial premature complex(es) + Couplets | `30+340` | 11 | 11 |
| Anteroseptal MI + Recent | `165+331` | 9 | 6 |
| Extensive anterior MI + Old | `166+332` | 7 | 7 |
| Atrial fibrillation + With a slow ventricular response | `50+347` | 6 | 6 |
| Anteroseptal MI + Acute | `165+330` | 4 | 4 |
| Inferior MI + Recent | `161+331` | 3 | 3 |
| Ventricular premature complex(es) + Couplets | `60+340` | 3 | 3 |
| Ventricular premature complex(es) + Polymorphic | `60+350` | 3 | 3 |
| Inferior MI + Acute | `161+330` | 2 | 2 |
| Anterior MI + Acute | `160+330` | 1 | 1 |

### B.5 CPSC 2018

SNOMED CT codes from the Challenge label files. Count = publisher's count as listed (what it counts is not defined by the publisher). Only the 9 codes with a count above 0 are shown; 124 listed codes with count 0 are left out [INV; DXMAP].

| Label as written | SNOMED code | Publisher's count |
|---|---|---|
| right bundle branch block | `59118001` | 1,857 |
| atrial fibrillation | `164889003` | 1,221 |
| sinus rhythm | `426783006` | 918 |
| st depression | `429622005` | 869 |
| 1st degree av block | `270492004` | 722 |
| ventricular ectopics | `164884008` | 700 |
| premature atrial contraction | `284470004` | 616 |
| left bundle branch block | `164909002` | 236 |
| st elevation | `164931005` | 220 |

### B.6 CPSC-Extra

SNOMED CT codes from the Challenge label files. Count = publisher's count as listed (what it counts is not defined by the publisher). Only the 72 codes with a count above 0 are shown; 61 listed codes with count 0 are left out [INV; DXMAP].

| Label as written | SNOMED code | Publisher's count |
|---|---|---|
| nonspecific st t abnormality | `428750005` | 1,290 |
| old myocardial infarction | `164867002` | 1,168 |
| st interval abnormal | `164930006` | 481 |
| myocardial ischemia | `164861001` | 384 |
| myocardial infarction | `164865005` | 376 |
| sinus tachycardia | `427084000` | 303 |
| bradycardia | `426627000` | 271 |
| premature ventricular contractions | `427172004` | 188 |
| chronic myocardial ischemia | `413844008` | 161 |
| left ventricular hypertrophy | `164873001` | 158 |
| atrial fibrillation | `164889003` | 153 |
| complete right bundle branch block | `713427006` | 113 |
| 1st degree av block | `270492004` | 106 |
| incomplete right bundle branch block | `713426002` | 86 |
| premature atrial contraction | `284470004` | 73 |
| st elevation | `164931005` | 66 |
| anterior myocardial infarction | `54329005` | 62 |
| st depression | `429622005` | 57 |
| atrial flutter | `164890007` | 54 |
| supraventricular premature beats | `63593006` | 53 |
| sinus bradycardia | `426177001` | 45 |
| incomplete left bundle branch block | `251120003` | 42 |
| left atrial hypertrophy | `446813000` | 40 |
| atrial fibrillation and flutter | `195080001` | 39 |
| left bundle branch block | `164909002` | 38 |
| complete heart block | `27885002` | 27 |
| t wave abnormal | `164934002` | 22 |
| 2nd degree av block | `195042002` | 21 |
| right ventricular hypertrophy | `89792004` | 20 |
| right atrial hypertrophy | `446358003` | 18 |
| atrial tachycardia | `713422000` | 15 |
| sinus arrhythmia | `427393009` | 11 |
| ventricular fibrillation | `164896001` | 10 |
| sinoatrial block | `65778007` | 9 |
| ventricular premature beats | `17338001` | 8 |
| atrioventricular junctional rhythm | `29320008` | 6 |
| ventricular pre excitation | `195060002` | 6 |
| av block | `233917008` | 5 |
| t wave inversion | `59931005` | 5 |
| ventricular bigeminy | `11157007` | 5 |
| ventricular hypertrophy | `266249003` | 5 |
| junctional escape | `426995002` | 4 |
| nonspecific intraventricular conduction disorder | `698252002` | 4 |
| prolonged qt interval | `111975006` | 4 |
| sinus rhythm | `426783006` | 4 |
| ventricular trigeminy | `251180001` | 4 |
| pacing rhythm | `10370003` | 3 |
| shortened pr interval | `49578007` | 3 |
| supraventricular tachycardia | `426761007` | 3 |
| ventricular escape beat | `75532003` | 3 |
| atrial hypertrophy | `195126007` | 2 |
| blocked premature atrial contraction | `251170000` | 2 |
| junctional premature complex | `251164006` | 2 |
| junctional tachycardia | `426648003` | 2 |
| acute myocardial ischemia | `413444003` | 1 |
| brady tachy syndrome | `74615001` | 1 |
| chronic atrial fibrillation | `426749004` | 1 |
| decreased qt interval | `77867006` | 1 |
| diffuse intraventricular block | `82226007` | 1 |
| high t-voltage | `251259000` | 1 |
| inferior ST segment depression | `704997005` | 1 |
| left atrial enlargement | `67741000119109` | 1 |
| left ventricular strain | `370365005` | 1 |
| qwave abnormal | `164917005` | 1 |
| r wave abnormal | `164921003` | 1 |
| right axis deviation | `47665007` | 1 |
| right bundle branch block | `59118001` | 1 |
| s t changes | `55930002` | 1 |
| u wave abnormal | `164937009` | 1 |
| ventricular escape rhythm | `81898007` | 1 |
| ventricular flutter | `111288001` | 1 |
| ventricular tachycardia | `164895002` | 1 |

### B.7 Georgia

SNOMED CT codes from the Challenge label files. Count = publisher's count as listed (what it counts is not defined by the publisher). Only the 67 codes with a count above 0 are shown; 66 listed codes with count 0 are left out [INV; DXMAP].

| Label as written | SNOMED code | Publisher's count |
|---|---|---|
| t wave abnormal | `164934002` | 2,306 |
| nonspecific st t abnormality | `428750005` | 1,883 |
| sinus rhythm | `426783006` | 1,752 |
| sinus bradycardia | `426177001` | 1,677 |
| prolonged qt interval | `111975006` | 1,391 |
| sinus tachycardia | `427084000` | 1,261 |
| left ventricular hypertrophy | `164873001` | 1,232 |
| st interval abnormal | `164930006` | 992 |
| left axis deviation | `39732003` | 940 |
| lateral ischaemia | `425623009` | 903 |
| left atrial enlargement | `67741000119109` | 870 |
| t wave inversion | `59931005` | 812 |
| 1st degree av block | `270492004` | 769 |
| premature atrial contraction | `284470004` | 639 |
| atrial fibrillation | `164889003` | 570 |
| right bundle branch block | `59118001` | 542 |
| qwave abnormal | `164917005` | 464 |
| sinus arrhythmia | `427393009` | 455 |
| inferior ischaemia | `425419005` | 451 |
| incomplete right bundle branch block | `713426002` | 407 |
| low qrs voltages | `251146004` | 374 |
| ventricular premature beats | `17338001` | 357 |
| anterior ischemia | `426434006` | 281 |
| left bundle branch block | `164909002` | 231 |
| nonspecific intraventricular conduction disorder | `698252002` | 203 |
| atrial flutter | `164890007` | 186 |
| left anterior fascicular block | `445118002` | 180 |
| early repolarization | `428417006` | 140 |
| st elevation | `164931005` | 134 |
| bundle branch block | `6374002` | 116 |
| incomplete left bundle branch block | `251120003` | 86 |
| right ventricular hypertrophy | `89792004` | 86 |
| right axis deviation | `47665007` | 83 |
| av block | `233917008` | 74 |
| left atrial abnormality | `253352002` | 72 |
| ventricular hypertrophy | `266249003` | 71 |
| atrial hypertrophy | `195126007` | 60 |
| atrial pacing pattern | `251268003` | 52 |
| ventricular pacing pattern | `251266004` | 46 |
| ventricular ectopics | `164884008` | 41 |
| st depression | `429622005` | 38 |
| supraventricular tachycardia | `426761007` | 32 |
| atrial tachycardia | `713422000` | 28 |
| complete right bundle branch block | `713427006` | 28 |
| left posterior fascicular block | `445211001` | 25 |
| 2nd degree av block | `195042002` | 23 |
| accelerated junctional rhythm | `426664006` | 19 |
| right atrial abnormality | `253339007` | 14 |
| suspect arm ecg leads reversed | `251139008` | 12 |
| r wave abnormal | `164921003` | 10 |
| complete heart block | `27885002` | 8 |
| myocardial infarction | `164865005` | 7 |
| wandering atrial pacemaker | `195101003` | 7 |
| bradycardia | `426627000` | 6 |
| s t changes | `55930002` | 6 |
| junctional escape | `426995002` | 5 |
| junctional tachycardia | `426648003` | 4 |
| ventricular fibrillation | `164896001` | 3 |
| atrial fibrillation and flutter | `195080001` | 2 |
| shortened pr interval | `49578007` | 2 |
| ventricular bigeminy | `11157007` | 2 |
| ventricular pre excitation | `195060002` | 2 |
| wolff parkinson white pattern | `74390002` | 2 |
| acute myocardial ischemia | `413444003` | 1 |
| supraventricular premature beats | `63593006` | 1 |
| ventricular escape rhythm | `81898007` | 1 |
| ventricular trigeminy | `251180001` | 1 |

### B.8 Ningbo

SNOMED CT codes from the Challenge label files. Count = publisher's count as listed (what it counts is not defined by the publisher). Only the 80 codes with a count above 0 are shown; 53 listed codes with count 0 are left out [INV; DXMAP].

| Label as written | SNOMED code | Publisher's count |
|---|---|---|
| sinus bradycardia | `426177001` | 12,670 |
| atrial flutter | `164890007` | 7,615 |
| sinus rhythm | `426783006` | 6,299 |
| sinus tachycardia | `427084000` | 5,687 |
| t wave abnormal | `164934002` | 5,167 |
| s t changes | `55930002` | 4,232 |
| left ventricular high voltage | `55827005` | 4,106 |
| t wave inversion | `59931005` | 2,720 |
| sinus arrhythmia | `427393009` | 2,550 |
| st depression | `429622005` | 1,266 |
| pacing rhythm | `10370003` | 1,182 |
| left axis deviation | `39732003` | 1,163 |
| complete right bundle branch block | `713427006` | 1,096 |
| premature ventricular contractions | `427172004` | 1,091 |
| premature atrial contraction | `284470004` | 1,054 |
| 1st degree av block | `270492004` | 893 |
| qwave abnormal | `164917005` | 828 |
| st interval abnormal | `164930006` | 799 |
| low qrs voltages | `251146004` | 794 |
| clockwise or counterclockwise vectorcardiographic loop | `61721007` | 653 |
| poor R wave Progression | `365413008` | 638 |
| right axis deviation | `47665007` | 638 |
| left ventricular hypertrophy | `164873001` | 632 |
| nonspecific intraventricular conduction disorder | `698252002` | 536 |
| bundle branch block | `6374002` | 385 |
| left anterior fascicular block | `445118002` | 380 |
| early repolarization | `428417006` | 344 |
| prolonged qt interval | `111975006` | 337 |
| incomplete right bundle branch block | `713426002` | 246 |
| atrial rhythm | `106068003` | 215 |
| tall p wave | `251223006` | 215 |
| complete left bundle branch block | `733534002` | 213 |
| right bundle branch block | `59118001` | 195 |
| atrial tachycardia | `713422000` | 176 |
| atrioventricular junctional rhythm | `29320008` | 139 |
| supraventricular tachycardia | `426761007` | 137 |
| fusion beats | `13640000` | 114 |
| u wave abnormal | `164937009` | 114 |
| paroxysmal ventricular tachycardia | `425856008` | 109 |
| prolonged P wave | `251205003` | 106 |
| right ventricular hypertrophy | `89792004` | 106 |
| ventricular escape rhythm | `81898007` | 96 |
| myocardial infarction | `164865005` | 83 |
| av block | `233917008` | 78 |
| complete heart block | `27885002` | 75 |
| wolff parkinson white pattern | `74390002` | 68 |
| blocked premature atrial contraction | `251170000` | 62 |
| junctional escape | `426995002` | 60 |
| atrioventricular dissociation | `50799005` | 59 |
| ventricular fibrillation | `164896001` | 59 |
| 2nd degree av block | `195042002` | 58 |
| anterior myocardial infarction | `54329005` | 57 |
| acute myocardial infarction | `57054005` | 49 |
| ventricular escape beat | `75532003` | 49 |
| p wave change | `164912004` | 47 |
| prolonged pr interval | `164947007` | 40 |
| left bundle branch block | `164909002` | 35 |
| right atrial hypertrophy | `446358003` | 33 |
| sinus arrest | `5609005` | 33 |
| right atrial  high voltage | `67751000119106` | 28 |
| mobitz type i wenckebach atrioventricular block | `54016002` | 25 |
| junctional tachycardia | `426648003` | 24 |
| shortened pr interval | `49578007` | 23 |
| atrioventricular reentrant tachycardia | `233897008` | 18 |
| atrial escape beat | `251187003` | 17 |
| accelerated atrial escape rhythm | `233892002` | 16 |
| accelerated idioventricular rhythm | `61277005` | 14 |
| accelerated junctional rhythm | `426664006` | 12 |
| junctional premature complex | `251164006` | 10 |
| supraventricular premature beats | `63593006` | 9 |
| left atrial hypertrophy | `446813000` | 8 |
| bradycardia | `426627000` | 7 |
| mobitz type II atrioventricular block | `426183003` | 7 |
| ventricular flutter | `111288001` | 7 |
| incomplete left bundle branch block | `251120003` | 6 |
| brugada | `418818005` | 5 |
| left posterior fascicular block | `445211001` | 5 |
| sinoatrial block | `65778007` | 5 |
| decreased qt interval | `77867006` | 2 |
| left atrial enlargement | `67741000119109` | 1 |

### B.9 Chapman-Shaoxing

SNOMED CT codes from the Challenge label files. Count = publisher's count as listed (what it counts is not defined by the publisher). Only the 54 codes with a count above 0 are shown; 79 listed codes with count 0 are left out [INV; DXMAP].

| Label as written | SNOMED code | Publisher's count |
|---|---|---|
| sinus bradycardia | `426177001` | 3,889 |
| t wave abnormal | `164934002` | 1,876 |
| sinus rhythm | `426783006` | 1,826 |
| atrial fibrillation | `164889003` | 1,780 |
| sinus tachycardia | `427084000` | 1,568 |
| left ventricular high voltage | `55827005` | 1,295 |
| nonspecific st t abnormality | `428750005` | 1,158 |
| supraventricular tachycardia | `426761007` | 587 |
| right bundle branch block | `59118001` | 454 |
| atrial flutter | `164890007` | 445 |
| st depression | `429622005` | 402 |
| left axis deviation | `39732003` | 382 |
| ventricular premature beats | `17338001` | 294 |
| premature atrial contraction | `284470004` | 258 |
| low qrs voltages | `251146004` | 249 |
| 1st degree av block | `270492004` | 247 |
| nonspecific intraventricular conduction disorder | `698252002` | 235 |
| qwave abnormal | `164917005` | 235 |
| right axis deviation | `47665007` | 215 |
| left bundle branch block | `164909002` | 205 |
| st elevation | `164931005` | 176 |
| av block | `233917008` | 166 |
| countercolockwise rotation | `251199005` | 162 |
| t wave inversion | `59931005` | 157 |
| atrial tachycardia | `713422000` | 121 |
| p wave change | `164912004` | 95 |
| clockwise rotation | `251198002` | 76 |
| prolonged qt interval | `111975006` | 57 |
| myocardial infarction | `164865005` | 40 |
| early repolarization | `428417006` | 22 |
| u wave abnormal | `164937009` | 22 |
| atrioventricular  node reentrant tachycardia | `251166008` | 16 |
| junctional escape | `426995002` | 15 |
| left ventricular hypertrophy | `164873001` | 15 |
| prolonged pr interval | `164947007` | 12 |
| ventricular pre excitation | `195060002` | 12 |
| 2nd degree av block | `195042002` | 8 |
| atrioventricular reentrant tachycardia | `233897008` | 8 |
| right atrial  high voltage | `67751000119106` | 8 |
| ventricular trigeminy | `251180001` | 8 |
| sinus atrium to atrial wandering rhythm | `17366009` | 7 |
| ventricular escape beat | `75532003` | 7 |
| mobitz type i wenckebach atrioventricular block | `54016002` | 6 |
| right ventricular hypertrophy | `89792004` | 4 |
| wolff parkinson white pattern | `74390002` | 4 |
| atrial bigeminy | `251173003` | 3 |
| fqrs wave | `164942001` | 3 |
| right atrial hypertrophy | `446358003` | 3 |
| ventricular bigeminy | `11157007` | 3 |
| fusion beats | `13640000` | 2 |
| st interval abnormal | `164930006` | 2 |
| wandering atrial pacemaker | `195101003` | 2 |
| complete heart block | `27885002` | 1 |
| junctional premature complex | `251164006` | 1 |

### B.10 CODE-15%

Yes/no columns in `exams.csv`. Count = exams marked "yes"; patients in the last column. `ST` means sinus tachycardia, and `normal_ecg` comes from an automatic system [INV; ZEN-CODE15].

| Column | Meaning (from the dataset page) | Exams | Patients |
|---|---|---|---|
| `normal_ecg` | normal ECG per automatic annotation system | 134,657 | 109,623 |
| `RBBB` | right bundle branch block | 9,672 | 6,672 |
| `ST` | sinus tachycardia (NOT ST elevation) | 7,584 | 6,894 |
| `AF` | atrial fibrillation | 7,033 | 4,799 |
| `LBBB` | left bundle branch block | 6,026 | 4,193 |
| `1dAVb` | first degree AV block | 5,716 | 4,701 |
| `SB` | sinus bradycardia | 5,605 | 4,976 |

### B.11 INCART

Free text, exactly as written (spelling kept). Count = records [INV].

**Patient diagnosis text**

| Text as written | Records | Patients |
|---|---|---|
| (no diagnosis text) | 34 | 14 |
| Coronary artery disease, arterial hypertension, left ventricular hypertrophy | 11 | 4 |
| Earlier MI | 9 | 4 |
| Transient ischemic attack | 7 | 4 |
| Acute MI | 6 | 2 |
| Coronary artery disease, arterial hypertension | 6 | 3 |
| Sinus node dysfunction | 2 | 1 |

**Patient diagnosis terms (text split at commas)**

| Text as written | Records | Patients |
|---|---|---|
| arterial hypertension | 17 | 7 |
| Coronary artery disease | 17 | 7 |
| left ventricular hypertrophy | 11 | 4 |

**Record description terms**

| Text as written | Records |
|---|---|
| PVCs | 34 |
| ventricular couplets | 14 |
| paroxysmal VT | 13 |
| ventricular bigeminy | 8 |
| noise | 7 |
| PVCs on bradycardia | 6 |
| couplets | 5 |
| ST depression | 4 |
| ST elevation | 4 |
| WPW | 4 |
| APCs | 3 |
| atrial couplets | 3 |
| AV nodal block 2 degree Moebits 1 | 3 |
| blocked APCs | 3 |
| bradycardia | 3 |
| fusion beats | 3 |
| SVEBs | 3 |
| tachycardia | 3 |
| atrial fibrillation | 2 |
| baseline wander | 2 |
| fusion beats on tachycardia | 2 |
| paroxysmal supraventricular tachycardia | 2 |
| polymorphic PVCs | 2 |
| PVCs on tachycardia | 2 |
| right bundle branch block | 2 |
| trigeminy | 2 |
| ventricular rhythm | 2 |
| ventricular trigeminy | 2 |
| bigeminy | 1 |
| bundle-branch blocks | 1 |
| intraventricular block | 1 |
| negative T | 1 |
| numerous fusion beats | 1 |
| numerous fusion beats and PVCs on tachycardia | 1 |
| paroxysmal atrial fibrillation | 1 |
| paroxysmal supraventricular tachycardia with aberrated QRS | 1 |
| paroxysmal VT on tachycardia | 1 |
| positional changes | 1 |
| positional form and HR change | 1 |
| PVCs and couplets on bradycardia | 1 |
| PVCs and couplets on tachycardia | 1 |
| PVCs and paroxysmal VT on bradycardia | 1 |
| PVCs and ventricular couplets on bradycardia | 1 |
| PVCs on sinus arrhythmia | 1 |
| sinus arrhythmia | 1 |
| ST change | 1 |
| ST changes | 1 |
| supraventricular couplets | 1 |
| supraventricular triplets | 1 |
| SVEBs with wide QRS | 1 |
| triplets on tachycardia | 1 |
| ventricular couplets and R-on-T | 1 |
| ventricular couplets as bigeminy | 1 |
| ventricular couplets on tachycardia | 1 |
| ventricular escape beats | 1 |
| VT | 1 |

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
- **[PN-MIMICED]** MIMIC-IV-ED, release 2.2, PhysioNet (diagnosis table description). https://physionet.org/content/mimic-iv-ed/2.2/
- **[PN-MIMICIV]** MIMIC-IV, release 2.2, PhysioNet (hosp and icu module descriptions). https://physionet.org/content/mimiciv/2.2/
- **[WHO-ICD10-2019]** WHO ICD-10, 2019 edition, official browser. https://icd.who.int/browse10/2019/en (I21, I22, I25; read 2026-10-21).
- **[CMS-CM-FY2025]** CMS/NCHS, "ICD-10-CM Official Guidelines for Coding and Reporting FY 2025", section I.C.9.e (pp. 52–54). https://www.cms.gov/files/document/fy-2025-icd-10-cm-coding-guidelines.pdf
- **[NLM-CM-API]** NIH/NLM Clinical Tables ICD-10-CM code list (edition year not stated). https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search
- **[THCC-TM-2016]** ICD-10-TM 2016, Volume 1 (Tabular List, English–Thai), Chapter IX pp. 286–288. Thai national health coding centre (THCC), http://thcc.or.th/ICD-10TM/ and http://www.thcc.or.th/ebook1/2016/
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
- **[INV]** Full label lists: `label_inventory_<dataset>.csv`, `label_inventory_summary.md` (made by a script from the downloaded files only; checked by the planner).
- **[AFCHK]** Atrial fibrillation vs flutter check for Ningbo and Chapman-Shaoxing (row "AF vs AFL check" in `verified_facts.md`; publisher's label file, our sample headers and the original release's `ConditionNames_SNOMED-CT.csv`).
- **[XWALK]** Common-label table: `label_crosswalk_common.csv` (a team mapping by meaning, checked by the planner; needs supervisor review).
- **[PROV]** Label provenance rows ("S13 provenance" in `verified_facts.md`, including the MIMIC Ext-ICD row).
- **[PROV-XTAB]** PTB-XL check of human validation vs machine-written first reports (row "S13 provenance (crosstab)" in `verified_facts.md`).
- **[LPROV]** Per-class provenance table: `label_provenance.csv` (row "S13 label_provenance" in `verified_facts.md`; counts equal the verified common-label table).
- **[PATH]** Label pathway rows ("S13 pathway" in `verified_facts.md`).
- **[S14A]** Label systems per dataset (row "S14 coding systems (Part A)" in `verified_facts.md`).
- **[S14C]** Comparison of WHO, US and Thai ICD-10 heart-attack codes (row "S14 comparison" in `verified_facts.md`, including the planner's note).
- **[OBS-DOWNLOAD]** `download_manifest.csv`: what was downloaded, from where, and its checksum.
- All checked facts: `verified_facts.md`.
