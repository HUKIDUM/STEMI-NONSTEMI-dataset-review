"""Build docs/dataset_report.pdf from docs/dataset_report.md with markdown_pdf.

The Markdown is split into PDF sections at lines of the form
``<!-- section: A4 -->`` or ``<!-- section: A4-L -->`` (A4-L = landscape, for wide tables).
Text before the first marker goes into a portrait section.

Usage: .venv/bin/python docs/report_build/build_pdf.py
"""

import pathlib
import re

from markdown_pdf import MarkdownPdf, Section

DOCS = pathlib.Path(__file__).resolve().parent.parent
SRC = DOCS / "dataset_report.md"
OUT = DOCS / "dataset_report.pdf"
CSS = (pathlib.Path(__file__).resolve().parent / "report.css").read_text(encoding="utf-8")

MARKER = re.compile(r"^<!-- section: (A4|A4-L) -->\s*$", re.MULTILINE)


def split_sections(text):
    """Return a list of (paper_size, markdown) pairs."""
    parts = MARKER.split(text)
    sections = [("A4", parts[0])]
    for i in range(1, len(parts), 2):
        sections.append((parts[i], parts[i + 1]))
    return [(size, md) for size, md in sections if md.strip()]


def main():
    pdf = MarkdownPdf(toc_level=2)
    for size, md in split_sections(SRC.read_text(encoding="utf-8")):
        pdf.add_section(Section(md, paper_size=size), user_css=CSS)
    pdf.meta["title"] = "ECG Datasets for STEMI and NSTEMI Prediction: A Simple Review"
    pdf.meta["author"] = "documenter (dataset review team)"
    pdf.save(OUT)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
