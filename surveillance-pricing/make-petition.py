from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.utils import ImageReader

PAGE_W, PAGE_H = letter   # 612 x 792
FORM_H = PAGE_H / 2       # 396 per half-sheet

BASE   = 8
MARGIN = 3 * BASE          # 24pt side margins
INNER_W = PAGE_W - 2 * MARGIN   # 564pt

ORANGE = HexColor('#F58220')
DARK   = HexColor('#58595B')
LIGHT  = HexColor('#CCCCCC')

LOGO_PATH = '/Users/mbbs/projects/vcndp-summer2026/surveillance-pricing/ndp-logo-white.png'

BAR_H      = 44            # 2-line bar: title + attribution, with breathing room
TOP_PAD    = 18            # ~0.25" print margin above bar
LABEL_SIZE = 7.0
LINE_H     = 20            # 20pt writing space (≈7mm)
SIG_LINE_H = 28            # 28pt for signature
FIELD_GAP  = 2             # 2pt between fields
SECT_GAP   = BASE          # 8pt between content sections — must exceed font ascender height
SPLIT_RATIO = (0.62, 0.34) # city/postal and street/unit column proportions


def split_widths():
    a = INNER_W * SPLIT_RATIO[0]
    b = INNER_W * SPLIT_RATIO[1]
    gap = INNER_W - a - b
    return a, b, gap


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


def draw_field(c, x, y, label, width, line_h=LINE_H):
    """Writing space + underline + label below. Returns y of label baseline."""
    rule_y = y - line_h
    c.setStrokeColor(DARK)
    c.setLineWidth(0.5)
    c.line(x, rule_y, x + width, rule_y)
    label_y = rule_y - LABEL_SIZE - 2   # label top 2pt below underline
    c.setFont('Helvetica-Bold', LABEL_SIZE)
    c.setFillColor(DARK)
    c.drawString(x, label_y, label.upper())
    return label_y


def draw_form(c, top_y):
    col_a, col_b, col_gap = split_widths()

    # ── Orange header bar — title + attribution ──────────────────────────────
    bar_y = top_y - BAR_H - TOP_PAD
    c.setFillColor(ORANGE)
    c.rect(MARGIN, bar_y, INNER_W, BAR_H, fill=1, stroke=0)

    # NDP logo — vertically centred, right-aligned
    logo   = ImageReader(LOGO_PATH)
    logo_h = 24
    logo_w = logo_h * (1650 / 300)   # 132pt
    c.drawImage(logo,
                PAGE_W - MARGIN - logo_w - BASE // 2,
                bar_y + (BAR_H - logo_h) / 2,
                width=logo_w, height=logo_h, mask='auto')

    # Title — upper line (baseline at ~2/3 of bar height)
    c.setFillColor(white)
    c.setFont('Helvetica-Bold', 13)
    c.drawString(MARGIN + BASE, bar_y + 27, 'STOP SURVEILLANCE PRICING')

    # Attribution — lower line (baseline at ~1/3 of bar height)
    c.setFont('Helvetica', 6)
    c.drawString(MARGIN + BASE, bar_y + 13,
        'Motion M-30 — MP Leah Gazan (Winnipeg Centre, NDP) '
        '— 45th Parliament, 1st Session — April 13, 2026')

    # ── Summary ──────────────────────────────────────────────────────────────
    y = bar_y - SECT_GAP
    c.setFont('Helvetica', 9)
    c.setFillColor(DARK)
    summary = (
        'Corporations use your personal data — where you live, what you search, how often you shop '
        '— to find the highest price you will pay, and charge you that. '
        'Two people buying the same product can be charged different amounts. '
        'Motion M-30 calls on the government to ban this practice, in stores and online.'
    )
    for ln in wrap(c, summary, 'Helvetica', 9, INNER_W):
        c.drawString(MARGIN, y, ln)
        y -= 11   # 11pt leading

    # ── Petition statement — indented block with left orange rule ─────────────
    y -= SECT_GAP
    stmt = (
        '\u201cI support MP Leah Gazan\u2019s Motion M-30 and call on the House of Commons '
        'to ban surveillance pricing \u2014 where personal data is used to charge '
        'Canadians more, in stores and online.\u201d'
    )
    rule_x    = MARGIN + BASE           # indent rule 8pt from margin
    text_x    = rule_x + BASE           # text 8pt right of rule
    stmt_w    = INNER_W - (text_x - MARGIN)
    stmt_lines = wrap(c, stmt, 'Helvetica-BoldOblique', 8.5, stmt_w)
    stmt_top   = y
    stmt_block_h = len(stmt_lines) * 11

    c.setStrokeColor(ORANGE)
    c.setLineWidth(2)
    c.line(rule_x, stmt_top + 9, rule_x, stmt_top - stmt_block_h + 2)
    c.setLineWidth(0.5)

    c.setFont('Helvetica-BoldOblique', 8.5)
    c.setFillColor(DARK)
    for ln in stmt_lines:
        c.drawString(text_x, y, ln)
        y -= 11

    # ── Fields ───────────────────────────────────────────────────────────────
    y -= SECT_GAP

    # Full Name
    y = draw_field(c, MARGIN, y, 'Full Name', INNER_W) - FIELD_GAP

    # Street Address | Unit / Apartment
    addr_b = draw_field(c, MARGIN, y, 'Street Address', col_a)
    unit_b = draw_field(c, MARGIN + col_a + col_gap, y, 'Unit / Apartment', col_b)
    y = min(addr_b, unit_b) - FIELD_GAP

    # City | Postal Code
    city_b = draw_field(c, MARGIN, y, 'City', col_a)
    pc_b   = draw_field(c, MARGIN + col_a + col_gap, y, 'Postal Code', col_b)
    y = min(city_b, pc_b) - FIELD_GAP

    # Email
    y = draw_field(c, MARGIN, y, 'Email Address', INNER_W) - FIELD_GAP

    # Phone (optional)
    y = draw_field(c, MARGIN, y, 'Phone (optional)', col_a) - FIELD_GAP

    # Signature | Date
    sig_b  = draw_field(c, MARGIN, y, 'Signature', col_a, line_h=SIG_LINE_H)
    date_b = draw_field(c, MARGIN + col_a + col_gap, y, 'Date', col_b, line_h=SIG_LINE_H)

    # ── Footer — pinned from bottom ───────────────────────────────────────────
    footer_y = (top_y - FORM_H) + 4 * BASE
    c.setFont('Helvetica-Oblique', 6.0)
    c.setFillColor(DARK)
    c.drawString(MARGIN, footer_y,
        'Info collected per NDP Privacy Policy. May be used to contact you about NDP activities; '
        'shared with riding associations; never sold. Opt out: dnc@ndp.ca \u2502 ndp.ca/privacy')
    c.setFont('Helvetica', 6.5)
    c.drawString(MARGIN, footer_y + 9,
        'Return signed forms to your chapter lead or any riding association event. \u2502 ndp.ca/ban-surveillance-pricing')


def draw_cut_line(c):
    cut_y = FORM_H + BASE
    c.setStrokeColor(DARK)
    c.setLineWidth(0.4)
    c.setDash(4, 4)
    c.line(MARGIN - 6, cut_y, PAGE_W - MARGIN + 6, cut_y)
    c.setDash()
    c.setFont('Helvetica', 8)
    c.setFillColor(DARK)
    c.drawCentredString(PAGE_W / 2, cut_y + 2, '✂')


out = '/Users/mbbs/projects/vcndp-summer2026/surveillance-pricing/surveillance-pricing-petition.pdf'
c = canvas.Canvas(out, pagesize=letter)
draw_form(c, PAGE_H)     # top half
draw_cut_line(c)
draw_form(c, FORM_H)     # bottom half
c.save()
print(f'Written: {out}')
