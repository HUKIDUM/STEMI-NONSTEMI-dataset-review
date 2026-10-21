# PLAN: Dataset review for acute STEMI / NSTEMI / non-MI

| Field | Value |
|---|---|
| Author | planner |
| Date | 2026-10-20 |
| Status | **DRAFT. Waiting for user approval. Nobody starts work before "PLAN APPROVED".** |
| Governing docs | `data_contract.md` 0.1.0-draft, `research_plan.md` 0.1.0-draft, `NEXT_STEPS.md` (read-only for this team) |
| Citation keys | **CMP**, **MCR**, **NB** = the three PDFs in `19-oct-2026/` (see `data_contract.md` §0) |

## 0. Goal and ground rules

**Goal.** For each of the 11 datasets in `data_contract.md` §2.1, answer 10 questions (Q1–Q10 below). Judge each one by how well it helps tell **STEMI from NSTEMI, and both from non-MI**. The outputs are a verified-facts table, small count tables made from metadata files, and a report (`docs/dataset_report.md` + `.pdf`).

**Ground rules (all teammates):**

- Every fact needs a source: a PDF page (`[MCR p.3]`), an official URL, a paper (DOI or PMC link), or a result file in `results/` made from a downloaded official file.
- If something is unknown, write **"not found"** and list where you looked. Never guess. Background knowledge stays tagged BG-UNCONFIRMED until a source confirms it.
- Planner records verified facts in `results/verified_facts.md`. Documenter uses **only** rows marked `verified` there.
- Local counts are *observations of the downloaded file*, not release facts (contract E2, E3). Write them that way.
- Contract rules still apply. Absence of an MI code never means non-MI (L1). Machine text, ST/T-change codes and broad MI statements are never turned into STEMI/NSTEMI (L2, L3). This review **describes** labels. It does not create training labels.
- Downloads cover **metadata and header files only**, never waveforms. Limit: 500 MB per dataset. Everything goes to `data/samples/<dataset_id>/` (gitignored, never committed). Credentialed, DUA or login sources get **no download**: coder stops and planner tells the lead.
- No GitHub (no clone/pull/push/gh; no fetching from github.com, see question U2). No installs without user approval. No deletes.

### The 10 questions (column keys used in `verified_facts.md`)

| Key | Question |
|---|---|
| Q1 `labels` | What labels exist, and in what coding (SCP-ECG, SNOMED CT, ICD-10, AHA, free text, rhythm flags, beat annotations) |
| Q2 `labellers` | Who labelled them: cardiologist(s), physicians, machine, billing codes? Any human check? |
| Q3 `collection` | Hospital(s), country, years, patient type |
| Q4 `setting` | Ambulance, ER, ward, clinic, ICU, Holter/home, or unknown |
| Q5 `device` | ECG machine brand/model, leads, sampling rate, recording length |
| Q6 `stemi_nstemi` | Can it separate STEMI vs NSTEMI, only MI vs no MI, or neither? Give counts of MI-related labels |
| Q7 `model_use` | Best use: STEMI-vs-NSTEMI classifier / MI-vs-non-MI / pretraining only / external test only / not useful |
| Q8 `combine` | Which datasets it can / cannot be combined with, and why (shared patients or overlap, labels, rate, length, leads) |
| Q9 `access` | Open download, account, credentialing, DUA |
| Q10 `size_license` | Size (ECGs, patients, GB) and license |

## 1. Order of work (priority by likely STEMI/NSTEMI usefulness)

The order puts first the datasets that have MI timing or subtype evidence, or that the PDFs name as the first pair [CMP p.4; MCR p.6].

| # | Dataset | Why this position (what planning lookups found, to be verified in phase 2) |
|---|---|---|
| 1 | `ptb_xl` | First pair [CMP p.4]. Has MI statements **plus** `infarction_stadium1/2` (acute/early → old/chronic) and ST-injury codes (PMC7248071). Best open candidate for MI timing. No STEMI/NSTEMI label as such. |
| 2 | `mimic_iv_ecg` | First pair [CMP p.4]. The ECG module is **open** (ODbL, physionet.org/content/mimic-iv-ecg/1.0). STEMI/NSTEMI would need ICD-10 I21.x through the **credentialed** modules (MIMIC-IV hosp/ED, or MIMIC-IV-ECG-ext-ICD). Open files give only machine report text. |
| 3 | `ptb_diagnostic` | 148 MI subjects (physionet.org/content/ptbdb/1.0.0). Header comments may give infarct location and dates, which bear on acuity. Must be checked in the headers. |
| 4 | `sph` | AHA MI codes 160/161/165/166 with *acute / recent / old* modifiers 330–332 (PMC9174207 Table 2). Very few acute cases (1+2+4). |
| 5 | `cpsc_2018` | Challenge SNOMED labels. Background: the CPSC 2018 class list includes ST elevation/depression (BG-UNCONFIRMED; the icbeb.org page was unreachable). |
| 6 | `cpsc_extra` | As CPSC; more SNOMED classes. Overlap with CPSC must be reviewed [MCR p.8]. |
| 7 | `georgia` | Challenge SNOMED labels. May include MI / ST codes; needs header counts. |
| 8 | `ningbo` | SNOMED labels from physicians, with a second physician check (physionet.org/content/ecg-arrhythmia/1.0.0). Linked to Chapman. |
| 9 | `chapman_shaoxing` | As Ningbo. |
| 10 | `code15` | Labels are 6 rhythm/conduction flags + `normal_ecg` + death; **no MI column** (zenodo.org/records/4916206). Most likely pretraining or not useful. |
| 11 | `incart` | 30-min Holter at 257 Hz, beat annotations; 2 patients with acute MI (physionet.org/content/incartdb/1.0.0). Most likely not useful. |

## 2. Sources to consult per dataset

The PDFs come first for every dataset: `data_contract.md` §2–§5 already gives page cites. Use the PMC copy of Nature papers, because nature.com blocks automated fetch.

| Dataset | Official page | Papers / docs | Notes |
|---|---|---|---|
| `ptb_xl` | https://physionet.org/content/ptb-xl/1.0.3/ | Wagner et al. 2020, Sci Data, https://pmc.ncbi.nlm.nih.gov/articles/PMC7248071/ | Labelling: up to 2 cardiologists; 31.2% initial reports auto-generated; `validated_by_human` flag; 400 Hz original resampled to 500 Hz; 51 sites, 11 device types (PMC7248071). Must be verified. |
| `mimic_iv_ecg` | https://physionet.org/content/mimic-iv-ecg/1.0/ | Gow et al. (cite as given on the page); MIMIC-IV-ECG-ext-ICD https://physionet.org/content/mimic-iv-ecg-ext-icd-labels/1.0.1/ (credentialed); MIMIC-IV https://physionet.org/content/mimiciv/ (credentialed) | ~160k patients; >600k cardiologist reports linked by `note_id` to MIMIC-IV-Note (not yet released per page); timestamps may not match clinical records. |
| `ptb_diagnostic` | https://physionet.org/content/ptbdb/1.0.0/ | Bousseljot et al. 1995 (cited on page) | 290 vs 294 subjects conflict [NB p.16] and on the page. |
| `sph` | https://doi.org/10.6084/m9.figshare.c.5779802.v1 (figshare API: https://api.figshare.com/v2/collections/5779802/articles) | Liu et al. 2022, Sci Data, https://pmc.ncbi.nlm.nih.gov/articles/PMC9174207/ | Files are CC0 on figshare. |
| `cpsc_2018`, `cpsc_extra` | https://physionet.org/content/challenge-2021/1.0.3/ ; http://2018.icbeb.org/Challenge.html (unreachable 2026-10-20) | Liu et al. 2018, J Med Imaging Health Inform, doi:10.1166/jmihi.2018.2442; Perez Alday et al. 2020, Physiol Meas, doi:10.1088/1361-6579/abc960; Reyna et al. 2021 CinC, doi:10.23919/CinC53138.2021.9662687 | The Challenge papers describe each source's institution and label process. |
| `georgia` | https://physionet.org/content/challenge-2021/1.0.3/ | Perez Alday 2020; Reyna 2021 (as above) | Page: "Southeastern US". Emory = BG-UNCONFIRMED. |
| `ningbo`, `chapman_shaoxing` | https://physionet.org/content/challenge-2021/1.0.3/ ; https://physionet.org/content/ecg-arrhythmia/1.0.0/ | Zheng et al. 2020, Sci Data, doi:10.1038/s41597-020-0386-x (Chapman); Zheng et al. 2020/2022 Ningbo paper (cited on the ecg-arrhythmia page) | GE MUSE ≠ acquisition model [NB p.15]. |
| `code15` | https://zenodo.org/records/4916206 | Ribeiro et al. 2020, Nat Commun, doi:10.1038/s41467-020-15432-4 (PMC copy) | Label-making method to be taken from the paper. |
| `incart` | https://physionet.org/content/incartdb/1.0.0/ | Page README / record-descriptions.txt | Native 75 vs Challenge 74 records [MCR p.3]. |

## 3. Small downloads for coder (metadata and headers only)

All sizes come from the official file listings on 2026-10-20. Header sizes come from HTTP HEAD requests on single files (0.57–2.7 KB each). Every source listed is **open access**; that is checked again just before download. Where a `SHA256SUMS.txt` exists, coder checks the downloaded files against it (download SHA256SUMS only for that check if it is small; for big ones, check only the lines needed). Downloads use `curl` (wget is not installed) or Python `urllib`, at a polite rate.

| Dataset | Files | Source URL base | Approx. size | Why |
|---|---|---|---|---|
| `ptb_xl` | `ptbxl_database.csv` (6.3 MB), `scp_statements.csv` (9.5 KB), 20 `records500` `.hea` headers chosen with seed 20261020 | https://physionet.org/files/ptb-xl/1.0.3/ | ~6.4 MB | All SCP codes, likelihoods, infarction stadium, `validated_by_human`, device, site, patients. Headers show lead names, gain and units. |
| `mimic_iv_ecg` | `record_list.csv` (67.1 MB), `machine_measurements.csv` (174.2 MB), `machine_measurements_data_dictionary.csv` (1 KB), `waveform_note_links.csv` (56.2 MB), 50 `.hea` headers chosen with seed 20261020 from `record_list.csv` | https://physionet.org/files/mimic-iv-ecg/1.0/ | ~298 MB | Counts of ECGs and subjects, all machine report statements (MI and ST wording, **machine text only**), cart and filter fields, note-link coverage, header leads and units. |
| `ptb_diagnostic` | all 549 `.hea` + `RECORDS`, `CONTROLS`, `README` | https://physionet.org/files/ptbdb/1.0.0/ | ~1.5 MB | Header comments: diagnosis, infarct location/dates if present, 15 channels, fs, sample count → duration. |
| `sph` | `metadata.csv` (999 KB), `code.csv` (1.8 KB), `rule.pdf` (47 KB). **Not** `records.tar.gz` (2.28 GB) | https://ndownloader.figshare.com/files/34793152 , /32630954 , /35284594 | ~1.05 MB | AHA code and modifier counts (MI 160–166 × acute/recent/old), patients, and duration if the metadata has it. |
| `cpsc_2018`, `cpsc_extra`, `georgia`, `ningbo`, `chapman_shaoxing` | **all** `.hea` headers of each Challenge 2021 folder (6,877 + 3,453 + 10,344 + 34,905 + 10,247 = 65,826 files), plus each folder's `RECORDS` | https://physionet.org/files/challenge-2021/1.0.3/training/<folder>/ | ~46 MB in total (≈0.7 KB/header); Ningbo ≈ 25 MB | Full `#Dx` SNOMED counts, so no rare MI/ST code is missed; also fs, length, lead names, age/sex. Many small requests (est. 1–2 h). See question U3. |
| (label names for the above) | `ConditionNames_SNOMED-CT.csv` (2.5 KB) | https://physionet.org/files/ecg-arrhythmia/1.0.0/ | 2.5 KB | SNOMED code → name. Codes not in it are looked up by planner (or with `dx_mapping_*.csv` if U2 allows). |
| `code15` | `exams.csv` (35.5 MB). **Not** the HDF5 zips (≈2.7 GB each) | https://zenodo.org/records/4916206/files/exams.csv | 35.5 MB | Label column sums, patients, exams per patient. Confirms whether any MI label exists. |
| `incart` | 75 `.hea`, `README`, `RECORDS`, `record-descriptions.txt`, `files-patients-diagnoses.txt`, `ANNOTATORS` | https://physionet.org/files/incartdb/1.0.0/ | ~55 KB | Per-record diagnoses (acute MI patients), fs, duration, gains. `.atr` is not needed. |
| *optional, overlap check* | Challenge 2021 `ptb-xl` (21,837) and `ptb` (516) `.hea` headers | https://physionet.org/files/challenge-2021/1.0.3/training/ptb-xl/ , /ptb/ | ~16 MB | Record-ID overlap between native and Challenge editions (contract O8, O10). Only if U4 = yes. |

**No download (credentialed / DUA).** MIMIC-IV clinical modules (hosp, ED), MIMIC-IV-ECG-ext-ICD (credentialed + DUA + CITI, per its page), and MIMIC-IV-Note. If coder meets a login wall anywhere else, coder stops and reports to planner.

## 4. Scripts for coder (`src/stemi/review/`, outputs in `results/`)

Constraints: `.venv` has pandas + numpy + pytest only (no wfdb, no h5py). That is enough, because only CSV and text `.hea` files are read. Every script takes the sample path as an argument and writes CSVs plus a short `results/<dataset>_summary.md` that says what the output is (a local observation of a named file, its release and download date). Each parser gets a unit test on small synthetic fixtures in `tests/`. Coder runs Python on downloaded files with `-I`.

| Script | Reads | Counts / outputs |
|---|---|---|
| `fetch_samples.py` | the table in §3 (hard-coded manifest) | Downloads to `data/samples/<id>/`. Writes `results/download_manifest.csv` (url, local path, bytes, sha256, date, checksum match yes/no/not available). Refuses any file not in the manifest, and anything over 500 MB per dataset. |
| `hea_parser.py` (module) | WFDB `.hea` text | fs, n_sig, n_samples → duration s, lead names in order, units/gain/baseline, comment lines as key/value pairs. |
| `review_ptbxl.py` | `ptbxl_database.csv`, `scp_statements.csv`, headers | `ptb_xl_scp_counts.csv`: every SCP code with description, category and diagnostic class, number of ECGs, number of patients, and counts at likelihood 100 / 50–<100 / <50 / 0. `ptb_xl_mi_by_stadium.csv`: MI and injury codes × `infarction_stadium1/2`. Also counts of `validated_by_human`, `initial_autogenerated_report`, `second_opinion`, devices, sites, patients, ECGs per patient, and header leads/fs/units. |
| `review_mimic.py` | the 3 CSVs + dictionary + headers | ECGs, subjects, ECGs per subject. Frequency table of all distinct `report_*` statements, with an *MI/ST keyword flag* (infarct, STEMI, injury, ST elevation, acute, …) for listing only (L2). `cart_id` and filter-field value counts as raw strings (C2.6). Share of ECGs with a `note_id`. Header leads/units/gain. Years are **not** reported from shifted dates (C2.7). |
| `review_ptbdb.py` | 549 headers | Per-record table: patient, channels, fs, duration, every comment field. Value counts of reason for admission / diagnosis and of any infarct-location or date fields. MI subjects with and without date fields. |
| `review_sph.py` | `metadata.csv`, `code.csv` | Counts for every AHA code and code+modifier pair (focus on 160–166 × 330–334), ECGs, patients, ECGs per patient, duration distribution if available, age/sex. |
| `review_challenge.py` | all headers of the 5 sources + `ConditionNames_SNOMED-CT.csv` | Per source: SNOMED code counts with names (unknown → "unmapped", for planner to look up); MI / ST-elevation / ST-depression / injury / Q-wave code counts; fs, duration distribution, lead order, gain/units; age/sex; whether any patient-ID field exists. |
| `review_code15.py` | `exams.csv` | Label column sums, `normal_ecg`, patients, exams per patient, `trace_file` spread. States that no MI column exists if none is found. |
| `review_incart.py` | headers + text files | Per-record diagnoses, patient number, fs, duration, gains; acute-MI records listed. |
| `overlap_ids.py` | outputs above (+ optional U4 headers) | ID-level overlap: PTB-XL native 21,799 vs Challenge 21,837; PTB-DB 549 vs Challenge 516; CPSC vs CPSC-Extra name ranges; INCART 75 vs 74 (from the Challenge `RECORDS` list). Signal-level duplicates are **out of scope** (no waveforms, O9). |
| `build_summary.py` | all `results/*` | `results/dataset_summary.csv`: one row per dataset with ECGs, patients, fs, leads, duration range, number of MI-related labels, and whether acute/subtype information exists. |

## 5. Steps tracked in STATUS.md

| Step | Owner | Done when |
|---|---|---|
| S0 Plan approved by user | lead | "PLAN APPROVED" received |
| S1 `fetch_samples.py` + tests; download open metadata (§3) | coder | manifest written; checksums checked |
| S2 Shared `hea_parser.py` + tests | coder | tests pass |
| S3 `ptb_xl` review: script, results, desk research Q1–Q10 | coder → planner verifies | rows verified in `verified_facts.md` |
| S4 `mimic_iv_ecg` | same | same |
| S5 `ptb_diagnostic` | same | same |
| S6 `sph` | same | same |
| S7 Challenge sources (`cpsc_2018`, `cpsc_extra`, `georgia`, `ningbo`, `chapman_shaoxing`) | same | same |
| S8 `code15` | same | same |
| S9 `incart` | same | same |
| S10 Overlap / combinability (Q8 for all) + `dataset_summary.csv` | coder → planner | Q8 rows verified |
| S11 Report `docs/dataset_report.md` | documenter | uses only verified rows; planner spot-checks |
| S12 Report PDF | documenter | PDF built (method depends on U6) |
| S13 Final report to lead | planner | sent |

Coder does both the counting **and** the desk research (official pages and papers) for Q1–Q10. Each finding goes into a per-dataset file `results/findings_<dataset>.md`, one line per question with its source. Planner checks each one against the source and moves it into `verified_facts.md`. After every finished step, planner updates STATUS.md and makes a local commit.

## 6. Report outline (documenter: `docs/dataset_report.md` → `.pdf`)

1. **Summary.** Answers the user's questions in one page: which datasets can be used, for which model, and which can be combined.
2. **How this review was done.** Sources, what was downloaded (metadata only), what was not (waveforms, credentialed data), and the verified / not found rule.
3. **Overview table.** All 11 datasets × key facts (labels, labeller, country/years, setting, device/fs/length, STEMI/NSTEMI ability, best use, access, size/license).
4. **STEMI / NSTEMI / MI label inventory.** Per dataset: the MI-related labels, counts, acute/recent/old information, and whether STEMI vs NSTEMI is possible. Plain statement of the L1/L2 limits.
5. **One section per dataset (in the §1 order).** Q1–Q10, each with its source.
6. **Combining datasets.** A matrix of can / cannot / only after checks, with reasons: overlap, label system, fs, length, leads, patient IDs. Links to contract O1–O11.
7. **Recommended use per model.** STEMI-vs-NSTEMI, MI-vs-non-MI, pretraining, external test.
8. **What is not known and what blocks progress.** "Not found" items and questions for the user and supervisor.
9. **Appendix.** Sources list; download manifest; result-file index.

Style: plain English, short sentences, every factual sentence cited.

## 7. Questions for the user (ASSUMPTION / BG-UNCONFIRMED)

- **U1 MIMIC credentialed access.** STEMI vs NSTEMI in MIMIC needs ICD-10 codes (e.g. I21.0–I21.3 vs I21.4; code meaning to be verified) from credentialed MIMIC-IV / MIMIC-IV-ECG-ext-ICD. Do you have PhysioNet credentialed access with the DUA signed? If yes, would you run a count script yourself? If not, the report will say "possible with credentialed access, not checked".
- **U2 GitHub-hosted label mappings.** The Challenge 2021 SNOMED mapping files (`dx_mapping_scored.csv`, `dx_mapping_unscored.csv`) are on GitHub. The team rule says "no GitHub at all". May coder or planner *read* these two files over plain HTTPS (no git, no account)? If not, we use the PhysioNet `ConditionNames_SNOMED-CT.csv` plus manual lookups.
- **U3 Challenge headers.** Download all 65,826 small headers (~46 MB, about 1–2 h of polite requests) so that rare MI/ST labels are counted completely? The alternative is one `g1` folder (≤1,000 headers) per source, which can miss rare labels and gives no full counts.
- **U4 Optional overlap headers.** Also download the Challenge copies of PTB-XL and PTB headers (~16 MB) for an ID-level overlap check?
- **U5 MIMIC CSVs (~298 MB).** OK to download these open files (ODbL)? They are the only way to count machine MI/ST statements and note-link coverage.
- **U6 PDF build.** `pandoc` is installed but has no PDF engine (no LaTeX, wkhtmltopdf, weasyprint or Chrome). Options: (a) install `weasyprint` into `.venv`, (b) install a LaTeX engine, (c) deliver HTML + Markdown only and you print to PDF. Which one?
- **U7 Code location.** Review scripts go in `src/stemi/review/` (new subpackage). OK?
- **U8 BG-UNCONFIRMED items to check (no answer needed now):** CPSC 2018 has an ST-elevation class; Georgia comes from Emory; PTB-DB headers have infarct date fields; Chapman/Ningbo export overlap; CODE-15 labels came from cardiologists + automatic systems. Each will be marked verified or not found.

## 8. Add-on S13: label provenance (approved by the user 2026-10-21, via team-lead)

**Goal.** A table, per dataset × label class, of HOW each label was made, plus a per-dataset label pathway (S1b). Columns:
- labeller (ECG machine / cardiologist reading the ECG / billing coder (ICD) / study doctors);
- steps (e.g. auto statement → cardiologist → 2nd cardiologist);
- basis (ECG only vs whole hospital stay or health record);
- timing link to this ECG;
- count;
- source.

**Classes in scope:** all MI / ST / ischaemia / Q-wave classes, plus the 21 labels in `results/label_crosswalk_common.csv`. MIMIC: I21.0–I21.3 (STEMI), I21.4 (NSTEMI), I21.9 / I21.A, I22, I25.2 (old MI), only if the user approves access (S0).

**Rules.** As for the review: every fact sourced; "not found" plus where we looked; no downloads without the user's OK; no logins; no GitHub. Commit locally after each step. A class gets the dataset-level method unless a source states a class-specific method; that inheritance is written explicitly in each cell ("dataset-level method; no class-specific statement found").

| Step | Owner | Content |
|---|---|---|
| S0 | planner | Identify `data/samples/mimic_iv_ecg/records_w_diag_icd10.csv` from web pages only (do NOT open it). Done 2026-10-21: MIMIC-IV-ECG-Ext-ICD (credentialed + DUA + CITI); reported to the lead; the user decides on access. |
| S1 | planner | Verify provenance facts per dataset (reuse existing verified rows; new rows tagged "S13"): PTB-XL, PTB Diagnostic, SPH, CODE-15%, CPSC 2018, CPSC-Extra, Georgia, Ningbo, Chapman, INCART, MIMIC-IV-ECG machine statements, and (if approved) Ext-ICD. |
| S1b | planner | **Pathway (scope addition 2026-10-21):** per dataset, an ordered chain: (1) where/when recorded, (2) each later labelling stage (who, with what), (3) which stage our label file comes from, (4) the documented time gap ECG → label. Every step sourced or "not found". Do not assume a stage the user suggested (e.g. ICU) without a source. Done: 8 "S13 pathway" rows. |
| S2 | coder | Per-class counts → `results/label_provenance.csv` (dataset, class, source codes, count, count type, provenance fields filled only from S13 verified rows). MIMIC ICD counts only via a user-run aggregate script, unless the user approves otherwise. |
| S3 | planner | Verify S2 against the files and rows. |
| S4 | documenter | Report §4c "How each label was made", from verified rows only; rebuild the PDF. |
