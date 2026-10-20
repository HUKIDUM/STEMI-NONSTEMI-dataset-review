# INCART review (local observation)

- Dataset: `incart`, release 1.0.0 native
- Script: `src/stemi/review/review_incart.py`; generated 2026-10-20T13:25:50+00:00
- Local observation of the downloaded file(s) named below; not a release-level fact (data_contract E2, E3). Labels are described, not converted into training labels (L1, L2).

## Input files

| local_path | url | sha256 | download_utc | checksum_match |
|---|---|---|---|---|
| data/samples/incart/RECORDS | https://physionet.org/files/incartdb/1.0.0/RECORDS | 9740d592ab5564dc812dc7f6cbd9b44a6694a2cd7d879c93dc95b2bd47313434 | 2026-10-20T12:38:32+00:00 | yes |
| data/samples/incart/record-descriptions.txt | https://physionet.org/files/incartdb/1.0.0/record-descriptions.txt | e119302fc9e16264f98b0c6d6f7438d27b51785d584a1609775dc1ed0ce35458 | 2026-10-20T12:38:45+00:00 | yes |
| data/samples/incart/files-patients-diagnoses.txt | https://physionet.org/files/incartdb/1.0.0/files-patients-diagnoses.txt | 7710993dd08ac1ee6e3912756b78cc16e9df40d14e5fb768c3c42a5197c79c17 | 2026-10-20T12:38:51+00:00 | yes |
| data/samples/incart/ANNOTATORS | https://physionet.org/files/incartdb/1.0.0/ANNOTATORS | 7391bbef14a82c1c74534ed835dd7ad86296238f50ef5a13d4290713ab75d6b3 | 2026-10-20T12:38:53+00:00 | yes |
| data/samples/incart/README | https://physionet.org/files/incartdb/1.0.0/README | 59e12ddc1601b0ca0a505117c984957a1c53d50d8673befce7c661ce5260564d | 2026-10-20T12:38:41+00:00 | yes |

## Basic counts

| item | value |
|---|---|
| records in RECORDS | 75 |
| headers read | 75 |
| fs values | 257: 75 |
| n_sig values | 12: 75 |
| duration s min / max | 1800 / 1800 |
| lead name sets | I|II|III|AVR|AVL|AVF|V1|V2|V3|V4|V5|V6 (75) |
| gains | 617.0 (17); 612.0 (13); 1041.0 (9); 623.0 (9); 240.0 (5); 254.0 (5); 514.0 (5); 515.0 (4); 306.0 (2); 516.0 (2); 248.0 (2); 1063.0 (2) |
| units |  |

## Lines mentioning infarct / MI / ischemia (listing only)

- files-patients-diagnoses.txt: Acute MI
- files-patients-diagnoses.txt: Transient ischemic attack
- files-patients-diagnoses.txt: Transient ischemic attack
- files-patients-diagnoses.txt: Transient ischemic attack
- files-patients-diagnoses.txt: Earlier MI
- files-patients-diagnoses.txt: Transient ischemic attack
- files-patients-diagnoses.txt: Earlier MI
- files-patients-diagnoses.txt: Earlier MI
- files-patients-diagnoses.txt: Acute MI
- files-patients-diagnoses.txt: Earlier MI
- README: The original records were collected from patients undergoing tests for coronary artery disease (17 men and 15 women, aged 18-80; mean age: 58). None of the patients had pacemakers; most had ventricular ectopic beats. In selecting records to be included in the database, preference was given to subjects with ECGs consistent with ischemia, coronary artery disease, conduction abnormalities, and arrhythmias; observations of those selected included:
- README: Acute MI		2
- README: Transient ischemic attack (angina pectoris)	5
- README: Earlier MI	4

## record-descriptions.txt (verbatim)

```
I01
PVCs, noise
I02
ventricular trigeminy, ventricular couplets
I03
ST elevation, PVCs
I04
bradycardia, tachycardia, PVCs, ventricular couplets, paroxysmal VT
I05
paroxysmal VT
I06
ST changes, PVCs
I07
PVCs, supraventricular triplets
I08
ventricular bigeminy, ventricular couplets
I09
ventricular couplets, ventricular escape beats, AV nodal block 2 degree Moebits 1
I10
tachycardia, AV nodal block 2 degree Moebits 1, noise
I11
PVCs, AV nodal block 2 degree Moebits 1
I12
ST depression, ventricular couplets
I13
PVCs
I14
PVCs, baseline wander
I15
ST depression, PVCs
I16
right bundle branch block, polymorphic PVCs, noise
I17
bradycardia, PVCs, right bundle branch block,  
I18
PVCs, numerous fusion beats
I19
ventricular trigeminy, PVCs
I20
ventricular couplets, fusion beats; APCs, atrial couplets, blocked APCs, paroxysmal supraventricular tachycardia
I21
PVCs, APCs, atrial couplets, blocked APCs
I22
paroxysmal VT, APCs, atrial couplets, blocked APCs
I23
polymorphic PVCs, intraventricular block
I24
PVCs,   ST depression
I25
paroxysmal VT
I26
ventricular couplets, paroxysmal supraventricular tachycardia
I27
ventricular bigeminy, trigeminy, PVCs
I28
PVCs on bradycardia
I29
PVCs, couplets, paroxysmal VT, noise
I30
VT
I31
paroxysmal VT, baseline wander
I32
ventricular bigeminy
I33
PVCs, SVEBs,  supraventricular couplets
I34
SVEBs, couplets,  paroxysmal supraventricular tachycardia with aberrated QRS
I35
ventricular couplets, fusion beats on tachycardia
I36
PVCs, ventricular couplets as bigeminy
I37
PVCs on bradycardia
I38
PVCs, couplets, triplets on tachycardia
I39
PVCs and couplets on bradycardia
I40
PVCs, ventricular bigeminy, ST change
I41
PVCs, sinus arrhythmia, noise
I42
PVCs, ventricular couplets, ventricular bigeminy, paroxysmal VT
I43
PVCs, ventricular couplets, ventricular bigeminy, paroxysmal VT, ventricular rhythm
I44
PVCs, paroxysmal VT
I45
ventricular couplets
I46
PVCs on tachycardia, fusion beats
I47
PVCs on sinus arrhythmia, ventricular bigeminy
I48
PVCs, ventricular couplets
I49
PVCs on bradycardia, atrial fibrillation
I50
PVCs, tachycardia, atrial fibrillation, ST depression
I51
PVCs on tachycardia, bigeminy, trigeminy
I52
PVCs on bradycardia, ventricular bigeminy
I53
PVCs, ventricular couplets and R-on-T
I54
PVCs, ventricular couplets, paroxysmal VT, noise
I55
paroxysmal VT
I56
PVCs , positional form and HR change 
I57
fusion beats, ventricular couplets on tachycardia
I58
PVCs on bradycardia
I59
PVCs, ventricular couplets, ST elevation
I60
ST elevation
I61
positional changes, bradycardia
I62
ventricular rhythm, ST elevation
I63
PVCs
I64
PVCs, negative T
I65
PVCs, couplets, paroxysmal VT, fusion beats on tachycardia
I66
paroxysmal VT, noise
I67
paroxysmal VT on tachycardia
I68
PVCs, WPW
I69
PVCs and ventricular couplets on bradycardia, WPW
I70
SVEBs with wide QRS, WPW
I71
paroxysmal atrial fibrillation, WPW, bundle-branch blocks
I72
PVCs and couplets on tachycardia
I73
PVCs on bradycardia, SVEBs, couplets
I74
numerous fusion beats and PVCs on tachycardia
I75
PVCs and paroxysmal VT on bradycardia
```

## files-patients-diagnoses.txt (verbatim)

```
patient 1
I01 I02
Coronary artery disease, arterial hypertension
patient 2
I03 I04 I05
Acute MI
patient 3
I06 I07
Transient ischemic attack
patient 4
I08

patient 5
I09 I10 I11

patient 6
I12 I13 I14

patient 7
I15
Transient ischemic attack
patient 8
I16 I17
Transient ischemic attack
patient 9
I18 I19

patient 10
I20 I21 I22
Coronary artery disease, arterial hypertension, left ventricular hypertrophy
patient 11
I23 I24
Earlier MI
patient 12
I25 I26
Sinus node dysfunction
patient 13
I27 I28

patient 14
I29 I30 I31 I32

patient 15
I33 I34

patient 16
I35 I36 I37
Coronary artery disease, arterial hypertension, left ventricular hypertrophy
patient 17
I38 I39
Coronary artery disease, arterial hypertension
patient 18
I40 I41
Transient ischemic attack
patient 19
I42 I43

patient 20
I44 I45 I46
Coronary artery disease, arterial hypertension, left ventricular hypertrophy
patient 21
I47 I48
Earlier MI
patient 22
I49 I50

patient 23
I51 I52 I53

patient 24
I54 I55 I56
Earlier MI
patient 25
I57 I58
Coronary artery disease, arterial hypertension
patient 26
I59 I60 I61

patient 27
I62 I63 I64
Acute MI
patient 28
I65 I66 I67

patient 29
I68 I69

patient 30
I70 I71

patient 31
I72 I73
Coronary artery disease, arterial hypertension, left ventricular hypertrophy
patient 32
I74 I75
Earlier MI
```

## ANNOTATORS (verbatim)

```
atr	reference beat annotations
```

## README (verbatim)

```
This database consists of 75 annotated recordings extracted from 32 Holter records. Each record is 30 minutes long and contains 12 standard leads, each sampled at 257 Hz, with gains varying from 250 to 1100 analog-to-digital converter units per millivolt. Gains for each record are specified in its .hea file. The reference annotation files contain over 175,000 beat annotations in all. 

The original records were collected from patients undergoing tests for coronary artery disease (17 men and 15 women, aged 18-80; mean age: 58). None of the patients had pacemakers; most had ventricular ectopic beats. In selecting records to be included in the database, preference was given to subjects with ECGs consistent with ischemia, coronary artery disease, conduction abnormalities, and arrhythmias; observations of those selected included: 

Diagnosis/ECG abnormalities		Patients

Acute MI		2

Transient ischemic attack (angina pectoris)	5

Earlier MI	4

Coronary artery disease with arterial hypertension		7 (4 with ECGs consistent with left ventricular hypertrophy)

Sinus node dysfunction	1

Atrial fibrillation or supraventricular tachycardia	3 (2 with paroxysmal)

WPW		2

Intraventricular heart block		3

AV block		1

Supraventricular ectopy	18

Diagnoses were confirmed by enzyme check, coronary angiography, electrophysiological study, pressure monitoring where necessary. 

Patients, dianoses and record features are identified in .hea files. Summary is availiable in record-descriptions.txt and files-patients-diagnoses.txt

The annotations were produced by an automatic algorithm and then corrected manually, following the standard PhysioBank beat annotation definitions. The algorithm generally places beat annotations in the middle of the QRS complex (as determined from all 12 leads); the locations have not been manually corrected, however, and there may be occasional misaligned annotations as a result. 

This database was contributed by St.-Petersburg Institute of Cardiological Technics (Incart), Saint-Petersburg, Russia. The database was initially developed by Viktor Tihonenko (vmt@incart.ru) and Alexander Khaustov (avk@incart.ru). Additional verification was done by Sergey Ivanov and Alexei Rivin (Incart). Please refer questions and corrections to avk@incart.ru.
```

## Header comments (per record)

| record | comments |
|---|---|
| I01 | <age>: 65 <sex>: F <diagnoses> Coronary artery disease, arterial hypertension | patient 1 | PVCs, noise |
| I02 | <age>: 65 <sex>: F <diagnoses> Coronary artery disease, arterial hypertension | patient 1 | ventricular trigeminy, ventricular couplets |
| I03 | <age>: 59 <sex>: M <diagnoses> Acute MI | patient 2 | ST elevation, PVCs |
| I04 | <age>: 59 <sex>: M <diagnoses> Acute MI | patient 2 | bradycardia, tachycardia, PVCs, ventricular couplets, paroxysmal VT |
| I05 | <age>: 59 <sex>: M <diagnoses> Acute MI | patient 2 | paroxysmal VT |
| I06 | <age>: 80 <sex>: M <diagnoses> Transient ischemic attack | patient 3 | ST changes, PVCs |
| I07 | <age>: 80 <sex>: M <diagnoses> Transient ischemic attack | patient 3 | PVCs, supraventricular triplets |
| I08 | <age>: 51 <sex>: F | patient 4 | ventricular bigeminy, ventricular couplets |
| I09 | <age>: 68 <sex>: M | patient 5 | ventricular couplets, ventricular escape beats, AV nodal block 2 degree Moebits 1 |
| I10 | <age>: 68 <sex>: M | patient 5 | tachycardia, AV nodal block 2 degree Moebits 1, noise |
| I11 | <age>: 68 <sex>: M | patient 5 | PVCs, AV nodal block 2 degree Moebits 1 |
| I12 | <age>: 39 <sex>: F | patient 6 | ST depression, ventricular couplets |
| I13 | <age>: 39 <sex>: F | patient 6 | PVCs |
| I14 | <age>: 39 <sex>: F | patient 6 | PVCs, baseline wander |
| I15 | <age>: 57 <sex>: M <diagnoses> Transient ischemic attack | patient 7 | ST depression, PVCs |
| I16 | <age>: 64 <sex>: M <diagnoses> Transient ischemic attack | patient 8 | right bundle branch block, polymorphic PVCs, noise |
| I17 | <age>: 64 <sex>: M <diagnoses> Transient ischemic attack | patient 8 | bradycardia, PVCs, right bundle branch block, |
| I18 | <age>: 18 <sex>: F | patient 9 | PVCs, numerous fusion beats |
| I19 | <age>: 18 <sex>: F | patient 9 | ventricular trigeminy, PVCs |
| I20 | <age>: 59 <sex>: F <diagnoses> Coronary artery disease, arterial hypertension, left ventricular hypertrophy | patient 10 | ventricular couplets, fusion beats; APCs, atrial couplets, blocked APCs, paroxysmal supraventricular tachycardia |
| I21 | <age>: 59 <sex>: F <diagnoses> Coronary artery disease, arterial hypertension, left ventricular hypertrophy | patient 10 | PVCs, APCs, atrial couplets, blocked APCs |
| I22 | <age>: 59 <sex>: F <diagnoses> Coronary artery disease, arterial hypertension, left ventricular hypertrophy | patient 10 | paroxysmal VT, APCs, atrial couplets, blocked APCs |
| I23 | <age>: 52 <sex>: M <diagnoses> Earlier MI | patient 11 | polymorphic PVCs, intraventricular block |
| I24 | <age>: 52 <sex>: M <diagnoses> Earlier MI | patient 11 | PVCs,   ST depression |
| I25 | <age>: 66 <sex>: F <diagnoses> Sinus node dysfunction | patient 12 | paroxysmal VT |
| I26 | <age>: 66 <sex>: F <diagnoses> Sinus node dysfunction | patient 12 | ventricular couplets, paroxysmal supraventricular tachycardia |
| I27 | <age>: 60 <sex>: M | patient 13 | ventricular bigeminy, trigeminy, PVCs |
| I28 | <age>: 60 <sex>: M | patient 13 | PVCs on bradycardia |
| I29 | <age>: 41 <sex>: F | patient 14 | PVCs, couplets, paroxysmal VT, noise |
| I30 | <age>: 41 <sex>: F | patient 14 | VT |
| I31 | <age>: 41 <sex>: F | patient 14 | paroxysmal VT, baseline wander |
| I32 | <age>: 41 <sex>: F | patient 14 | ventricular bigeminy |
| I33 | <age>: 40 <sex>: M | patient 15 | PVCs, SVEBs,  supraventricular couplets |
| I34 | <age>: 40 <sex>: M | patient 15 | SVEBs, couplets,  paroxysmal supraventricular tachycardia with aberrated QRS |
| I35 | <age>: 38 <sex>: F <diagnoses> Coronary artery disease, arterial hypertension, left ventricular hypertrophy | patient 16 | ventricular couplets, fusion beats on tachycardia |
| I36 | <age>: 38 <sex>: F <diagnoses> Coronary artery disease, arterial hypertension, left ventricular hypertrophy | patient 16 | PVCs, ventricular couplets as bigeminy |
| I37 | <age>: 38 <sex>: F <diagnoses> Coronary artery disease, arterial hypertension, left ventricular hypertrophy | patient 16 | PVCs on bradycardia |
| I38 | <age>: 60 <sex>: F <diagnoses> Coronary artery disease, arterial hypertension | patient 17 | PVCs, couplets, triplets on tachycardia |
| I39 | <age>: 60 <sex>: F <diagnoses> Coronary artery disease, arterial hypertension | patient 17 | PVCs and couplets on bradycardia |
| I40 | <age>: 66 <sex>: M <diagnoses> Transient ischemic attack | patient 18 | PVCs, ventricular bigeminy, ST change |
| I41 | <age>: 66 <sex>: M <diagnoses> Transient ischemic attack | patient 18 | PVCs, sinus arrhythmia, noise |
| I42 | <age>: 19 <sex>: M | patient 19 | PVCs, ventricular couplets, ventricular bigeminy, paroxysmal VT |
| I43 | <age>: 19 <sex>: M | patient 19 | PVCs, ventricular couplets, ventricular bigeminy, paroxysmal VT, ventricular rhythm |
| I44 | <age>: 53 <sex>: F <diagnoses> Coronary artery disease, arterial hypertension, left ventricular hypertrophy | patient 20 | PVCs, paroxysmal VT |
| I45 | <age>: 53 <sex>: F <diagnoses> Coronary artery disease, arterial hypertension, left ventricular hypertrophy | patient 20 | ventricular couplets |
| I46 | <age>: 53 <sex>: F <diagnoses> Coronary artery disease, arterial hypertension, left ventricular hypertrophy | patient 20 | PVCs on tachycardia, fusion beats |
| I47 | <age>: 68 <sex>: F <diagnoses> Earlier MI | patient 21 | PVCs on sinus arrhythmia, ventricular bigeminy |
| I48 | <age>: 68 <sex>: F <diagnoses> Earlier MI | patient 21 | PVCs, ventricular couplets |
| I49 | <age>: 70 <sex>: M | patient 22 | PVCs on bradycardia, atrial fibrillation |
| I50 | <age>: 70 <sex>: M | patient 22 | PVCs, tachycardia, atrial fibrillation, ST depression |
| I51 | <age>: 56 <sex>: M | patient 23 | PVCs on tachycardia, bigeminy, trigeminy |
| I52 | <age>: 56 <sex>: M | patient 23 | PVCs on bradycardia, ventricular bigeminy |
| I53 | <age>: 56 <sex>: M | patient 23 | PVCs, ventricular couplets and R-on-T |
| I54 | <age>: 74 <sex>: M <diagnoses> Earlier MI | patient 24 | PVCs, ventricular couplets, paroxysmal VT, noise |
| I55 | <age>: 74 <sex>: M <diagnoses> Earlier MI | patient 24 | paroxysmal VT |
| I56 | <age>: 74 <sex>: M <diagnoses> Earlier MI | patient 24 | PVCs , positional form and HR change |
| I57 | <age>: 45 <sex>: F <diagnoses> Coronary artery disease, arterial hypertension | patient 25 | fusion beats, ventricular couplets on tachycardia |
| I58 | <age>: 45 <sex>: F <diagnoses> Coronary artery disease, arterial hypertension | patient 25 | PVCs on bradycardia |
| I59 | <age>: 49 <sex>: F | patient 26 | PVCs, ventricular couplets, ST elevation |
| I60 | <age>: 49 <sex>: F | patient 26 | ST elevation |
| I61 | <age>: 49 <sex>: F | patient 26 | positional changes, bradycardia |
| I62 | <age>: 58 <sex>: M <diagnoses> Acute MI | patient 27 | ventricular rhythm, ST elevation |
| I63 | <age>: 58 <sex>: M <diagnoses> Acute MI | patient 27 | PVCs |
| I64 | <age>: 58 <sex>: M <diagnoses> Acute MI | patient 27 | PVCs, negative T |
| I65 | <age>: 58 <sex>: F | patient 28 | PVCs, couplets, paroxysmal VT, fusion beats on tachycardia |
| I66 | <age>: 58 <sex>: F | patient 28 | paroxysmal VT, noise |
| I67 | <age>: 58 <sex>: F | patient 28 | paroxysmal VT on tachycardia |
| I68 | <age>: 62 <sex>: M | patient 29 | PVCs, WPW |
| I69 | <age>: 62 <sex>: M | patient 29 | PVCs and ventricular couplets on bradycardia, WPW |
| I70 | <age>: 64 <sex>: M | patient 30 | SVEBs with wide QRS, WPW |
| I71 | <age>: 64 <sex>: M | patient 30 | paroxysmal atrial fibrillation, WPW, bundle-branch blocks |
| I72 | <age>: 73 <sex>: M <diagnoses> Coronary artery disease, arterial hypertension, left ventricular hypertrophy | patient 31 | PVCs and couplets on tachycardia |
| I73 | <age>: 73 <sex>: M <diagnoses> Coronary artery disease, arterial hypertension, left ventricular hypertrophy | patient 31 | PVCs on bradycardia, SVEBs, couplets |
| I74 | <age>: 66 <sex>: M <diagnoses> Earlier MI | patient 32 | numerous fusion beats and PVCs on tachycardia |
| I75 | <age>: 66 <sex>: M <diagnoses> Earlier MI | patient 32 | PVCs and paroxysmal VT on bradycardia |
