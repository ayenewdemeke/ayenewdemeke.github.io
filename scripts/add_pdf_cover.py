"""Prepend a cover page (title, authors, venue, license/notice lines) to an accepted-manuscript PDF.

Usage:
  python scripts/add_pdf_cover.py SRC.pdf files/DEST.pdf \
      --title "Paper title" --authors "A. Author, B. Author" --venue "Journal, vol, article (year)" \
      --meta-authors "A. Author; B. Author" \
      --line "Author accepted manuscript. ..." --line "(c) 2026. This manuscript version ..."

Lines may contain simple ReportLab markup (<b>, <i>, <a href="..." color="blue">).
Requires: pip install pypdf reportlab (use a venv outside the repo).
"""
import argparse, io
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("dest")
ap.add_argument("--title", required=True); ap.add_argument("--authors", required=True)
ap.add_argument("--venue", required=True); ap.add_argument("--meta-authors", required=True)
ap.add_argument("--line", action="append", default=[])
a = ap.parse_args()

ss = getSampleStyleSheet()
buf = io.BytesIO()
story = [Paragraph(a.title, ss["Title"]), Paragraph(f"{a.authors}<br/><i>{a.venue}</i>", ss["Normal"]), Spacer(1, 24)]
for line in a.line:
    story += [Paragraph(line, ss["BodyText"]), Spacer(1, 10)]
SimpleDocTemplate(buf, pagesize=letter, leftMargin=72, rightMargin=72, topMargin=90).build(story)

w = PdfWriter()
for p in list(PdfReader(buf).pages) + list(PdfReader(a.src).pages):
    w.add_page(p)
w.add_metadata({"/Title": a.title, "/Author": a.meta_authors})
with open(a.dest, "wb") as f:
    w.write(f)
print("wrote", a.dest)
