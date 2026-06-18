# -*- coding: utf-8 -*-
"""Year 8 cover lesson: Solving Two-Step Equations (60 min, non-specialist deliverable)."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ---------- palette / fonts ----------
NAVY   = RGBColor(0x1E, 0x27, 0x61)
NAVY_D = RGBColor(0x14, 0x1B, 0x47)
ICE    = RGBColor(0xCA, 0xDC, 0xFC)
ICE_LT = RGBColor(0xEC, 0xF2, 0xFE)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
INK    = RGBColor(0x26, 0x2B, 0x33)
MUTED  = RGBColor(0x5B, 0x65, 0x77)
RED_T  = RGBColor(0xFB, 0xE9, 0xE7); RED_D  = RGBColor(0xB3, 0x3A, 0x2B)
AMB_T  = RGBColor(0xFD, 0xF3, 0xD7); AMB_D  = RGBColor(0x9A, 0x6A, 0x0F)
GRN_T  = RGBColor(0xE6, 0xF3, 0xE7); GRN_D  = RGBColor(0x2C, 0x7A, 0x3F)
HEAD = "Trebuchet MS"
BODY = "Calibri"

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

# ---------- helpers ----------
def new_slide(bg=WHITE):
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = bg
    return s

def add_text(slide, x, y, w, h, paras, valign=MSO_ANCHOR.TOP, wrap=True):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = valign
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = p.get("align", PP_ALIGN.LEFT)
        if p.get("space_after") is not None: para.space_after = Pt(p["space_after"])
        if p.get("space_before") is not None: para.space_before = Pt(p["space_before"])
        if p.get("line") is not None: para.line_spacing = p["line"]
        for txt, o in p["runs"]:
            r = para.add_run(); r.text = txt
            r.font.size = Pt(o.get("size", 16))
            r.font.bold = o.get("bold", False)
            r.font.italic = o.get("italic", False)
            r.font.name = o.get("font", BODY)
            r.font.color.rgb = o.get("color", INK)
    return tb

def card(slide, x, y, w, h, fill=ICE_LT, line=None, line_w=1.0, round_=True, radius=0.10):
    shp = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if round_ else MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h))
    if round_:
        try: shp.adjustments[0] = radius
        except Exception: pass
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else:
        shp.line.color.rgb = line; shp.line.width = Pt(line_w)
    shp.shadow.inherit = False
    return shp

def rect(slide, x, y, w, h, fill, line=None):
    return card(slide, x, y, w, h, fill=fill, line=line, round_=False)

def circle(slide, x, y, d, fill, txt, txt_color=WHITE, size=16, bold=True):
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    shp.line.fill.background(); shp.shadow.inherit = False
    tf = shp.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = txt
    r.font.size = Pt(size); r.font.bold = bold; r.font.name = HEAD
    r.font.color.rgb = txt_color
    return shp

def slide_title(slide, kicker, title_txt):
    add_text(slide, 0.7, 0.38, 11.9, 0.3,
             [{"runs": [(kicker, {"size": 12, "bold": True, "color": MUTED, "font": HEAD})]}])
    add_text(slide, 0.7, 0.66, 11.9, 0.8,
             [{"runs": [(title_txt, {"size": 32, "bold": True, "color": NAVY, "font": HEAD})]}])

def footer(slide, n):
    add_text(slide, 0.7, 7.08, 11.9, 0.3,
             [{"runs": [(u"Solving two-step equations · Maths · Year 8 · slide %d" % n,
                         {"size": 9, "color": MUTED})]}])

def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text

def R(t, **kw): return (t, kw)

# ============================================================
# SLIDE 1 — TITLE
# ============================================================
s = new_slide(NAVY)
add_text(s, 0.0, 1.05, 13.333, 0.35,
         [{"runs": [R(u"MATHEMATICS · ALGEBRA · COVER LESSON", size=13, bold=True, color=ICE, font=HEAD)],
           "align": PP_ALIGN.CENTER}])
add_text(s, 0.0, 1.55, 13.333, 1.1,
         [{"runs": [R(u"Solving Two-Step Equations", size=44, bold=True, color=WHITE, font=HEAD)],
           "align": PP_ALIGN.CENTER}])
add_text(s, 0.0, 2.75, 13.333, 0.5,
         [{"runs": [R(u"Year 8  ·  finding the unknown in equations like 3x + 5 = 20",
                      size=20, color=ICE)], "align": PP_ALIGN.CENTER}])
# balance scale motif
rect(s, 4.4, 4.55, 4.5, 0.06, ICE)                      # beam
tri = s.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(6.44), Inches(4.61), Inches(0.45), Inches(0.55))
tri.fill.solid(); tri.fill.fore_color.rgb = ICE; tri.line.fill.background(); tri.shadow.inherit = False
tri.rotation = 0
rect(s, 6.19, 5.16, 0.95, 0.07, ICE)                    # base
rect(s, 4.59, 4.61, 0.025, 0.26, ICE)                   # left string
rect(s, 8.69, 4.61, 0.025, 0.26, ICE)                   # right string
lp = card(s, 3.85, 4.87, 1.5, 0.55, fill=ICE); lt = lp.text_frame
lt.vertical_anchor = MSO_ANCHOR.MIDDLE; p = lt.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = u"3x + 5"; r.font.size = Pt(18); r.font.bold = True; r.font.name = HEAD; r.font.color.rgb = NAVY
rp = card(s, 7.95, 4.87, 1.5, 0.55, fill=ICE); rt = rp.text_frame
rt.vertical_anchor = MSO_ANCHOR.MIDDLE; p = rt.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = u"20"; r.font.size = Pt(18); r.font.bold = True; r.font.name = HEAD; r.font.color.rgb = NAVY
add_text(s, 0.0, 6.45, 13.333, 0.4,
         [{"runs": [R(u"[School Name]   ·   Today's Date", size=14, color=ICE)],
           "align": PP_ALIGN.CENTER}])
notes(s, u"[3 mins, including settling] Welcome the class in and take the register. "
         u"Say: \"Good morning/afternoon. Your normal teacher has set today's lesson and everything "
         u"you need is on these slides, including all the answers, so we can run it together exactly "
         u"as planned. Today's topic is solving two-step equations. An equation is a maths sentence "
         u"with an equals sign and a mystery number in it, written as a letter like x. Our job is to "
         u"find that mystery number.\" You don't need to be a maths specialist: every example is fully "
         u"worked through on the slides and in these notes. Students need: exercise book, pen, ruler. "
         u"No calculators are needed (and ideally not used). When everyone is settled, move on.")

# ============================================================
# SLIDE 2 — HOW THIS LESSON WORKS
# ============================================================
s = new_slide()
slide_title(s, u"BEFORE WE START", u"How this lesson works")
rows = [
    (u"Work through the slides in order", u"Don't skip ahead — each slide builds on the one before."),
    (u"Write everything in your exercise book", u"Date and title, then show every step of working for every question."),
    (u"Self-mark when an answers slide appears", u"Tick what you got right; correct anything you got wrong in a different colour."),
    (u"Stuck? Use the 3 Bs", u"Brain (re-read the worked example) → Buddy (ask your neighbour quietly) → Boss (ask the teacher)."),
    (u"Finished early?", u"Head to the Challenge slide — there's a spot-the-mistake puzzle waiting for you."),
]
y = 1.72
for i, (head, sub) in enumerate(rows):
    circle(s, 0.8, y + 0.10, 0.52, NAVY, str(i + 1), size=18)
    add_text(s, 1.55, y, 10.9, 0.95,
             [{"runs": [R(head, size=18, bold=True, color=NAVY, font=HEAD)], "space_after": 2},
              {"runs": [R(sub, size=14.5, color=MUTED)]}])
    y += 1.02
footer(s, 2)
notes(s, u"[2 mins] Read the five rules aloud. Say: \"Two of these really matter today. First — show "
         u"your working. In algebra the working IS the maths; an answer on its own scores nothing. "
         u"Second — when an answers slide comes up, you mark your own work honestly. Getting something "
         u"wrong and fixing it is exactly how you get better at this.\" "
         u"Tip: writing the date and title on the board now saves questions later.")

# ============================================================
# SLIDE 3 — LEARNING OBJECTIVES
# ============================================================
s = new_slide()
slide_title(s, u"TODAY'S GOALS", u"By the end of this lesson, you will be able to…")
card(s, 0.8, 1.85, 5.75, 2.5, fill=ICE_LT)
circle(s, 1.15, 2.2, 0.55, NAVY, u"1", size=18)
add_text(s, 1.15, 3.0, 5.05, 1.2,
         [{"runs": [R(u"Solve two-step equations", size=20, bold=True, color=NAVY, font=HEAD)], "space_after": 4},
          {"runs": [R(u"like 3x + 5 = 20, using inverse operations on both sides.", size=15, color=INK)]}])
card(s, 6.85, 1.85, 5.75, 2.5, fill=ICE_LT)
circle(s, 7.2, 2.2, 0.55, NAVY, u"2", size=18)
add_text(s, 7.2, 3.0, 5.05, 1.2,
         [{"runs": [R(u"Check a solution", size=20, bold=True, color=NAVY, font=HEAD)], "space_after": 4},
          {"runs": [R(u"by substituting it back into the equation to see if both sides balance.", size=15, color=INK)]}])
card(s, 0.8, 4.75, 11.8, 1.55, fill=WHITE, line=ICE, line_w=1.5)
add_text(s, 1.15, 5.0, 11.2, 1.1,
         [{"runs": [R(u"Why “two-step”?  ", size=15, bold=True, color=NAVY, font=HEAD),
                    R(u"Because two operations have happened to x. In 3x + 5 = 20, x was multiplied by 3, "
                      u"then 5 was added — so we need two “undo” steps to get x back on its own.",
                      size=15, color=INK)], "line": 1.15}])
footer(s, 3)
notes(s, u"[1 min] Read the two objectives aloud, then the \"Why two-step?\" box. The key phrase to use "
         u"all lesson is \"inverse operation\", which just means the opposite operation: the inverse of "
         u"adding 5 is subtracting 5; the inverse of multiplying by 3 is dividing by 3.")

# ============================================================
# SLIDE 4 — RETRIEVAL STARTER
# ============================================================
s = new_slide()
slide_title(s, u"DO NOW · 5 MINUTES", u"Starter: what do you remember?")
card(s, 0.8, 1.62, 11.8, 0.62, fill=NAVY)
add_text(s, 1.1, 1.74, 11.2, 0.4,
         [{"runs": [R(u"In your book  ·  no calculator  ·  on your own  ·  answers on the next slide",
                      size=14, bold=True, color=WHITE, font=HEAD)]}])
qs = [
    (u"1", u"Solve:  x + 7 = 15"),
    (u"2", u"Solve:  3x = 21"),
    (u"3", u"Solve:  x − 4 = 9"),
    (u"4", u"Simplify:  4a + 3a − 2"),
    (u"5", u"If y = 6, work out the value of  2y + 3"),
]
pos = [(0.8, 2.55), (6.85, 2.55), (0.8, 3.95), (6.85, 3.95), (0.8, 5.35)]
for (num, q), (x, y) in zip(qs, pos):
    card(s, x, y, 5.75, 1.15, fill=ICE_LT)
    circle(s, x + 0.3, y + 0.31, 0.52, NAVY, num, size=17)
    add_text(s, x + 1.05, y + 0.0, 4.5, 1.15,
             [{"runs": [R(q, size=18, bold=True, color=INK)]}], valign=MSO_ANCHOR.MIDDLE)
card(s, 6.85, 5.35, 5.75, 1.15, fill=WHITE, line=ICE, line_w=1.5)
add_text(s, 7.15, 5.35, 5.2, 1.15,
         [{"runs": [R(u"Hint for Q1–3: ", size=13.5, bold=True, color=NAVY),
                    R(u"what's the opposite of what has been done to the letter?", size=13.5, color=MUTED)]}],
         valign=MSO_ANCHOR.MIDDLE)
footer(s, 4)
notes(s, u"[6 mins — 5 working + 1 settling] Say: \"Five questions to warm your brain up — these use "
         u"things you've already learned. Five minutes, in your book, no calculators, in silence. Number "
         u"your answers 1 to 5.\" Q1–3 are one-step equations (last lessons' work), Q4 and Q5 revisit "
         u"simplifying and substitution from earlier units. Circulate while they work. "
         u"Watch for the classic error on Q3: for x − 4 = 9 some students will answer 5 (doing 9 minus 4) "
         u"— the correct answer is 13, because the opposite of subtracting 4 is ADDING 4. Don't correct it "
         u"yet; the next slide handles it.")

# ============================================================
# SLIDE 5 — STARTER ANSWERS
# ============================================================
s = new_slide()
slide_title(s, u"SELF-MARK", u"Starter answers")
ans = [
    (u"1", u"x = 8",  u"x + 7 = 15  →  subtract 7 from both sides."),
    (u"2", u"x = 7",  u"3x = 21  →  3x means 3 × x, so divide both sides by 3."),
    (u"3", u"x = 13", u"x − 4 = 9  →  ADD 4 to both sides. (Not 9 − 4 = 5 — that's the classic trap!)"),
    (u"4", u"7a − 2", u"4a + 3a = 7a. The − 2 isn't an “a” term, so it stays as it is."),
    (u"5", u"15",     u"2y + 3 with y = 6  →  2 × 6 + 3 = 12 + 3 = 15."),
]
y = 1.75
for num, a, how in ans:
    circle(s, 0.8, y + 0.13, 0.5, NAVY, num, size=16)
    add_text(s, 1.55, y, 1.85, 0.8, [{"runs": [R(a, size=21, bold=True, color=GRN_D, font=HEAD)]}],
             valign=MSO_ANCHOR.MIDDLE)
    add_text(s, 3.55, y, 9.0, 0.8, [{"runs": [R(how, size=14.5, color=INK)]}],
             valign=MSO_ANCHOR.MIDDLE)
    y += 0.92
add_text(s, 0.8, 6.45, 11.8, 0.45,
         [{"runs": [R(u"Tick each one you got right. Correct any mistakes in a different colour — "
                      u"5/5 is great, but a fixed mistake is even better.", size=14, italic=True, color=MUTED)]}])
footer(s, 5)
notes(s, u"[3 mins] Say: \"Pens down. Swap to your marking colour and mark your own as I read these "
         u"out.\" Go through each answer, reading the explanation column aloud. Pause on Q3 — ask for a "
         u"show of hands: \"Who got 5? Don't worry, that's the most common wrong answer in the country. "
         u"Who can explain why it's 13?\" (Because the equation says some number minus 4 gives 9, so the "
         u"number must be BIGGER than 9: 13 − 4 = 9.) This idea — using the opposite operation — is the "
         u"whole of today's lesson.")

# ============================================================
# SLIDE 6 — KEY VOCABULARY
# ============================================================
s = new_slide()
slide_title(s, u"KEY WORDS", u"Vocabulary and notation")
vocab = [
    (u"Equation",          u"A statement that two expressions are equal, shown by the = sign.", u"3x + 5 = 20"),
    (u"Unknown (variable)", u"The letter standing for the number we don't know yet.",            u"the x"),
    (u"Solution",          u"The value of the unknown that makes both sides balance.",           u"x = 5"),
    (u"Inverse operation", u"The operation that undoes another.",                                u"+ undoes −,  × undoes ÷"),
    (u"Coefficient",       u"The number the unknown is multiplied by.",                          u"the 3 in 3x"),
]
y = 1.7
for term, defn, ex in vocab:
    card(s, 0.8, y, 2.9, 0.78, fill=NAVY)
    add_text(s, 1.0, y, 2.5, 0.78, [{"runs": [R(term, size=16, bold=True, color=WHITE, font=HEAD)]}],
             valign=MSO_ANCHOR.MIDDLE)
    add_text(s, 3.95, y, 5.9, 0.78, [{"runs": [R(defn, size=14, color=INK)]}], valign=MSO_ANCHOR.MIDDLE)
    add_text(s, 10.0, y, 2.6, 0.78, [{"runs": [R(ex, size=14, bold=True, color=NAVY)]}],
             valign=MSO_ANCHOR.MIDDLE)
    y += 0.92
card(s, 0.8, 6.35, 11.8, 0.7, fill=ICE_LT)
add_text(s, 1.1, 6.35, 11.2, 0.7,
         [{"runs": [R(u"Notation:  ", size=14.5, bold=True, color=NAVY, font=HEAD),
                    R(u"3x means 3 × x (we don't write the × sign).   x/2 means x ÷ 2.",
                      size=14.5, color=INK)]}], valign=MSO_ANCHOR.MIDDLE)
footer(s, 6)
notes(s, u"[3 mins] Read each word, its meaning, and the example. Pronunciation: coefficient is "
         u"\"co-uh-FISH-unt\". Say: \"The big one today is INVERSE OPERATION — it just means the "
         u"opposite. The inverse of add 5 is subtract 5. The inverse of multiply by 3 is divide by 3.\" "
         u"Quick check: ask the class — \"What's the inverse of subtracting 7?\" (adding 7) — \"of "
         u"dividing by 2?\" (multiplying by 2). Also stress the notation box: 3x means 3 times x; "
         u"students often ask what 3x \"is\".")

# ============================================================
# SLIDE 7 — BIG IDEA: BALANCE
# ============================================================
s = new_slide()
slide_title(s, u"THE BIG IDEA", u"An equation is a balance")
add_text(s, 0.8, 1.75, 5.4, 1.5,
         [{"runs": [R(u"The = sign tells you the two sides have exactly the same value — like a set of "
                      u"balanced scales.", size=16, color=INK)], "space_after": 8, "line": 1.15},
          {"runs": [R(u"If you change one side, the scales tip… unless you do the same thing to the "
                      u"other side.", size=16, color=INK)], "line": 1.15}])
card(s, 0.8, 3.45, 5.4, 1.35, fill=NAVY)
add_text(s, 1.1, 3.62, 4.8, 1.0,
         [{"runs": [R(u"THE GOLDEN RULE", size=13, bold=True, color=ICE, font=HEAD)], "space_after": 4},
          {"runs": [R(u"Whatever you do to one side, you must do to the other.", size=17, bold=True,
                      color=WHITE, font=HEAD)], "line": 1.1}])
add_text(s, 0.8, 5.05, 5.4, 1.6,
         [{"runs": [R(u"Bar model:  2x + 3 = 11", size=15, bold=True, color=NAVY, font=HEAD)],
           "space_after": 4},
          {"runs": [R(u"The top bar (two x's and a 3) is the same length as the bottom bar (11). "
                      u"Remove the 3 and the two x's must make 8 — so each x is 4.",
                      size=13.5, color=MUTED)], "line": 1.12}])
# right: balance scale
rect(s, 7.3, 2.1, 4.4, 0.06, NAVY)
tri = s.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(9.28), Inches(2.16), Inches(0.45), Inches(0.5))
tri.fill.solid(); tri.fill.fore_color.rgb = NAVY; tri.line.fill.background(); tri.shadow.inherit = False
rect(s, 9.03, 2.66, 0.95, 0.07, NAVY)
rect(s, 7.48, 2.16, 0.025, 0.24, NAVY)
rect(s, 11.5, 2.16, 0.025, 0.24, NAVY)
pan1 = card(s, 6.75, 2.4, 1.5, 0.5, fill=ICE)
t = pan1.text_frame; t.vertical_anchor = MSO_ANCHOR.MIDDLE
p = t.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = u"2x + 3"; r.font.size = Pt(16); r.font.bold = True; r.font.name = HEAD; r.font.color.rgb = NAVY
pan2 = card(s, 10.78, 2.4, 1.5, 0.5, fill=ICE)
t = pan2.text_frame; t.vertical_anchor = MSO_ANCHOR.MIDDLE
p = t.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = u"11"; r.font.size = Pt(16); r.font.bold = True; r.font.name = HEAD; r.font.color.rgb = NAVY
# bar model: total width 4.95in for 11 units => unit 0.45
UX = 7.05; UY = 3.95; UNIT = 0.45; BH = 0.62
for i in range(2):
    b = rect(s, UX + i * 4 * UNIT, UY, 4 * UNIT - 0.04, BH, ICE, line=NAVY)
    t = b.text_frame; t.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = t.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = u"x"; r.font.size = Pt(17); r.font.bold = True; r.font.italic = True
    r.font.name = HEAD; r.font.color.rgb = NAVY
b = rect(s, UX + 8 * UNIT, UY, 3 * UNIT - 0.04, BH, WHITE, line=NAVY)
t = b.text_frame; t.vertical_anchor = MSO_ANCHOR.MIDDLE
p = t.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = u"3"; r.font.size = Pt(17); r.font.bold = True; r.font.name = HEAD; r.font.color.rgb = NAVY
b = rect(s, UX, UY + BH + 0.12, 11 * UNIT - 0.04, BH, NAVY)
t = b.text_frame; t.vertical_anchor = MSO_ANCHOR.MIDDLE
p = t.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = u"11"; r.font.size = Pt(17); r.font.bold = True; r.font.name = HEAD; r.font.color.rgb = WHITE
add_text(s, 7.05, 5.45, 5.0, 1.2,
         [{"runs": [R(u"Take 3 from both bars:  2x = 8", size=15, bold=True, color=NAVY)], "space_after": 3},
          {"runs": [R(u"Split 8 between the two x's:  x = 4", size=15, bold=True, color=GRN_D)]}])
footer(s, 7)
notes(s, u"[4 mins] Say: \"Look at the scales. The left pan holds 2x + 3, the right pan holds 11, and "
         u"they balance — that's what the equals sign means.\" Then the golden rule — get the whole "
         u"class to read it aloud together once: \"Whatever you do to one side, you must do to the "
         u"other.\" Then walk through the bar model on the right, reading the two lines at the bottom. "
         u"Common misconception to flag: students sometimes change only one side of an equation — the "
         u"scales picture shows why that breaks everything.")

# ============================================================
# SLIDE 8 — WORKED EXAMPLE 1
# ============================================================
s = new_slide()
slide_title(s, u"WORKED EXAMPLE 1", u"Solve  3x + 5 = 20")
card(s, 0.8, 1.75, 5.6, 4.6, fill=ICE_LT)
work = [
    (u"3x + 5 = 20", 26, NAVY, True, False),
    (u"− 5 from both sides", 13.5, MUTED, False, True),
    (u"3x = 15", 26, NAVY, True, False),
    (u"÷ 3 on both sides", 13.5, MUTED, False, True),
    (u"x = 5", 30, GRN_D, True, False),
]
paras = []
for txt, sz, col, bold, ital in work:
    paras.append({"runs": [R(txt, size=sz, bold=bold, italic=ital, color=col,
                             font=HEAD if bold else BODY)],
                  "align": PP_ALIGN.CENTER, "space_after": 8})
add_text(s, 1.1, 2.05, 5.0, 4.0, paras)
steps = [
    (u"1", u"Undo the + 5 first", u"It was the last thing done to x, so it's the first thing we undo. Inverse of + 5 is − 5."),
    (u"2", u"Undo the × 3", u"3x means 3 × x. The inverse of multiplying by 3 is dividing by 3."),
    (u"3", u"Check it!", u"Substitute back in:  3 × 5 + 5 = 15 + 5 = 20  ✓  Both sides match."),
]
y = 1.75
for num, head, sub in steps:
    circle(s, 6.85, y + 0.08, 0.5, NAVY, num, size=16)
    add_text(s, 7.6, y, 5.0, 1.25,
             [{"runs": [R(head, size=17, bold=True, color=NAVY, font=HEAD)], "space_after": 2},
              {"runs": [R(sub, size=14, color=INK)], "line": 1.1}])
    y += 1.32
card(s, 6.85, 5.85, 5.75, 0.85, fill=GRN_T)
add_text(s, 7.15, 5.85, 5.2, 0.85,
         [{"runs": [R(u"Socks and shoes:  ", size=14, bold=True, color=GRN_D, font=HEAD),
                    R(u"socks on first, shoes last — so shoes come OFF first. Undo the last operation first.",
                      size=14, color=INK)]}], valign=MSO_ANCHOR.MIDDLE)
footer(s, 8)
notes(s, u"[5 mins] Talk through the working line by line, pointing at the screen. Script: \"x was "
         u"multiplied by 3, then 5 was added. To get x back on its own we undo those — in reverse "
         u"order, like socks and shoes. Step 1: subtract 5 from BOTH sides — golden rule — leaving "
         u"3x = 15. Step 2: 3x means 3 times x, so divide BOTH sides by 3: x = 5. Step 3: check it — "
         u"3 times 5 is 15, plus 5 is 20. The equation balances, so we KNOW we're right.\" "
         u"Emphasise that the check takes 5 seconds and catches almost every mistake. "
         u"Ask before moving on: \"What would step 1 be for 2x + 9 = 17?\" (subtract 9 from both sides).")

# ============================================================
# SLIDE 9 — WORKED EXAMPLE 2
# ============================================================
s = new_slide()
slide_title(s, u"WORKED EXAMPLE 2", u"Solve  4x − 7 = 13")
card(s, 0.8, 1.75, 5.6, 4.6, fill=ICE_LT)
work = [
    (u"4x − 7 = 13", 26, NAVY, True, False),
    (u"+ 7 to both sides", 13.5, MUTED, False, True),
    (u"4x = 20", 26, NAVY, True, False),
    (u"÷ 4 on both sides", 13.5, MUTED, False, True),
    (u"x = 5", 30, GRN_D, True, False),
]
paras = []
for txt, sz, col, bold, ital in work:
    paras.append({"runs": [R(txt, size=sz, bold=bold, italic=ital, color=col,
                             font=HEAD if bold else BODY)],
                  "align": PP_ALIGN.CENTER, "space_after": 8})
add_text(s, 1.1, 2.05, 5.0, 4.0, paras)
card(s, 6.85, 1.75, 5.75, 1.5, fill=WHITE, line=ICE, line_w=1.5)
add_text(s, 7.15, 1.95, 5.2, 1.15,
         [{"runs": [R(u"What's different?  ", size=15, bold=True, color=NAVY, font=HEAD),
                    R(u"This time 7 was subtracted. The inverse of − 7 is + 7, so we ADD 7 to both sides.",
                      size=14.5, color=INK)], "line": 1.15}])
card(s, 6.85, 3.5, 5.75, 1.5, fill=WHITE, line=ICE, line_w=1.5)
add_text(s, 7.15, 3.7, 5.2, 1.15,
         [{"runs": [R(u"Same answer, two routes.  ", size=15, bold=True, color=NAVY, font=HEAD),
                    R(u"You could divide by 4 first — it still works. Undoing the + or − first usually "
                      u"keeps the numbers friendlier.", size=14.5, color=INK)], "line": 1.15}])
card(s, 6.85, 5.25, 5.75, 1.1, fill=GRN_T)
add_text(s, 7.15, 5.25, 5.2, 1.1,
         [{"runs": [R(u"Check:  ", size=15, bold=True, color=GRN_D, font=HEAD),
                    R(u"4 × 5 − 7 = 20 − 7 = 13  ✓", size=16, bold=True, color=INK)]}],
         valign=MSO_ANCHOR.MIDDLE)
footer(s, 9)
notes(s, u"[4 mins] Same routine as example 1 — talk through each line. Script: \"This one has a "
         u"subtraction. Careful — the most common mistake here is to subtract 7 again. We need the "
         u"INVERSE: the opposite of subtracting 7 is adding 7. Add 7 to both sides: 4x = 20. Divide "
         u"both sides by 4: x = 5. Check: 4 times 5 is 20, minus 7 is 13. Balanced!\" "
         u"Point out the \"two routes\" box: there's more than one correct method — that's normal in "
         u"maths — but undoing the add/subtract first usually avoids fractions.")

# ============================================================
# SLIDE 10 — YOUR TURN (GUIDED PRACTICE)
# ============================================================
s = new_slide()
slide_title(s, u"GUIDED PRACTICE", u"Your turn — use the same steps")
card(s, 0.8, 1.62, 11.8, 0.62, fill=NAVY)
add_text(s, 1.1, 1.74, 11.2, 0.4,
         [{"runs": [R(u"In your book  ·  copy the equation, then one step per line  ·  5 minutes  ·  "
                      u"don't forget the check!", size=14, bold=True, color=WHITE, font=HEAD)]}])
for x0, label, eq, s1, s2 in [
    (0.8,  u"A", u"2x + 3 = 11", u"Step 1:  subtract ___ from both sides", u"Step 2:  divide both sides by ___"),
    (6.85, u"B", u"5x − 4 = 26", u"Step 1:  _______ 4 to both sides",      u"Step 2:  divide both sides by ___"),
]:
    card(s, x0, 2.5, 5.75, 3.7, fill=ICE_LT)
    circle(s, x0 + 0.35, 2.85, 0.55, NAVY, label, size=18)
    add_text(s, x0 + 1.15, 2.85, 4.3, 0.6,
             [{"runs": [R(u"Solve:  " + eq, size=22, bold=True, color=NAVY, font=HEAD)]}])
    add_text(s, x0 + 0.4, 3.85, 5.0, 2.2,
             [{"runs": [R(s1, size=15.5, color=INK)], "space_after": 10},
              {"runs": [R(s2, size=15.5, color=INK)], "space_after": 10},
              {"runs": [R(u"Step 3:  check by substituting your answer back in.", size=15.5, color=INK)],
               "space_after": 10},
              {"runs": [R(u"Stuck? The worked examples on slides 8–9 use exactly the same steps.",
                          size=13, italic=True, color=MUTED)]}])
footer(s, 10)
notes(s, u"[6 mins] Say: \"Your turn. Two equations, same recipe as the examples. Copy the equation, "
         u"then one step per line, then check your answer. Five minutes.\" Circulate while they work — "
         u"the sentence frames on the cards tell them what each step should be. "
         u"ANSWERS for your reference: A) subtract 3 from both sides giving 2x = 8, divide by 2 giving "
         u"x = 4 (check: 2×4+3 = 11 ✓). B) ADD 4 to both sides giving 5x = 30, divide by 5 giving x = 6 "
         u"(check: 5×6−4 = 26 ✓). After 5 minutes, ask two confident volunteers to read out their steps "
         u"and confirm against these answers. If many struggled, re-show slide 8 before moving on.")

# ============================================================
# SLIDE 11 — COMMON MISTAKES
# ============================================================
s = new_slide()
slide_title(s, u"BE CAREFUL", u"Three mistakes to avoid")
mistakes = [
    (u"Changing only one side",
     u"3x + 5 = 20  →  3x = 20",
     u"Subtract 5 from BOTH sides:  3x = 15. Keep the balance!"),
    (u"Taking the number from the x-term too",
     u"5x + 3 = 23  →  2x = 20",
     u"Subtracting 3 only removes the + 3. The 5x is untouched:  5x = 20."),
    (u"Repeating instead of inverting",
     u"2x − 5 = 11  →  2x = 6",
     u"The inverse of − 5 is + 5. Add 5 to both sides:  2x = 16."),
]
y = 1.72
for head, wrong, right in mistakes:
    add_text(s, 0.8, y, 4.0, 1.45,
             [{"runs": [R(head, size=16, bold=True, color=NAVY, font=HEAD)], "line": 1.1}],
             valign=MSO_ANCHOR.MIDDLE)
    card(s, 4.95, y, 3.6, 1.45, fill=RED_T)
    add_text(s, 5.2, y + 0.18, 3.15, 1.1,
             [{"runs": [R(u"✗  ", size=16, bold=True, color=RED_D), R(wrong, size=14.5, bold=True, color=RED_D)],
               "space_after": 2}])
    card(s, 8.75, y, 3.85, 1.45, fill=GRN_T)
    add_text(s, 9.0, y + 0.18, 3.4, 1.1,
             [{"runs": [R(u"✓  ", size=16, bold=True, color=GRN_D), R(right, size=13.5, color=INK)],
               "line": 1.1}])
    y += 1.68
footer(s, 11)
notes(s, u"[3 mins] Say: \"Before you practise on your own, here are the three mistakes that catch "
         u"people out — if you avoid these, you'll fly.\" Read each row: the red box is the wrong move, "
         u"the green box is the fix. Mistake 2 is the big one for this topic: when subtracting 3 from "
         u"5x + 3, some students also knock the 5 down to 2 — but the 3 and the 5x are different things; "
         u"removing the + 3 leaves 5x alone. Ask: \"If I subtract 2 from 4x + 2, what's left?\" (4x, "
         u"not 2x.)")

# ============================================================
# SLIDE 12 — INDEPENDENT PRACTICE (RAG)
# ============================================================
s = new_slide()
slide_title(s, u"INDEPENDENT PRACTICE · 13 MINUTES", u"Pick your starting point")
cols = [
    (RED_T, RED_D, u"WARM-UP", u"Start here if you want to build confidence",
     [u"1)   2x + 1 = 9", u"2)   3x + 2 = 14", u"3)   4x − 3 = 9"]),
    (AMB_T, AMB_D, u"CORE", u"Most people start here",
     [u"4)   5x + 7 = 42", u"5)   10 = 3x + 1", u"6)   x/2 + 3 = 7"]),
    (GRN_T, GRN_D, u"STRETCH", u"Everyone tries at least one",
     [u"7)   7 = 5x − 8", u"8)   x/3 − 2 = 4", u"9)   I think of a number, multiply it by 4 and subtract 5. The answer is 23. What was my number?"]),
]
x = 0.8
for fill, deep, head, sub, qlist in cols:
    card(s, x, 1.7, 3.84, 4.55, fill=fill)
    add_text(s, x + 0.3, 1.95, 3.25, 0.75,
             [{"runs": [R(head, size=18, bold=True, color=deep, font=HEAD)], "space_after": 2},
              {"runs": [R(sub, size=12, italic=True, color=MUTED)]}])
    paras = []
    for q in qlist:
        paras.append({"runs": [R(q, size=15.5, bold=True, color=INK)], "space_after": 12, "line": 1.1})
    add_text(s, x + 0.3, 2.95, 3.25, 3.1, paras)
    x += 4.0
card(s, 0.8, 6.45, 11.8, 0.62, fill=NAVY)
add_text(s, 1.1, 6.57, 11.2, 0.4,
         [{"runs": [R(u"Every step on its own line  ·  check each answer by substituting  ·  "
                      u"finished? → Challenge slide", size=13.5, bold=True, color=WHITE, font=HEAD)]}])
footer(s, 12)
notes(s, u"[13 mins, including the Challenge slide for early finishers] Say: \"Now it's over to you. "
         u"Choose your starting column: warm-up if you're not yet sure, core if you're fairly confident. "
         u"Work down and to the right — everyone should attempt at least one stretch question. Full "
         u"working, one step per line, and check every answer by substituting it back.\" "
         u"ANSWERS for your reference: 1) x=4  2) x=4  3) x=3  4) x=7  5) x=3  6) x=8  7) x=3  8) x=18  "
         u"9) the number is 7 (the equation is 4n − 5 = 23). "
         u"Tips while circulating: Q5 and Q7 have the x-term on the RIGHT — it works exactly the same "
         u"way (for Q5, subtract 1 from both sides to get 9 = 3x, so x = 3). Q6: x/2 means x divided by "
         u"2, so after subtracting 3 you MULTIPLY both sides by 2. Early finishers go to the next slide. "
         u"If time is short, drop the stretch column.")

# ============================================================
# SLIDE 13 — CHALLENGE
# ============================================================
s = new_slide()
slide_title(s, u"CHALLENGE", u"For the brave (and the finished)")
card(s, 0.8, 1.75, 5.75, 4.5, fill=ICE_LT)
add_text(s, 1.1, 2.0, 5.15, 0.8,
         [{"runs": [R(u"🕵  Spot the mistake", size=19, bold=True, color=NAVY, font=HEAD)]}])
card(s, 1.1, 2.75, 5.15, 2.0, fill=WHITE, line=ICE, line_w=1.5)
add_text(s, 1.45, 2.95, 4.5, 1.7,
         [{"runs": [R(u"Aisha solves  5x + 3 = 23:", size=14.5, italic=True, color=MUTED)], "space_after": 6},
          {"runs": [R(u"5x + 3 = 23", size=18, bold=True, color=INK)], "space_after": 4},
          {"runs": [R(u"2x = 20", size=18, bold=True, color=RED_D)], "space_after": 4},
          {"runs": [R(u"x = 10", size=18, bold=True, color=RED_D)]}])
add_text(s, 1.1, 5.0, 5.15, 1.1,
         [{"runs": [R(u"What has Aisha done wrong? Explain it in a sentence, then find the correct "
                      u"solution — and prove yours works.", size=14.5, color=INK)], "line": 1.15}])
card(s, 6.85, 1.75, 5.75, 4.5, fill=ICE_LT)
add_text(s, 7.15, 2.0, 5.15, 0.8,
         [{"runs": [R(u"🛠  Equation builder", size=19, bold=True, color=NAVY, font=HEAD)]}])
add_text(s, 7.15, 2.75, 5.15, 1.6,
         [{"runs": [R(u"Write your own two-step equation whose solution is  x = 4.",
                      size=15.5, color=INK)], "space_after": 8, "line": 1.15},
          {"runs": [R(u"Then swap with a neighbour and solve each other's.", size=15.5, color=INK)],
           "line": 1.15}])
card(s, 7.15, 4.45, 5.15, 1.55, fill=WHITE, line=ICE, line_w=1.5)
add_text(s, 7.45, 4.62, 4.6, 1.25,
         [{"runs": [R(u"Success criteria:", size=13.5, bold=True, color=NAVY, font=HEAD)], "space_after": 3},
          {"runs": [R(u"• it has a multiply step AND an add or subtract step", size=13.5, color=INK)],
           "space_after": 2},
          {"runs": [R(u"• substituting x = 4 makes both sides equal", size=13.5, color=INK)]}])
footer(s, 13)
notes(s, u"[For early finishers — no separate time slot] Direct fast workers here from the practice "
         u"task. For your reference: Aisha's mistake is that when she subtracted 3 from both sides, she "
         u"also took 3 away from the 5x (turning it into 2x). Subtracting 3 only removes the + 3 — the "
         u"correct working is 5x + 3 = 23 → 5x = 20 → x = 4 (check: 5 × 4 + 3 = 23 ✓). "
         u"For the equation builder, any equation works if substituting 4 balances it — e.g. 3x + 2 = 14 "
         u"or 2x − 5 = 3. Students check each other's by solving them.")

# ============================================================
# SLIDE 14 — EXIT TICKET
# ============================================================
s = new_slide()
slide_title(s, u"EXIT TICKET · 5 MINUTES", u"Prove what you've learned")
card(s, 0.8, 1.62, 11.8, 0.62, fill=NAVY)
add_text(s, 1.1, 1.74, 11.2, 0.4,
         [{"runs": [R(u"On your own  ·  in your book under the heading “Exit ticket”  ·  full working",
                      size=14, bold=True, color=WHITE, font=HEAD)]}])
ex = [
    (u"1", u"Solve:  3x + 4 = 19"),
    (u"2", u"Solve:  2x − 5 = 11"),
    (u"3", u"Jo says x = 6 is the solution of  4x + 2 = 25.\nIs Jo right? Show how you know."),
]
y = 2.55
for num, q in ex:
    card(s, 0.8, y, 11.8, 1.25, fill=ICE_LT)
    circle(s, 1.15, y + 0.36, 0.52, NAVY, num, size=17)
    lines = q.split(u"\n")
    paras = [{"runs": [R(lines[0], size=18, bold=True, color=INK)], "space_after": 2}]
    if len(lines) > 1:
        paras.append({"runs": [R(lines[1], size=15, color=MUTED)]})
    add_text(s, 1.95, y, 10.3, 1.25, paras, valign=MSO_ANCHOR.MIDDLE)
    y += 1.42
footer(s, 14)
notes(s, u"[5 mins] Say: \"Last task — this is how you prove to yourself, and to your teacher, that "
         u"today has stuck. Three questions, on your own, in silence, full working. Five minutes.\" "
         u"Question 3 is deliberately different: students should substitute 6 into 4x + 2, get 26, and "
         u"notice that 26 is not 25 — so Jo is WRONG. Answers are on the next slide. Your normal teacher "
         u"will want to see this work, so make sure names/dates are on it; if students worked on paper "
         u"rather than books, collect it in.")

# ============================================================
# SLIDE 15 — ANSWERS
# ============================================================
s = new_slide()
slide_title(s, u"SELF-MARK", u"Answers")
add_text(s, 0.8, 1.65, 11.8, 0.4,
         [{"runs": [R(u"Independent practice", size=17, bold=True, color=NAVY, font=HEAD)]}])
pr = [
    (RED_T, RED_D, [u"1)  x = 4    2)  x = 4    3)  x = 3"]),
    (AMB_T, AMB_D, [u"4)  x = 7    5)  x = 3    6)  x = 8"]),
    (GRN_T, GRN_D, [u"7)  x = 3    8)  x = 18", u"9)  the number was 7"]),
]
x = 0.8
for fill, deep, lines in pr:
    card(s, x, 2.1, 3.84, 1.05, fill=fill)
    add_text(s, x + 0.3, 2.1, 3.3, 1.05,
             [{"runs": [R(ln, size=14.5, bold=True, color=INK)], "line": 1.2} for ln in lines],
             valign=MSO_ANCHOR.MIDDLE)
    x += 4.0
add_text(s, 0.8, 3.45, 11.8, 0.4,
         [{"runs": [R(u"Challenge — Aisha's mistake", size=17, bold=True, color=NAVY, font=HEAD)]}])
card(s, 0.8, 3.9, 11.8, 0.95, fill=ICE_LT)
add_text(s, 1.1, 3.9, 11.2, 0.95,
         [{"runs": [R(u"Subtracting 3 should only remove the + 3 — Aisha also took 3 from the 5x. "
                      u"Correct:  5x + 3 = 23  →  5x = 20  →  x = 4   (check: 5 × 4 + 3 = 23 ✓)",
                      size=14.5, color=INK)], "line": 1.15}], valign=MSO_ANCHOR.MIDDLE)
add_text(s, 0.8, 5.05, 11.8, 0.4,
         [{"runs": [R(u"Exit ticket", size=17, bold=True, color=NAVY, font=HEAD)]}])
card(s, 0.8, 5.5, 11.8, 1.1, fill=GRN_T)
add_text(s, 1.1, 5.5, 11.2, 1.1,
         [{"runs": [R(u"1)  x = 5        2)  x = 8        3)  Jo is wrong: substituting gives "
                      u"4 × 6 + 2 = 26, and 26 ≠ 25. (The real solution isn't a whole number!)",
                      size=15, bold=True, color=INK)], "line": 1.2}], valign=MSO_ANCHOR.MIDDLE)
add_text(s, 0.8, 6.78, 11.8, 0.55,
         [{"runs": [R(u"Curriculum alignment based on Oak National Academy's curriculum knowledge graphs "
                      u"(Open Government Licence v3.0), Oak's representation of the National Curriculum "
                      u"for England (2014) — not an official DfE publication.",
                      size=8.5, italic=True, color=MUTED)], "line": 1.1}])
notes(s, u"[4 mins] Say: \"Marking colours out — mark your practice questions and your exit ticket.\" "
         u"Read the answers aloud, then ask for a quick confidence vote: \"Hands up if you'd be happy "
         u"to solve 6x + 1 = 19 right now.\" (If anyone shouts an answer: x = 3.) "
         u"Finish: \"Two things to remember: an equation is a balance — same to both sides — and always "
         u"check by substituting. Books closed, equipment away.\" Leave any collected exit tickets and a "
         u"brief note on how the lesson went for the class teacher.")

prs.save(u"Year8-Solving-Two-Step-Equations-Lesson.pptx")
print("Saved Year8-Solving-Two-Step-Equations-Lesson.pptx with %d slides" % len(prs.slides._sldIdLst))
