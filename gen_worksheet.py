# -*- coding: utf-8 -*-
"""Companion student worksheet for the Year 8 Solving Two-Step Equations cover lesson."""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY = RGBColor(0x1E, 0x27, 0x61)
GREY = RGBColor(0x5B, 0x65, 0x77)
INK  = RGBColor(0x26, 0x2B, 0x33)
LINE_GREY = "BFC5D0"
BOX_FILL  = "ECF2FE"
NAVY_FILL = "1E2761"

doc = Document()

# ---- base style ----
normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(11)
normal.font.color.rgb = INK
normal.paragraph_format.space_after = Pt(4)

# ---- A4 portrait, 1-inch margins ----
sec = doc.sections[0]
sec.page_width  = Inches(8.27)
sec.page_height = Inches(11.69)
for m in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
    setattr(sec, m, Inches(0.8))

# ---------- helpers ----------
def shade(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), hex_fill)
    tcPr.append(sh)

def set_borders(tbl, color=LINE_GREY, sz=6):
    tblPr = tbl._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + edge)
        e.set(qn("w:val"), "single"); e.set(qn("w:sz"), str(sz))
        e.set(qn("w:space"), "0"); e.set(qn("w:color"), color)
        borders.append(e)
    tblPr.append(borders)

def no_borders(tbl):
    tblPr = tbl._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + edge); e.set(qn("w:val"), "nil"); borders.append(e)
    tblPr.append(borders)

def keep_together(tbl):
    """Stop a table row from splitting across a page break."""
    for row in tbl.rows:
        trPr = row._tr.get_or_add_trPr()
        cant = OxmlElement("w:cantSplit"); trPr.append(cant)

def cell_pad(cell, twips=80):
    tcPr = cell._tc.get_or_add_tcPr()
    mar = OxmlElement("w:tcMar")
    for edge in ("top", "left", "bottom", "right"):
        e = OxmlElement("w:" + edge); e.set(qn("w:w"), str(twips)); e.set(qn("w:type"), "dxa")
        mar.append(e)
    tcPr.append(mar)

def run(p, text, size=11, bold=False, italic=False, color=INK, font="Calibri"):
    r = p.add_run(text)
    r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
    r.font.color.rgb = color; r.font.name = font
    return r

def para(text="", size=11, bold=False, italic=False, color=INK, align=None,
         before=0, after=4, font="Calibri"):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    if align is not None: p.alignment = align
    if text: run(p, text, size, bold, italic, color, font)
    return p

def heading(text):
    p = para(text, size=14, bold=True, color=NAVY, before=10, after=4, font="Calibri")
    return p

def blank_lines(n, leader="", width_after=True):
    """n ruled lines for written answers, via a bottom-bordered empty paragraph each."""
    for _ in range(n):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(10)
        pPr = p._p.get_or_add_pPr()
        pbdr = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single"); bottom.set(qn("w:sz"), "6")
        bottom.set(qn("w:space"), "1"); bottom.set(qn("w:color"), LINE_GREY)
        pbdr.append(bottom); pPr.append(pbdr)

def working_box(height_lines=3):
    """A bordered single-cell box for showing working."""
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_borders(t)
    cell = t.cell(0, 0); cell_pad(cell, 100)
    cell.width = Inches(6.6)
    for _ in range(height_lines - 1):
        cell.add_paragraph()
    return t

# ============================================================
# HEADER BLOCK
# ============================================================
t = doc.add_table(rows=1, cols=1); t.alignment = WD_TABLE_ALIGNMENT.CENTER
no_borders(t)
hc = t.cell(0, 0); shade(hc, NAVY_FILL); cell_pad(hc, 120)
p = hc.paragraphs[0]; p.paragraph_format.space_after = Pt(2)
run(p, "Solving Two-Step Equations", size=18, bold=True,
    color=RGBColor(0xFF, 0xFF, 0xFF), font="Calibri")
p2 = hc.add_paragraph(); p2.paragraph_format.space_after = Pt(0)
run(p2, "Maths  ·  Year 8  ·  Algebra", size=11,
    color=RGBColor(0xCA, 0xDC, 0xFC), font="Calibri")

# name / class / date row
para("", after=2)
info = doc.add_table(rows=1, cols=3); info.alignment = WD_TABLE_ALIGNMENT.CENTER
no_borders(info)
for i, label in enumerate(("Name:  ____________________", "Class:  ____________", "Date:  ____________")):
    c = info.cell(0, i); cell_pad(c, 40)
    pp = c.paragraphs[0]; run(pp, label, size=11, color=INK)

para("Goal:  solve equations like 3x + 5 = 20 by undoing each step, and check your answer "
     "by substituting it back in.", size=10.5, italic=True, color=GREY, before=6, after=2)

# ============================================================
# STARTER
# ============================================================
heading("1  ·  Starter — what do you remember?")
para("Solve these in the space provided. No calculator.", size=10.5, italic=True, color=GREY, after=6)
starter = doc.add_table(rows=1, cols=2); no_borders(starter); starter.alignment = WD_TABLE_ALIGNMENT.CENTER
left = [("a)", "x + 7 = 15"), ("c)", "x − 4 = 9"), ("e)", "If y = 6, find  2y + 3")]
right = [("b)", "3x = 21"), ("d)", "Simplify  4a + 3a − 2"), ("", "")]
def starter_col(cell, items):
    cell_pad(cell, 40)
    first = True
    for tag, q in items:
        if not q: continue
        p = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        p.paragraph_format.space_after = Pt(14)
        run(p, tag + "  ", size=11, bold=True, color=NAVY)
        run(p, q + "   =  ________", size=11)
starter_col(starter.cell(0, 0), left)
starter_col(starter.cell(0, 1), right)

# ============================================================
# REMEMBER BOX (notes during teaching)
# ============================================================
heading("2  ·  Remember (fill in as your teacher explains)")
rb = doc.add_table(rows=1, cols=1); set_borders(rb, color="1E2761", sz=6); rb.alignment = WD_TABLE_ALIGNMENT.CENTER
rc = rb.cell(0, 0); shade(rc, BOX_FILL); cell_pad(rc, 110)
pp = rc.paragraphs[0]; pp.paragraph_format.space_after = Pt(6)
run(pp, "The Golden Rule:  ", size=11.5, bold=True, color=NAVY)
run(pp, "whatever you do to one side of the equation, you must do to the ____________ side.", size=11)
pp = rc.add_paragraph(); pp.paragraph_format.space_after = Pt(6)
run(pp, "Inverse operations:  ", size=11.5, bold=True, color=NAVY)
run(pp, "+ undoes ____    − undoes ____    × undoes ____    ÷ undoes ____", size=11)
pp = rc.add_paragraph(); pp.paragraph_format.space_after = Pt(0)
run(pp, "Undo the ____________ thing that was done to x first  (think: socks and shoes).",
    size=11)

# ============================================================
# WORKED EXAMPLE (to copy)
# ============================================================
heading("3  ·  Worked example — copy this down")
we = doc.add_table(rows=1, cols=2); no_borders(we); we.alignment = WD_TABLE_ALIGNMENT.CENTER
wc = we.cell(0, 0); cell_pad(wc, 60); wc.width = Inches(3.0)
steps = [("Solve  3x + 5 = 20", True, NAVY, 12),
         ("− 5 from both sides", False, GREY, 10),
         ("3x = 15", True, NAVY, 12),
         ("÷ 3 on both sides", False, GREY, 10),
         ("x = 5", True, RGBColor(0x2C,0x7A,0x3F), 13)]
first = True
for txt, b, col, sz in steps:
    p = wc.paragraphs[0] if first else wc.add_paragraph(); first = False
    p.paragraph_format.space_after = Pt(3)
    run(p, txt, size=sz, bold=b, color=col)
nc = we.cell(0, 1); cell_pad(nc, 60); nc.width = Inches(3.6)
p = nc.paragraphs[0]; p.paragraph_format.space_after = Pt(4)
run(p, "Check:  ", size=11, bold=True, color=NAVY)
run(p, "3 × 5 + 5 = 15 + 5 = 20  ✓", size=11)
p = nc.add_paragraph(); p.paragraph_format.space_after = Pt(0)
run(p, "Always finish by checking — substitute your answer back in and make sure both "
       "sides are equal.", size=10.5, italic=True, color=GREY)

# ============================================================
# MAIN TASK — RAG
# ============================================================
heading("4  ·  Your turn — show every step")
para("Start at whichever level you like, then work down and across. Show one step per line and "
     "check each answer. Everyone tries at least one Stretch question.", size=10.5, italic=True,
     color=GREY, after=6)

def task_block(tag, tag_color, fill, questions):
    tbl = doc.add_table(rows=1, cols=1); set_borders(tbl); tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.cell(0, 0); cell_pad(c, 90); keep_together(tbl)
    hp = c.paragraphs[0]; hp.paragraph_format.space_after = Pt(4)
    r = run(hp, " " + tag + " ", size=11, bold=True, color=RGBColor(0xFF,0xFF,0xFF))
    # shade the tag run
    rpr = r._r.get_or_add_rPr(); sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), fill)
    rpr.append(sh)
    for q in questions:
        qp = c.add_paragraph(); qp.paragraph_format.space_after = Pt(2)
        run(qp, q, size=11.5, bold=True, color=INK)
        # two ruled answer lines
        for _ in range(2):
            lp = c.add_paragraph(); lp.paragraph_format.space_after = Pt(8)
            pPr = lp._p.get_or_add_pPr(); pbdr = OxmlElement("w:pBdr")
            bottom = OxmlElement("w:bottom")
            bottom.set(qn("w:val"), "single"); bottom.set(qn("w:sz"), "4")
            bottom.set(qn("w:space"), "1"); bottom.set(qn("w:color"), LINE_GREY)
            pbdr.append(bottom); pPr.append(pbdr)
    para("", after=2)

task_block("WARM-UP", NAVY, "B33A2B",
           ["1)   2x + 1 = 9", "2)   3x + 2 = 14", "3)   4x − 3 = 9"])
task_block("CORE", NAVY, "9A6A0F",
           ["4)   5x + 7 = 42", "5)   10 = 3x + 1", "6)   x/2 + 3 = 7"])
task_block("STRETCH", NAVY, "2C7A3F",
           ["7)   7 = 5x − 8",
            "8)   x/3 − 2 = 4",
            "9)   I think of a number, multiply it by 4 and subtract 5. The answer is 23. "
            "What was my number?"])

# ============================================================
# CHALLENGE
# ============================================================
heading("5  ·  Challenge — spot the mistake")
para("Aisha solves  5x + 3 = 23  like this:", size=10.5, italic=True, color=GREY, after=4)
ch = doc.add_table(rows=1, cols=1); set_borders(ch); ch.alignment = WD_TABLE_ALIGNMENT.CENTER
cc = ch.cell(0, 0); cell_pad(cc, 90); keep_together(ch)
for txt, col in [("5x + 3 = 23", INK), ("2x = 20", RGBColor(0xB3,0x3A,0x2B)),
                 ("x = 10", RGBColor(0xB3,0x3A,0x2B))]:
    pp = cc.paragraphs[0] if txt == "5x + 3 = 23" else cc.add_paragraph()
    pp.paragraph_format.space_after = Pt(2); run(pp, txt, size=12, bold=True, color=col)
para("What did Aisha do wrong? Write the correct solution and prove it works.", after=6)
blank_lines(3)

# ============================================================
# SELF-ASSESSMENT
# ============================================================
heading("How well do I understand today's topic?")
sa = doc.add_table(rows=1, cols=1); set_borders(sa); sa.alignment = WD_TABLE_ALIGNMENT.CENTER
sc = sa.cell(0, 0); cell_pad(sc, 100)
pp = sc.paragraphs[0]; pp.paragraph_format.space_after = Pt(4)
run(pp, "Colour the circle that matches how you feel:        ", size=11)
run(pp, "● Red ", size=13, bold=True, color=RGBColor(0xC0,0x39,0x2B))
run(pp, "(need more help)      ", size=10.5, color=GREY)
run(pp, "● Amber ", size=13, bold=True, color=RGBColor(0xC8,0x8A,0x14))
run(pp, "(nearly there)      ", size=10.5, color=GREY)
run(pp, "● Green ", size=13, bold=True, color=RGBColor(0x2C,0x7A,0x3F))
run(pp, "(confident)", size=10.5, color=GREY)
pp = sc.add_paragraph(); pp.paragraph_format.space_before = Pt(4); pp.paragraph_format.space_after = Pt(0)
run(pp, "One thing I could explain to someone else:  ", size=11, bold=True, color=NAVY)
run(pp, "________________________________________", size=11)

# footer note
para("Answers are on the lesson slides so you can mark your own work.  "
     "Curriculum alignment: Oak National Academy knowledge graphs (OGL v3.0), "
     "Oak's representation of the National Curriculum for England (2014) — not an official "
     "DfE publication.", size=8, italic=True, color=GREY, before=10, after=0)

doc.save("Year8-Solving-Two-Step-Equations-Worksheet.docx")
print("Saved Year8-Solving-Two-Step-Equations-Worksheet.docx")
