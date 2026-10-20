# STATUS: Dataset review (STEMI / NSTEMI / non-MI)

Owner: planner. A new session reads this first. Plan: `PLAN.md`.

Last update: 2026-10-20

## Done
- S0 (partial): `PLAN.md` drafted and sent to team-lead for user approval.

- Environment: documenter installed `markdown_pdf` 1.13.3 (+ deps pymupdf 2.0, pymupdf_layout 2.0, pymupdf4llm 2.0, markdown-it-py 4.2.0, mdurl 0.1.2) into the project `.venv` only, for building `docs/dataset_report.pdf`. Approved by the user via team-lead (as reported by documenter 2026-10-20; versions checked with `pip list`). This answers U6 (PDF engine) unless the lead says otherwise.

## In progress
- Waiting for "PLAN APPROVED" from team-lead. **No work starts before it.**

## Next
- S1 coder: `fetch_samples.py` + open metadata downloads (PLAN §3).

## Open questions for the user (PLAN §7)
- U1 MIMIC credentialed access? U2 read GitHub-hosted dx_mapping CSVs? U3 all 65,826 Challenge headers vs g1 only?
- U4 optional overlap headers? U5 MIMIC CSVs ~298 MB OK? U6 PDF engine: resolved by the markdown_pdf install (pending lead confirmation). U7 code in `src/stemi/review/`?

## Result files
- (none yet) Verified facts will be in `results/verified_facts.md`.
