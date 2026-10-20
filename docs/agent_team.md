# How this review was made

The review was carried out with an AI agent team in Claude Code. The researcher set the goal and the rules, and approved the plan, every download, every install and every scope change.

## Roles

| Role | Job | Could not |
|---|---|---|
| **Lead** | Passed messages between the researcher and the team, asked for every approval, spot-checked results | Approve anything on the researcher's behalf |
| **Planner (checker)** | Wrote the plan (`docs/project/PLAN.md`), checked every finding against its source, kept `STATUS.md` and made the git commits | Write code or the report |
| **Coder** | Wrote the scripts in `src/stemi/review/` and their tests, downloaded approved metadata samples, counted labels, leads, rates and patients | Download anything without the researcher's explicit yes |
| **Documenter** | Wrote `docs/dataset_report.md` and built the PDF in plain English | Use any fact the planner had not marked verified |

## Rules the team worked under

- **Every fact needs a source:** a PDF page, an official dataset page, a paper, or a count reproduced from downloaded files. Unknown facts are written as "not found", together with where the team looked.
- **Verification before use:** the planner re-checked each finding (recounting numbers from the files and re-reading quotes on the pages) before adding it to `results/verified_facts.md`. Only verified rows reach the report.
- **Downloads:** metadata and header files only, at most 500 MB per dataset, each one approved by the researcher with the exact files, URL and size. Never ECG waveforms. Every download is logged with its checksum and approval text in `results/download_manifest.csv`.
- **No credentials:** the team never logged in to any service, accepted any data use agreement or handled credentialed data. The MIMIC-IV ICD count script is for the researcher to run on their own credentialed files.
- **Assumptions are flagged:** anything marked ASSUMPTION or BG-UNCONFIRMED in the data contract went to the researcher as a question, not decided by the team.
- **Saved progress:** after every finished step the planner updated `STATUS.md` and made a git commit, so work could resume after an interruption.

## What the checking caught

Examples of errors found and fixed before they reached the report:

- An ambiguous date format in PTB Diagnostic headers, resolved as day-first from the data (374 of 541 dates have a first number above 12).
- A rule about ages over 89 that the source states for only two of the five Challenge datasets.
- Misquoted wording from the INCART README, and ST-elevation mentions in 4 records rather than 1.
- PTB-XL "non-specific ST elevation/depression" codes wrongly described as belonging to the ST/T diagnostic class.
- A wrong claim that MIMIC-IV-ECG and PTB-XL cannot share patients "because they are from different countries" (PTB-XL's country is not stated).

The full history of the work, including every check and correction, is in the git log.
