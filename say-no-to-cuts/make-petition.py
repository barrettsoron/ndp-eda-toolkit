from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
import os

# ── CONTENT ───────────────────────────────────────────────────────────────────

TITLE       = 'SAY NO TO CARNEY\u2019S CUTS'
ATTRIBUTION = (
    'Federal NDP Campaign \u2014 ndp.ca/say-no-to-cuts \u2014 April 2026'
)
SUMMARY = (
    'Mark Carney and the Liberals are planning deep cuts to the services Canadians depend on. '
    'Working families will face longer emergency room waits, gutted employment insurance services, '
    'and reduced Canada Post access for seniors, rural communities, and people with disabilities. '
    'Austerity is not leadership. Cuts are not solutions. Abandoning people is not nation-building.'
)
STATEMENT = (
    '\u201cI oppose the Liberal government\u2019s planned cuts to public services '
    'and call on the government to protect healthcare, Canada Post, and the employment '
    'services that Canadians depend on.\u201d'
)

LABEL_FULL_NAME = 'Full Name'
LABEL_ADDR      = 'Street Address'
LABEL_UNIT      = 'Unit / Apartment'
LABEL_CITY      = 'City'
LABEL_POSTAL    = 'Postal Code'
LABEL_EMAIL     = 'Email Address'
LABEL_PHONE     = 'Phone (optional)'
LABEL_SIGNATURE = 'Signature'
LABEL_DATE      = 'Date'

FOOTER_RETURN  = 'Return signed forms to your chapter lead or any riding association event. \u2502 ndp.ca/say-no-to-cuts'
FOOTER_PRIVACY = (
    'Info collected per NDP Privacy Policy. May be used to contact you about NDP activities; '
    'shared with riding associations; never sold. Opt out: dnc@ndp.ca \u2502 ndp.ca/privacy'
)

OUTPUT = os.path.join(os.path.dirname(__file__), 'say-no-to-cuts-petition.pdf')

# ── LAYOUT CONSTANTS — do not change without reading references/layout.md ─────

LOGO_PATH = os.path.join(os.path.dirname(__file__), 'ndp-logo-white.png')

PAGE_W, PAGE_H = letter
FORM_H   = PAGE_H / 2

BASE        = 8
MARGIN      = 3 * BASE
INNER_W     = PAGE_W - 2 * MARGIN

ORANGE      = HexColor('#F58220')
DARK        = HexColor('#58595B')

BAR_H       = 44
TOP_PAD     = 18
LABEL_SIZE  = 7.0
LINE_H      = 20
SIG_LINE_H  = 28
FIELD_GAP   = 2
SECT_GAP    = BASE
SPLIT       = (0.62, 0.34)


# ── HELPERS ───────────────────────────────────────────────────────────────────

def split_widths():
    a = INNER_W * SPLIT[0]
    b = INNER_W * SPLIT[1]
    return a, b, INNER_W - a - b


def wrap(c, text, font, size, max_w):
    words = text.split()
    line, lines = [], []
    for word in words:
        test = ' '.join(line + [word])
        if c.stringWidth(test, font, size) <= max_w:
            line.append(word)
        else:
            lines.append(' '.join(line))
            line = [word]
    lines.append(' '.join(line))
    return lines


def fit_font(c, text, font, max_w, start=13.0, floor=7.0):
    size = start
    while c.stringWidth(text, font, size) > max_w and size > floor:
        size -= 0.25
    return size


def draw_field(c, x, y, label, width, line_h=LINE_H):
    rule_y  = y - line_h
    c.setStrokeColor(DARK)
    c.setLineWidth(0.5)
    c.line(x, rule_y, x + width, rule_y)
    label_y = rule_y - LABEL_SIZE - 2
    c.setFont('Helvetica-Bold', LABEL_SIZE)
    c.setFillColor(DARK)
    c.drawString(x, label_y, label.upper())
    return label_y


# ── FORM ──────────────────────────────────────────────────────────────────────

def draw_form(c, top_y):
    col_a, col_b, col_gap = split_widths()

    bar_y = top_y - BAR_H - TOP_PAD
    c.setFillColor(ORANGE)
    c.rect(MARGIN, bar_y, INNER_W, BAR_H, fill=1, stroke=0)

    logo   = ImageReader(LOGO_PATH)
    logo_h = 24
    logo_w = logo_h * (1650 / 300)
    c.drawImage(logo,
                PAGE_W - MARGIN - logo_w - BASE // 2,
                bar_y + (BAR_H - logo_h) / 2,
                width=logo_w, height=logo_h, mask='auto')

    title_max_w = INNER_W - logo_w - BASE // 2 - BASE
    title_size  = fit_font(c, TITLE, 'Helvetica-Bold', title_max_w)
    c.setFillColor(white)
    c.setFont('Helvetica-Bold', title_size)
    c.drawString(MARGIN + BASE, bar_y + 27, TITLE)

    c.setFont('Helvetica', 6)
    c.drawString(MARGIN + BASE, bar_y + 13, ATTRIBUTION)

    y = bar_y - SECT_GAP
    c.setFont('Helvetica', 9)
    c.setFillColor(DARK)
    for ln in wrap(c, SUMMARY, 'Helvetica', 9, INNER_W):
        c.drawString(MARGIN, y, ln)
        y -= 11

    y -= SECT_GAP
    rule_x = MARGIN + BASE
    text_x = rule_x + BASE
    stmt_w = INNER_W - (text_x - MARGIN)
    stmt_lines   = wrap(c, STATEMENT, 'Helvetica-BoldOblique', 8.5, stmt_w)
    stmt_block_h = len(stmt_lines) * 11

    c.setStrokeColor(ORANGE)
    c.setLineWidth(2)
    c.line(rule_x, y + 9, rule_x, y - stmt_block_h + 2)
    c.setLineWidth(0.5)

    c.setFont('Helvetica-BoldOblique', 8.5)
    c.setFillColor(DARK)
    for ln in stmt_lines:
        c.drawString(text_x, y, ln)
        y -= 11

    y -= SECT_GAP

    y = draw_field(c, MARGIN, y, LABEL_FULL_NAME, INNER_W) - FIELD_GAP

    a_b = draw_field(c, MARGIN,              y, LABEL_ADDR,   col_a)
    u_b = draw_field(c, MARGIN+col_a+col_gap, y, LABEL_UNIT,   col_b)
    y = min(a_b, u_b) - FIELD_GAP

    c_b = draw_field(c, MARGIN,              y, LABEL_CITY,   col_a)
    p_b = draw_field(c, MARGIN+col_a+col_gap, y, LABEL_POSTAL, col_b)
    y = min(c_b, p_b) - FIELD_GAP

    y = draw_field(c, MARGIN, y, LABEL_EMAIL, INNER_W) - FIELD_GAP
    y = draw_field(c, MARGIN, y, LABEL_PHONE, col_a)   - FIELD_GAP

    draw_field(c, MARGIN,              y, LABEL_SIGNATURE, col_a, line_h=SIG_LINE_H)
    draw_field(c, MARGIN+col_a+col_gap, y, LABEL_DATE,      col_b, line_h=SIG_LINE_H)

    footer_y = (top_y - FORM_H) + 4 * BASE
    c.setFont('Helvetica-Oblique', 6.0)
    c.setFillColor(DARK)
    priv_lines = wrap(c, FOOTER_PRIVACY, 'Helvetica-Oblique', 6.0, INNER_W)
    y_foot = footer_y
    for ln in reversed(priv_lines):
        c.drawString(MARGIN, y_foot, ln)
        y_foot += 9
    c.setFont('Helvetica', 6.5)
    c.drawString(MARGIN, y_foot, FOOTER_RETURN)


def draw_cut_line(c):
    cut_y = FORM_H + BASE
    c.setStrokeColor(DARK)
    c.setLineWidth(0.4)
    c.setDash(4, 4)
    c.line(MARGIN - 6, cut_y, PAGE_W - MARGIN + 6, cut_y)
    c.setDash()
    c.setFont('Helvetica', 8)
    c.setFillColor(DARK)
    c.drawCentredString(PAGE_W / 2, cut_y + 2, '\u2702')


# ── GENERATE ──────────────────────────────────────────────────────────────────

cv = canvas.Canvas(OUTPUT, pagesize=letter)
draw_form(cv, PAGE_H)
draw_cut_line(cv)
draw_form(cv, FORM_H)
cv.save()
print(f'Written: {OUTPUT}')
