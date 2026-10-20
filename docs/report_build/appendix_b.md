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
