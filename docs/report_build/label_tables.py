"""Build the Markdown for report section 4b and Appendix B from the label CSVs in results/.

Usage: python3 docs/report_build/label_tables.py
Writes docs/report_build/section_4b.md and docs/report_build/appendix_b.md.
Only reads results/label_crosswalk_common.csv and results/label_inventory_<dataset>.csv.
"""

import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"
OUT = pathlib.Path(__file__).resolve().parent

ORDER = ["ptb_xl", "mimic_iv_ecg", "ptb_diagnostic", "sph", "cpsc_2018", "cpsc_extra",
         "georgia", "ningbo", "chapman_shaoxing", "code15", "incart"]
SHORT = {"ptb_xl": "PTB-XL", "mimic_iv_ecg": "MIMIC", "ptb_diagnostic": "PTB-Diag", "sph": "SPH",
         "cpsc_2018": "CPSC", "cpsc_extra": "CPSC-Ex", "georgia": "Georgia", "ningbo": "Ningbo",
         "chapman_shaoxing": "Chapman", "code15": "CODE-15", "incart": "INCART"}
CHALLENGE = ["cpsc_2018", "cpsc_extra", "georgia", "ningbo", "chapman_shaoxing"]

# Plain-language glosses: simple, non-numeric, no diagnostic criteria.
GLOSS = {
    "Normal ECG": "Normal ECG (the ECG shows no problem)",
    "Sinus rhythm": "Sinus rhythm (the normal heartbeat, started by the heart's own pacemaker)",
    "Sinus bradycardia": "Sinus bradycardia (a slow heartbeat that starts in the heart's normal pacemaker)",
    "Sinus tachycardia": "Sinus tachycardia (a fast heartbeat that starts in the heart's normal pacemaker)",
    "Atrial fibrillation": "Atrial fibrillation (the upper heart chambers beat in a fast, irregular, chaotic way)",
    "Atrial flutter": "Atrial flutter (the upper heart chambers beat fast in a regular, circling pattern)",
    "1st-degree AV block": "1st-degree AV block (the signal from the upper to the lower heart chambers is slowed)",
    "LBBB": "LBBB (left bundle branch block: a delay in the heart's electrical wiring on the left side)",
    "RBBB (complete)": "RBBB, complete (right bundle branch block: a delay in the heart's electrical wiring on the right side)",
    "RBBB (incomplete)": "RBBB, incomplete (a partial delay in the wiring on the right side)",
    "LAFB": "LAFB (left anterior fascicular block: a delay in one front branch of the left-side wiring)",
    "PAC (atrial premature)": "PAC (premature atrial contraction: an extra, early beat from the upper chambers)",
    "PVC (ventricular premature)": "PVC (premature ventricular contraction: an extra, early beat from the lower chambers)",
    "LVH": "LVH (left ventricular hypertrophy: the wall of the main pumping chamber is thickened)",
    "Long QT": "Long QT (the heart takes longer than usual to recharge between beats)",
    "MI (any)": "MI, any (any heart-attack label, new or old)",
    "Old MI": "Old MI (a heart attack in the past)",
    "ST elevation": "ST elevation (the ST segment of the ECG wave is raised)",
    "ST depression": "ST depression (the ST segment of the ECG wave is lowered)",
    "Ischaemia (any)": "Ischaemia, any (low blood flow to the heart muscle)",
    "T-wave abnormality": "T-wave abnormality (the T wave, the last part of each beat on the ECG, has an unusual shape)",
}


def fmt(v):
    v = v.strip()
    if v.isdigit():
        return f"{int(v):,}"
    return v


def read_csv(path):
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if not ln.startswith("#")]
    return list(csv.DictReader(lines))


def section_4b():
    rows = read_csv(RESULTS / "label_crosswalk_common.csv")
    assert [r["label"] for r in rows] == list(GLOSS), [r["label"] for r in rows]
    out = ["| Label (plain English) | " + " | ".join(SHORT[d] for d in ORDER) + " |",
           "|---" * (len(ORDER) + 1) + "|"]
    for r in rows:
        out.append("| " + GLOSS[r["label"]] + " | " + " | ".join(fmt(r[d]) for d in ORDER) + " |")
    return "\n".join(out)


def esc(text):
    return text.replace("|", "\\|").strip()


def code(text):
    return f"`{text}`" if text else "–"


def table(header, body):
    out = ["| " + " | ".join(header) + " |", "|---" * len(header) + "|"]
    out += ["| " + " | ".join(row) + " |" for row in body]
    return "\n".join(out)


def by_count(rows):
    return sorted(rows, key=lambda r: (-int(r["count"]), r["label_as_written"].lower()))


def appendix_b():
    parts = []
    titles = {"ptb_xl": "B.1 PTB-XL", "mimic_iv_ecg": "B.2 MIMIC-IV-ECG", "ptb_diagnostic": "B.3 PTB Diagnostic",
              "sph": "B.4 SPH", "cpsc_2018": "B.5 CPSC 2018", "cpsc_extra": "B.6 CPSC-Extra",
              "georgia": "B.7 Georgia", "ningbo": "B.8 Ningbo", "chapman_shaoxing": "B.9 Chapman-Shaoxing",
              "code15": "B.10 CODE-15%", "incart": "B.11 INCART"}
    for ds in ["ptb_xl", "mimic_iv_ecg", "ptb_diagnostic", "sph", "cpsc_2018", "cpsc_extra",
               "georgia", "ningbo", "chapman_shaoxing", "code15", "incart"]:
        rows = read_csv(RESULTS / f"label_inventory_{ds}.csv")
        parts.append(f"### {titles[ds]}\n")
        if ds == "ptb_xl":
            parts.append(f"All {len(rows)} SCP-ECG statements. Count = ECGs with the code at any likelihood. "
                         "Class = the diagnostic class in `scp_statements.csv` (blank for shape and rhythm codes) [INV].\n")
            body = []
            for r in by_count(rows):
                cls = r["extra"].split(";")[0].replace("diagnostic_class=", "")
                kind = r["label_kind"].replace("SCP statement (", "").rstrip(")")
                body.append([esc(r["label_as_written"]), code(r["code"]), kind,
                             "" if cls == "nan" else cls, fmt(r["count"])])
            parts.append(table(["Label as written", "Code", "Kind", "Class", "ECGs"], body))
        elif ds == "mimic_iv_ecg":
            parts.append("Not checked: label file not downloaded. The machine report file was not approved for "
                         "download, and the diagnosis codes need credentialed access [INV].")
        elif ds == "ptb_diagnostic":
            parts.append("Free text from the header comments, exactly as written (spelling kept). "
                         "Count = records; patients in the last column [INV].\n")
            for kind, name in [("header comment: Reason for admission", "Reason for admission"),
                               ("header comment: Acute infarction (localization)", "Acute infarction (localization)"),
                               ("header comment: Former infarction (localization)", "Former infarction (localization)")]:
                sub = by_count([r for r in rows if r["label_kind"] == kind])
                parts.append(f"**{name}**\n")
                parts.append(table(["Text as written", "Records", "Patients"],
                                   [[esc(r["label_as_written"]), fmt(r["count"]), fmt(r["n_patients"])] for r in sub]))
                parts.append("")
        elif ds == "sph":
            parts.append("AHA statement codes. Count = ECG records; patients in the last column [INV].\n")
            prim = by_count([r for r in rows if r["label_kind"] == "AHA primary statement"])
            parts.append(f"**Main codes ({len(prim)})**\n")
            parts.append(table(["Label as written", "Code", "ECGs", "Patients"],
                               [[esc(r["label_as_written"]), code(r["code"]), fmt(r["count"]), fmt(r["n_patients"])]
                                for r in prim]))
            pairs = by_count([r for r in rows if r["label_kind"] == "AHA statement + modifier"])
            parts.append(f"\n**Main code + add-on code pairs ({len(pairs)})**\n")
            parts.append(table(["Label as written", "Code", "ECGs", "Patients"],
                               [[esc(r["label_as_written"]), code(r["code"]), fmt(r["count"]), fmt(r["n_patients"])]
                                for r in pairs]))
        elif ds in CHALLENGE:
            listed = [r for r in rows if int(r["count"]) > 0]
            zero = len(rows) - len(listed)
            parts.append(f"SNOMED CT codes from the Challenge label files. Count = publisher's count as listed "
                         f"(what it counts is not defined by the publisher). Only the {len(listed)} codes with a "
                         f"count above 0 are shown; {zero} listed codes with count 0 are left out [INV; DXMAP].\n")
            parts.append(table(["Label as written", "SNOMED code", "Publisher's count"],
                               [[esc(r["label_as_written"]), code(r["code"]), fmt(r["count"])]
                                for r in by_count(listed)]))
        elif ds == "code15":
            parts.append("Yes/no columns in `exams.csv`. Count = exams marked \"yes\"; patients in the last column. "
                         "`ST` means sinus tachycardia, and `normal_ecg` comes from an automatic system [INV; ZEN-CODE15].\n")
            body = []
            for r in by_count(rows):
                meaning = r["extra"].split(": ", 1)[1] if ": " in r["extra"] else ""
                body.append([code(r["label_as_written"]), esc(meaning), fmt(r["count"]), fmt(r["n_patients"])])
            parts.append(table(["Column", "Meaning (from the dataset page)", "Exams", "Patients"], body))
        elif ds == "incart":
            parts.append("Free text, exactly as written (spelling kept). Count = records [INV].\n")
            for kind, name, with_pat in [
                    ("patient diagnosis (raw text)", "Patient diagnosis text", True),
                    ("patient diagnosis term (raw text split on commas)", "Patient diagnosis terms (text split at commas)", True),
                    ("record description term", "Record description terms", False)]:
                sub = by_count([r for r in rows if r["label_kind"] == kind])
                parts.append(f"**{name}**\n")
                if with_pat:
                    parts.append(table(["Text as written", "Records", "Patients"],
                                       [[esc(r["label_as_written"]), fmt(r["count"]),
                                         fmt(r["n_patients"].split(".")[0])] for r in sub]))
                else:
                    parts.append(table(["Text as written", "Records"],
                                       [[esc(r["label_as_written"]), fmt(r["count"])] for r in sub]))
                parts.append("")
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def provenance_tables():
    """Per-class tables for section 4c from results/label_provenance.csv."""
    rows = read_csv(RESULTS / "label_provenance.csv")
    by_ds = {}
    for r in rows:
        by_ds.setdefault(r["dataset"], []).append(r)
    out = []

    def simple(ds, title, stage, count_head, extra_note=""):
        out.append(f"**{title}** (our file: {stage}){extra_note}\n")
        out.append(table(["Class", "Source code(s)", count_head],
                         [[r["class"], code(esc(r["source_codes"])), fmt(r["count"])] for r in by_ds[ds]]))
        out.append("")

    out.append("**PTB-XL** (our file: SCP codes converted from the report text). Count = ECGs. "
               "\"Checked by a person\" = `validated_by_human`; \"Machine first report\" = `initial_autogenerated_report` [LPROV].\n")
    out.append(table(["Class", "Source code(s)", "ECGs", "Checked by a person", "Machine first report"],
                     [[r["class"], code(esc(r["source_codes"])), fmt(r["count"]),
                       fmt(r["human_validated_n"]), fmt(r["autogenerated_n"])] for r in by_ds["ptb_xl"]]))
    out.append("")
    simple("sph", "SPH", "AHA codes after translation", "ECGs")
    simple("ptb_diagnostic", "PTB Diagnostic", "header clinical summary", "Records")
    out.append("**CODE-15%** (our file: study labels in `exams.csv`). Count = exams. "
               "Exception: `normal_ecg` is set by an automatic system; the other columns come from the report-based method [LPROV].\n")
    out.append(table(["Class", "Source column", "Exams", "Made by"],
                     [[r["class"], code(esc(r["source_codes"])), fmt(r["count"]),
                       "automatic system" if r["source_codes"] == "normal_ecg" else "report-based method (full CODE)"]
                      for r in by_ds["code15"]]))
    out.append("")
    out.append("**INCART** (count = records). Exception: some classes come from the **record descriptions** "
               "(author not found), others from the **patient diagnoses** (made after a clinical work-up; "
               "who made them: not found) [LPROV].\n")
    out.append(table(["Class", "Source text", "Records", "Our file"],
                     [[r["class"], esc(r["source_codes"]), fmt(r["count"]),
                       "record descriptions" if "record-descriptions" in r["pathway_stage_of_our_file"] else "patient diagnoses"]
                      for r in by_ds["incart"]]))
    out.append("")
    out.append("**The five Challenge datasets** (our file: the 2021 Challenge SNOMED mapping). "
               "Count = publisher's count as listed; sums of several codes may count one recording twice [LPROV].\n")
    classes = [r["class"] for r in by_ds["cpsc_2018"]]
    lookup = {(r["dataset"], r["class"]): r for r in rows}
    out.append(table(["Class", "SNOMED code(s)"] + [SHORT[d] for d in CHALLENGE],
                     [[c, code(esc(lookup[("cpsc_2018", c)]["source_codes"]))] +
                      [fmt(lookup[(d, c)]["count"]) for d in CHALLENGE] for c in classes]))
    out.append("")
    out.append("**MIMIC-IV-ECG** (our file: none opened). The ICD code groups are the team's assumption "
               "(marked ASSUMPTION) and need the supervisor's sign-off (section 9) [LPROV].\n")
    out.append(table(["Class (as named in our results table)", "Source", "Count"],
                     [[esc(r["class"]), code(esc(r["source_codes"])), r["count"]] for r in by_ds["mimic_iv_ecg"]]))
    return "\n".join(out).rstrip() + "\n"


if __name__ == "__main__":
    (OUT / "section_4b.md").write_text(section_4b() + "\n", encoding="utf-8")
    (OUT / "appendix_b.md").write_text(appendix_b(), encoding="utf-8")
    (OUT / "section_4c_classes.md").write_text(provenance_tables(), encoding="utf-8")
    print("wrote section_4b.md, appendix_b.md and section_4c_classes.md")
