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

TITLE      = 'HALTE À LA TARIFICATION DE SURVEILLANCE'
ATTRIBUTION = (
    'Motion M-30 — Députée Leah Gazan (Winnipeg-Centre, NPD) '
    '— 45e Parlement, 1re session — 13 avril 2026'
)
SUMMARY = (
    'Les entreprises utilisent vos données personnelles — où vous habitez, ce que vous cherchez, '
    'à quelle fréquence vous magasinez — pour trouver le prix le plus élevé que vous accepterez '
    'de payer, et vous le facturer. Deux personnes qui achètent le même produit peuvent se voir '
    'facturer des montants différents. La motion M-30 demande au gouvernement d\u2019interdire '
    'cette pratique, en magasin et en ligne.'
)
STATEMENT = (
    '\u00abJ\u2019appuie la motion M-30 de la députée Leah Gazan et demande à la Chambre des '
    'communes d\u2019interdire la tarification de surveillance \u2014 où des données personnelles '
    'sont utilisées pour faire payer davantage les Canadiennes et les Canadiens, '
    'en magasin et en ligne.\u00bb'
)
FOOTER_RETURN  = 'Retournez les formulaires signés à votre responsable de section ou à tout événement de l\u2019association de circonscription. \u2502 npd.ca/interdire-tarification-surveillance'
FOOTER_PRIVACY = (
    'Renseignements recueillis conformément à la politique de confidentialité du NPD. '
    'Peuvent servir à vous joindre au sujet des activités du NPD; partagés avec les associations '
    'de circonscription; jamais vendus. Désabonnement\u202f: dnc@npd.ca \u2502 npd.ca/confidentialite'
)

FIELDS = [
    ('Nom complet',          'full',  None),
    ('Adresse civique',      'split_a', 'Unité / Appartement'),
    ('Ville',                'split_a', 'Code postal'),
    ('Adresse courriel',     'full',  None),
    ('Téléphone (facultatif)', 'half', None),
    ('Signature',            'split_a_sig', 'Date'),
]


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


def fit_font_size(c, text, font, max_w, start=13.0, min_size=7.0):
    """Step down from start until text fits within max_w."""
    size = start
    while c.stringWidth(text, font, size) > max_w and size > min_size:
        size -= 0.25
    return size


def draw_field(c, x, y, label, width, line_h=LINE_H):
    """Writing space + underline + label below. Returns y of label baseline."""
    rule_y = y - line_h
    c.setStrokeColor(DARK)
    c.setLineWidth(0.5)
    c.line(x, rule_y, x + width, rule_y)
    label_y = rule_y - LABEL_SIZE - 2
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

    # Title — auto-fit to available width beside logo
    title_max_w = INNER_W - logo_w - BASE // 2 - BASE   # indent + logo clearance
    title_size  = fit_font_size(c, TITLE, 'Helvetica-Bold', title_max_w)
    c.setFillColor(white)
    c.setFont('Helvetica-Bold', title_size)
    c.drawString(MARGIN + BASE, bar_y + 27, TITLE)

    # Attribution — lower line
    c.setFont('Helvetica', 6)
    c.drawString(MARGIN + BASE, bar_y + 13, ATTRIBUTION)

    # ── Summary ──────────────────────────────────────────────────────────────
    y = bar_y - SECT_GAP
    c.setFont('Helvetica', 9)
    c.setFillColor(DARK)
    for ln in wrap(c, SUMMARY, 'Helvetica', 9, INNER_W):
        c.drawString(MARGIN, y, ln)
        y -= 11

    # ── Petition statement — indented block with left orange rule ─────────────
    y -= SECT_GAP
    rule_x    = MARGIN + BASE
    text_x    = rule_x + BASE
    stmt_w    = INNER_W - (text_x - MARGIN)
    stmt_lines = wrap(c, STATEMENT, 'Helvetica-BoldOblique', 8.5, stmt_w)
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

    # Nom complet
    y = draw_field(c, MARGIN, y, 'Nom complet', INNER_W) - FIELD_GAP

    # Adresse civique | Unité / Appartement
    addr_b = draw_field(c, MARGIN, y, 'Adresse civique', col_a)
    unit_b = draw_field(c, MARGIN + col_a + col_gap, y, 'Unité / Appartement', col_b)
    y = min(addr_b, unit_b) - FIELD_GAP

    # Ville | Code postal
    city_b = draw_field(c, MARGIN, y, 'Ville', col_a)
    pc_b   = draw_field(c, MARGIN + col_a + col_gap, y, 'Code postal', col_b)
    y = min(city_b, pc_b) - FIELD_GAP

    # Adresse courriel
    y = draw_field(c, MARGIN, y, 'Adresse courriel', INNER_W) - FIELD_GAP

    # Téléphone (facultatif)
    y = draw_field(c, MARGIN, y, 'Téléphone (facultatif)', col_a) - FIELD_GAP

    # Signature | Date
    draw_field(c, MARGIN, y, 'Signature', col_a, line_h=SIG_LINE_H)
    draw_field(c, MARGIN + col_a + col_gap, y, 'Date', col_b, line_h=SIG_LINE_H)

    # ── Footer — pinned from bottom, wrapping if needed ──────────────────────
    footer_y = (top_y - FORM_H) + 4 * BASE
    c.setFont('Helvetica-Oblique', 6.0)
    c.setFillColor(DARK)
    privacy_lines = wrap(c, FOOTER_PRIVACY, 'Helvetica-Oblique', 6.0, INNER_W)
    y_foot = footer_y
    for ln in reversed(privacy_lines):          # draw bottom-up
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
    c.drawCentredString(PAGE_W / 2, cut_y + 2, '✂')


out = '/Users/mbbs/projects/vcndp-summer2026/surveillance-pricing/surveillance-pricing-petition-fr.pdf'
c = canvas.Canvas(out, pagesize=letter)
draw_form(c, PAGE_H)
draw_cut_line(c)
draw_form(c, FORM_H)
c.save()
print(f'Written: {out}')
