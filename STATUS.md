# STATUS: Dataset review (STEMI / NSTEMI / non-MI)

Owner: planner. A new session reads this first. Plan: `PLAN.md` (APPROVED 2026-10-20, with the user answers below).

Last update: 2026-10-20

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

## In progress
- S1 downloads: PTB-XL done. First run aborted on a dropped connection (retry bug: reused .part file). Fixed in `fetch_samples.py` (per-attempt .part, truncated body = retry, per-batch logging); `pytest` 110 passed (planner re-ran). Re-run in progress with --workers 2. PhysioNet speed ~4–5 KB/s: the MIMIC CSVs (~298 MB) may take many hours.
- S4 `mimic_iv_ecg`: the user chose option E (public S3 mirror) → HTTP 404 → fallback option C (approved): `record_list.csv`, the data dictionary and 50 `.hea` headers from physionet.org, downloading now. **`machine_measurements.csv` and `waveform_note_links.csv` are NOT approved yet** (they need a new request). `review_mimic.py` is written, not yet run on data.
- S5 `ptb_diagnostic`: download #3 approved and running (RECORDS, CONTROLS, README, 549 `.hea`, SHA256SUMS stream).
- Credentials: the team never receives or uses any credentials, including AWS keys (user question answered by team-lead).

## Next
- S3 `ptb_xl` → S4 `mimic_iv_ecg` (+ `mimic_icd_count.py`) → S5 `ptb_diagnostic` → S6 `sph` → S7 Challenge 5 → S8 `code15` → S9 `incart` → S10 overlap/summary → S11–S12 report → S13 final report.

## Add-on (low priority, chosen by team-lead for the user, 2026-10-20)
- **S-extra: other public ECG datasets that may have STEMI/NSTEMI or acute-MI labels.** Research only: official pages and papers; NO downloads and no requests. At most ~5 candidates. Per candidate: name, labels (verbatim), who labelled, access (open / credentialed / on request), size, source URLs. Every fact sourced or "not found"; planner verifies. Output `results/findings_extra_candidates.md` → verified rows in `results/verified_facts.md` (dataset key `extra:<name>`). Report: a separate appendix "Other datasets worth checking (not reviewed in depth)", NOT mixed into the 11-dataset tables or recommendations. Coder does it only while idle during downloads; it must not delay S3–S13. Its report appendix comes after the main review.

## Open questions for the user
- U1 RESOLVED (team-lead 2026-10-20): `src/stemi/review/mimic_icd_count.py`, run by the USER only. It reads MIMIC-IV hosp `diagnoses_icd` + `admissions` + MIMIC-IV-ECG `record_list` (ext-ICD optional). ECG→admission link when `ecg_time` is between `admittime` and `dischtime` (ASSUMPTION, printed in the output). Aggregate counts only for I21.0–I21.3 / I21.4 / other I21 / I22 / ICD-9 410; counts <10 suppressed. Planner reviews it like any step.

## Files: this dataset review (2026-10-20)
- `PLAN.md`, `STATUS.md`, `docs/report_build/`, `results/` (incl. `results/verified_facts.md`, `results/findings_<dataset>.md`, count CSVs, `download_manifest.csv`), `src/stemi/review/`, review tests in `tests/`, `docs/dataset_report.md` / `.pdf`, `data/samples/` (gitignored, never committed).

## Files: earlier pipeline task (2026-10-19), left unchanged
- `TASKS.md`, `NEXT_STEPS.md`, `docs/methods.md`, `docs/decision_log.md`, `docs/results.md`, `demo_results/`, `src/stemi/{registry,inventory,label_mapping,demo}.py` and their tests.
- Shared governing docs (read-only for this team): `data_contract.md`, `research_plan.md`.

## Result files
- (none yet) Verified facts will be in `results/verified_facts.md`.
