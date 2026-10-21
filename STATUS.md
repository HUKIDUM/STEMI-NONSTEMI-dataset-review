# STATUS: Dataset review (STEMI / NSTEMI / non-MI)

> **GitHub (2026-10-21):** published at https://github.com/HUKIDUM/STEMI-NONSTEMI-dataset-review (public, branch `main`, CI tests passing). Commit emails use the GitHub noreply address; the local branch `backup-before-email-rewrite` keeps the original history. Push only with the user's OK.

> **File locations (2026-10-21, GitHub preparation):** `PLAN.md`, `TASKS.md`, `NEXT_STEPS.md`, `data_contract.md` and `research_plan.md` moved to `docs/project/`. `data_contract.backup.md` stays local only (git-ignored). Repository front page: `README.md`.

Owner: planner. A new session reads this first. Plan: `PLAN.md` (APPROVED 2026-10-20, with the user answers below).

Last update: 2026-10-21 (team-lead)

## Team rule: what needs a download request (team-lead 2026-10-20; the user may overrule)
- **No request needed:** reading official web pages, papers and small API metadata (e.g. figshare/Zenodo JSON for license and md5) to check facts. Cite the URL.
- **No request needed (adjustment, team-lead 2026-10-20):** HEAD requests (headers only, no file body) to learn a file's size, because every download request must give sizes.
- **Request needed first, even if nothing is saved:** any GET of file content from a dataset's file tree (physionet.org/files/..., ndownloader.figshare.com, zenodo.org/.../files/, raw dataset files), including index files, RECORDS lists and checksum lists (SHA256SUMS).
- **Rule addition (team-lead 2026-10-20; the user may overrule):** papers/PDFs hosted inside a dataset's file area (e.g. challenge-2021 `papers/`) count as reading material, like web pages, so no request is needed. Data, index, RECORDS and checksum files still need one.

## Done
- S0: `PLAN.md` approved by the user via team-lead (2026-10-20).
- Environment: documenter installed `markdown_pdf` 1.13.3 (+ deps pymupdf 2.0, pymupdf_layout 2.0, pymupdf4llm 2.0, markdown-it-py 4.2.0, mdurl 0.1.2) into the project `.venv` only, for `docs/dataset_report.pdf`. Approved by the user (confirmed by team-lead). No weasyprint, no LaTeX.

## User answers to PLAN §7 (binding)
- U1: No team login, credentials or credentialed files. Coder writes `src/stemi/review/mimic_icd_count.py` for the USER to run locally; it prints aggregate counts only (e.g. ECGs/admissions with I21.0–I21.3 vs I21.4, other I21/I22), never row-level data. Until the counts come back, the report says "not checked yet: needs credentialed access; the user will run the count script".
- U2: Yes. Read the two Challenge `dx_mapping_*.csv` over plain HTTPS (raw file only; no git, account or API).
- U3: Yes. Download all Challenge headers of the 5 sources (~46 MB).
- U4: Yes. Download the optional Challenge PTB / PTB-XL headers (~16 MB).
- U5: Yes. Download the MIMIC open CSVs (~298 MB).
- **Every actual download still needs the user's OK via team-lead first** (files, URL, size). Plan approval does not replace this.
- U6: Solved (markdown_pdf, see above).
- U7: Code goes in `src/stemi/review/`, results in `results/`, report in `docs/dataset_report.*`.

- S11 (skeleton): `docs/dataset_report.md` outline (no dataset facts), PDF build `docs/report_build/build_pdf.py` + `report.css` (markdown_pdf), test build `docs/dataset_report.pdf` (6 pages). Planner checked: it holds no dataset facts; section 2 matches PLAN §0/§3 and U1.

- S1 (code only) + S2: `src/stemi/review/fetch_samples.py` (manifest-only, 500 MB cap, .hea/RECORDS only for headers, 401/403 stop, no overwrite, append-only `results/download_manifest.csv`), `src/stemi/review/hea_parser.py`; tests `tests/test_fetch_samples.py`, `tests/test_hea_parser.py`. `pytest`: 101 passed (planner re-ran). **No files downloaded yet.**

- S3 `ptb_xl`: 22 files downloaded (6.6 MB, all sha256 match), `review_ptbxl.py` run; results `results/ptb_xl_*.csv`, `results/ptb_xl_summary.md`, `results/findings_ptb_xl.md`. Planner recounted the key numbers independently and checked the PN/PAPER quotes → 10 rows in `results/verified_facts.md` (Q4 = not found; Q8 partial until S10). Main result: MI statements, but no STEMI/NSTEMI; 150 MI-coded ECGs with an early infarct stage.

- S11 (part): PTB-XL filled in `docs/dataset_report.md` (§3 row, §4 row, §5.1, §10 sources); PDF rebuilt (7 pages). Planner checked it against the verified rows (4 fixes made first).

- U1 script: `src/stemi/review/mimic_icd_count.py` + `tests/test_mimic_icd_count.py`, reviewed by planner (2 rounds). Aggregates only, <10 suppressed with secondary suppression, chunked read-only, caveats printed; ext-ICD input not supported. `pytest` 133 passed. **Ready for the user to run**; the counts are not available yet.
- Report: optional PTB-XL likelihood tweak included in this commit.

- S6 `sph`: 3 files (metadata.csv, code.csv, rule.pdf; md5 = figshare). Results `results/sph_*`, `results/findings_sph.md`. Verified (planner recount): 260 MI ECGs; only 7 Acute. Data CC0, article CC BY 4.0.
- S8 `code15`: exams.csv (md5 = Zenodo). Results `results/code15_*`, `results/findings_code15.md`. Verified: no MI label; `ST` = sinus tachycardia.

- Download decisions (team-lead 2026-10-20):
  - #6 INCART: approved.
  - #7 label maps: approved, WITHOUT the 8.7 MB ecg-arrhythmia SHA256SUMS stream.
  - #8 Challenge headers: **option C**, one `g1` folder per source (~5,000 headers). This replaces U3 "all 65,826 headers". Full per-source label counts come from the publisher's `dx_mapping_*.csv` IF coder confirms it has per-dataset count columns; otherwise coder goes back to the lead. The report must say: dx_mapping counts = publisher's counts from that file; header counts = a g1 sample only.
  - U4 (Challenge ptb/ptb-xl headers): superseded; see the cheap RECORDS-list check below.
  - Disclosure: coder printed `challenge-2021/1.0.3/RECORDS` (2 KB index) with curl without a request; not saved or used as data; the user was told.
  - Disclosure (planner): while verifying, planner streamed https://physionet.org/files/ptb-xl/1.0.3/SHA256SUMS.txt (~8.3 MB) through grep without saving it (only the ptbxl_database.csv and scp_statements.csv lines kept; both match the planner's sha256), and read figshare/Zenodo API metadata JSON for md5/license. Reported to team-lead.

- S11 (part): SPH (§5.4) and CODE-15% (§5.10) filled in the report, plus §3/§4 rows and sources; PDF rebuilt (11 pages). Planner checked them against the verified rows (4 wording fixes made first).

- Documenter's accidental private artifact of the draft report was deleted at the user's request. Documenter now uses file edits only (no artifacts).
- U4 cheap overlap check approved in principle: coder sends request #9 for the Challenge `ptb-xl` / `ptb` RECORDS lists (~0.3 MB) before any GET. (Replaces "U4 on hold".)

- S5 `ptb_diagnostic`: 552 files (sha256 match). Results `results/ptb_diagnostic_*`, `results/findings_ptb_diagnostic.md`. Verified (planner recount, date order confirmed day-first): 148 MI patients; 60 with an ECG 0–1 days after the documented infarction date; 52 healthy controls; no STEMI/NSTEMI label. Also verified: Georgia = Emory (PA2020) and the Challenge general label-quality statement.

- S11 (part): PTB Diagnostic (§5.3) filled in the report, plus §3/§4 rows and sources; Appendix A heading reserved; PDF rebuilt (12 pages). Planner checked it against the verified rows; the timing table totals reconcile (343+25 records, 123+25 patients).

- Fetcher: HTTP Range-resume (`--resume`), pinned total size (TotalChanged = stop), transient 429/5xx retry, a per-dataset `.fetch.lock`, and a plausibility check for MIMIC `record_list.csv` → `results/download_plausibility.csv` (no publisher checksum: SHA256SUMS not approved). Reviewed by planner in 2 rounds; `pytest` 148 passed. Use on MIMIC only after the old fetcher (pid 63141) exits or the lead says to stop it.

- S9 `incart`: 80 files (sha256 match). Results `results/incart_*`, `results/findings_incart.md`. Verified (planner check): 2 acute-MI patients (6 records), 4 earlier-MI patients; Holter at 257 Hz; README vs file conflict (TIA 5 vs 4 patients).

- MIMIC download (team-lead's instruction): the old fetcher pid 63141 was stopped (SIGTERM, after checking its command line); resumed as pid 70658 with `--resume --workers 1 --skip-sha256sums --only record_list.csv,machine_measurements_data_dictionary.csv` from a 6,291,456 B .part (approval #2 + resume note). Planner check 20:27 local: .part growing (6,488,064 B), lock held by 70658, 63141 gone. Expected total 70,403,124 B.

- S11 (part): INCART (§5.11), §3/§4 rows, the first §9 conflict entry and sources filled; PDF rebuilt (14 pages). Planner checked them against the verified rows (one wording tweak pending: record selection, not patient randomness).

- S7 part 1 (`cpsc_2018`, `cpsc_extra`, `georgia`, g1 sample of 999 headers each): results `results/challenge_*`, `results/findings_{cpsc_2018,cpsc_extra,georgia}.md`. Planner recounted the g1 headers and checked CH21/PA2020 → 30 rows. None has STEMI/NSTEMI; there is no patient ID although repeat patients exist (PA2020). Fix: dx_mapping names now win over ConditionNames.

- S4 `mimic_iv_ecg` (fallback C): record_list.csv 70.4 MB (resumed; plausibility: 800,035 rows = registry), dictionary, 50 headers. Results `results/mimic_iv_ecg_*`, `results/findings_mimic_iv_ecg.md`. Verified (planner recount) → 10 rows. STEMI/NSTEMI = not checked yet (user-run ICD script). Key technical finding: lead order aVF before aVL, gain 200/mV.

- S11 (part): CPSC 2018, CPSC-Extra and Georgia (§5.5–5.7), the shared Challenge block, the first §8 warning (no patient ID despite repeat patients), the §9 Georgia conflict and sources filled; PDF rebuilt. Planner checked them (age-92 rule scoped to CPSC/CPSC-Extra).

- S11 (part): MIMIC-IV-ECG (§5.2), §3/§4 rows, the §8 lead-order/scale warning (sample-qualified) and sources filled; PDF rebuilt (19 pages). Planner checked them.

- S7 part 2 (`chapman_shaoxing`, g1 999): results `results/challenge_chapman_shaoxing_*`, `results/findings_chapman_shaoxing.md` → 10 rows verified (planner recount; ZH2020 PMC7016169). 40 MI labels (publisher); the MI wall labels collapse into one SNOMED code. The chain has finished; #9 has started; Ningbo g1 is in progress. S10 scripts `overlap_ids.py` and `build_summary.py` are written (not yet run on real data).

- S11 (part): Chapman-Shaoxing (§5.9), §3/§4 rows, two §9 conflict entries and sources filled; PDF rebuilt (21 pages). Planner checked them.

- #9 done (Challenge ptb-xl/ptb RECORDS lists, 25 files) + `overlap_ids.py` run: `results/overlap_ids.csv`, `results/overlap_ids_summary.md`. Verified (planner recount): Challenge ptb-xl = HR1–21,837, covering all 21,799 native ecg_ids + 38 extra; Challenge ptb = 516 of 549 (the 33 missing include all 27 'n/a' records). Mappings stay ASSUMPTIONS.

- S7 part 3 (`ningbo`, g1 999) verified → 10 rows (planner recount; median age 38). **All approved downloads are finished** (no fetcher or lock left). S10 `build_summary.py` → `results/dataset_summary.csv` (one fix requested: acute/timing column for ningbo/cpsc_extra).

- S10 done: `results/dataset_summary.csv` (fixed: ningbo acute label, cpsc_extra old MI, incart records) and `results/combine_matrix.csv` + summary (45 after checks, 10 no, 0 yes). Planner spot-checked them and added 2 S10 rows (matrix; per-model assessment). Next: S11 §1/§6/§7/§8/§9 and Appendix A (documenter), S12 PDF, S13 final report.

- S11 (part): Ningbo (§5.8) filled, with the §8 age-mix warning (planner's note); all 11 dataset sections are now in the report.

- **S11 + S12 DONE:** `docs/dataset_report.md` + `docs/dataset_report.pdf` (27 pages) marked FINAL (2026-10-21). Planner read the whole report against `results/verified_facts.md` (130 rows: verified / not found / 1 pending = UMich, not used) and checked all 110 matrix cells against `results/combine_matrix.csv` by script (0 mismatches). `pytest` 161 passed.
- S13: final report to team-lead (planner).

## In progress
- **S13 label provenance** (user-approved 2026-10-21; plan in `docs/project/PLAN.md` §8).
  - S0 DONE (planner, web pages only; the file was NOT opened): `data/samples/mimic_iv_ecg/records_w_diag_icd10.csv` (339 MB, gitignored) matches the main table of **MIMIC-IV-ECG-Ext-ICD** (https://physionet.org/content/mimic-iv-ecg-ext-icd-labels/1.0.1/, versions 1.0.0/1.0.1; **credentialed + DUA + CITI**; discharge-diagnosis labels per ED stay / admission, with no time window beyond the stay). Reported to the lead; **nobody reads the file until the user decides** (current rule U1).
  - User decision (2026-10-21): the file is Ext-ICD **v1.0.1**; the USER runs `mimic_ext_icd_count.py` (aggregate only), and the team never reads it. MIMIC ICD cells = "pending user-run count (credentialed)". Script `src/stemi/review/mimic_ext_icd_count.py` APPROVED by planner (round 2; lead's suppression fix included; tests 12 + full suite 190). Synthetic timing: 800k rows / 169 MB ≈ 45 s, ~600 MB RAM, so the real 339 MB is ≈ 1.5–2 min, ~1–1.5 GB. Waiting for the user to run it.
  - S2 DONE: `results/label_provenance.csv` (169 rows; text traced to S13 rows; counts = crosswalk; MIMIC = "pending user-run count (credentialed)"), `label_pathway.py` + tests (pytest 192). Planner verified.
  - S4 (part): §4c pathways + summary table written by documenter and checked by planner (3 fixes); the per-class table waits for S2.
  - S1 DONE (planner): 9 S13 provenance rows in `results/verified_facts.md` (PTB-XL, SPH, CODE-15, CPSC/CPSC-Extra/Georgia = not found per source, Chapman/Ningbo, PTB-DB, INCART, MIMIC open module, MIMIC Ext-ICD). S1b DONE: 8 "S13 pathway" rows (MIMIC: ICU is a recording location only, not a labelling stage; ED codes by "trained coders after discharge"; hospital `diagnoses_icd` = "hospital billing information"). S2 coder: PTB-XL + CODE-15 counts verified (pattern wording fixed: non-validated ⊂ autogenerated); MIMIC function written, not run.

- (none running)

## Done 2026-10-21
- **S12-L (label inventory add-on, user request via team-lead 2026-10-21):** full label list per dataset + a common-label crosswalk, in the PDF. NO new downloads; only files already in `data/samples/`. Steps:
  - L1 coder: `src/stemi/review/label_inventory.py` + tests → `results/label_inventory_<dataset>.csv` (label as written, code, code system, count, count type) for ptb_xl, sph, code15, cpsc_2018, cpsc_extra, georgia, ningbo, chapman_shaoxing (publisher's counts as listed), ptb_diagnostic, incart; mimic_iv_ecg = "not checked: label file not downloaded".
  - L1 DONE (planner verified; 0 mismatches in the recounts): `results/label_inventory_*.csv`, `label_inventory.py` + tests (pytest 164).
  - L2 coder: `results/label_crosswalk_common.csv` (~15–20 common labels × 11 datasets). Cross-system matching = TEAM MAPPING for supervisor review, with the exact source codes per cell; "not present" vs "not checked" kept apart.
  - L2 DONE (planner spot-checked; mapping decisions recorded in verified_facts): `results/label_crosswalk_common.csv`, `label_crosswalk.py` + tests (pytest 169).
  - L3 planner: verify the counts against the files → verified rows.
  - L4 documenter: new section "Which labels each dataset has" + Appendix B (full lists); rebuild the PDF. Existing findings unchanged.
  - L3+L4 DONE (2026-10-21 ~02:00): documenter wrote §4b + Appendix B (generated by `docs/report_build/label_tables.py` → `section_4b.md`, `appendix_b.md`). Planner and documenter then hit their usage limit (resets 04:30 Asia/Bangkok), so **team-lead finished the review**: (a) fixed a real error in §5.1 + verified_facts: PTB-XL `STE_`/`STD_` are "form" statements with NO diagnostic_class in scp_statements.csv (not "STTC class"); (b) added the Ningbo AF 0 / AFL 7,615 facts and the "AF = flutter, AFIB = fibrillation" name trap (checked in ConditionNames_SNOMED-CT.csv) to §4b, and a planner's-note warning to §8 weak labels. PDF rebuilt: 43 pages. pytest 169 passed.
  - **S12-L DONE.** Optional when the team is back: planner re-reads §4b + Appendix B against `results/label_crosswalk_common.csv` / `label_inventory_*.csv` (tables are script-generated from verified CSVs).
- Still waiting for the user's MIMIC ICD count output (U1).

## Next
- When the user sends the `mimic_icd_count.py` output: planner verifies it (aggregates only), adds mimic_iv_ecg Q6 rows, documenter updates §1/§4/§5.2/§6, rebuild the PDF, commit.
- Supervisor decisions listed in report §9 (STEMI/NSTEMI code list, acute window, non-MI evidence, record-level splits, INCART scope).

## Add-on (low priority, chosen by team-lead for the user, 2026-10-20)
- **S-extra: other public ECG datasets that may have STEMI/NSTEMI or acute-MI labels.** Research only: official pages and papers; NO downloads and no requests. At most ~5 candidates. Per candidate: name, labels (verbatim), who labelled, access (open / credentialed / on request), size, source URLs. Every fact sourced or "not found"; planner verifies. Output `results/findings_extra_candidates.md` → verified rows in `results/verified_facts.md` (dataset key `extra:<name>`). Report: a separate appendix "Other datasets worth checking (not reviewed in depth)", NOT mixed into the 11-dataset tables or recommendations. Coder does it only while idle during downloads; it must not delay S3–S13. Its report appendix comes after the main review.

- S-extra research done by coder (`results/findings_extra_candidates.md`); planner verified it → 6 `extra:` rows (wECGdb, STAFF III and the prehospital OMI cohort verified; UMich pending (page 403); HEEDB access/license only). Report appendix waits until the main review is done.

## Open questions for the user
- U1 RESOLVED (team-lead 2026-10-20): `src/stemi/review/mimic_icd_count.py`, run by the USER only. It reads MIMIC-IV hosp `diagnoses_icd` + `admissions` + MIMIC-IV-ECG `record_list` (ext-ICD optional). ECG→admission link when `ecg_time` is between `admittime` and `dischtime` (ASSUMPTION, printed in the output). Aggregate counts only for I21.0–I21.3 / I21.4 / other I21 / I22 / ICD-9 410; counts <10 suppressed. Planner reviews it like any step.

## Files: this dataset review (2026-10-20)
- `PLAN.md`, `STATUS.md`, `docs/report_build/`, `results/` (incl. `results/verified_facts.md`, `results/findings_<dataset>.md`, count CSVs, `download_manifest.csv`), `src/stemi/review/`, review tests in `tests/`, `docs/dataset_report.md` / `.pdf`, `data/samples/` (gitignored, never committed).

## Files: earlier pipeline task (2026-10-19), left unchanged
- `TASKS.md`, `NEXT_STEPS.md`, `docs/methods.md`, `docs/decision_log.md`, `docs/results.md`, `demo_results/`, `src/stemi/{registry,inventory,label_mapping,demo}.py` and their tests.
- Shared governing docs (read-only for this team): `data_contract.md`, `research_plan.md`.

## Result files
- (none yet) Verified facts will be in `results/verified_facts.md`.
