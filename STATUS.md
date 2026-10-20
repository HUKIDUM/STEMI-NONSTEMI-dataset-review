# STATUS: Dataset review (STEMI / NSTEMI / non-MI)

Owner: planner. A new session reads this first. Plan: `PLAN.md` (APPROVED 2026-10-20, with the user answers below).

Last update: 2026-10-20

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

## In progress
- S1 downloads: PTB-XL done. First run aborted on a dropped connection (retry bug: reused .part file). Fixed in `fetch_samples.py` (per-attempt .part, truncated body = retry, per-batch logging); `pytest` 110 passed (planner re-ran). Re-run in progress with --workers 2. PhysioNet speed ~4–5 KB/s: the MIMIC CSVs (~298 MB) may take many hours.
- S4 `mimic_iv_ecg`: the user chose option E (public S3 mirror) → HTTP 404 → fallback option C (approved): `record_list.csv`, the data dictionary and 50 `.hea` headers from physionet.org, downloading now. **`machine_measurements.csv` and `waveform_note_links.csv` are NOT approved yet** (they need a new request). `review_mimic.py` is written, not yet run on data.
- S5 `ptb_diagnostic`: download #3 approved and running (RECORDS, CONTROLS, README, 549 `.hea`, SHA256SUMS stream).
- Credentials: the team never receives or uses any credentials, including AWS keys (user question answered by team-lead).

## Next
- S3 `ptb_xl` → S4 `mimic_iv_ecg` (+ `mimic_icd_count.py`) → S5 `ptb_diagnostic` → S6 `sph` → S7 Challenge 5 → S8 `code15` → S9 `incart` → S10 overlap/summary → S11–S12 report → S13 final report.

## Open questions for the user
- U1 RESOLVED (team-lead 2026-10-20): `src/stemi/review/mimic_icd_count.py`, run by the USER only. It reads MIMIC-IV hosp `diagnoses_icd` + `admissions` + MIMIC-IV-ECG `record_list` (ext-ICD optional). ECG→admission link when `ecg_time` is between `admittime` and `dischtime` (ASSUMPTION, printed in the output). Aggregate counts only for I21.0–I21.3 / I21.4 / other I21 / I22 / ICD-9 410; counts <10 suppressed. Planner reviews it like any step.

## Files: this dataset review (2026-10-20)
- `PLAN.md`, `STATUS.md`, `docs/report_build/`, `results/` (incl. `results/verified_facts.md`, `results/findings_<dataset>.md`, count CSVs, `download_manifest.csv`), `src/stemi/review/`, review tests in `tests/`, `docs/dataset_report.md` / `.pdf`, `data/samples/` (gitignored, never committed).

## Files: earlier pipeline task (2026-10-19), left unchanged
- `TASKS.md`, `NEXT_STEPS.md`, `docs/methods.md`, `docs/decision_log.md`, `docs/results.md`, `demo_results/`, `src/stemi/{registry,inventory,label_mapping,demo}.py` and their tests.
- Shared governing docs (read-only for this team): `data_contract.md`, `research_plan.md`.

## Result files
- (none yet) Verified facts will be in `results/verified_facts.md`.
