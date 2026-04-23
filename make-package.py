"""
Builds data-centre-regina/data-centre-package.pdf — full shareable asset package.

Page order:
  1    Cover page (attribution, licence, disclaimer)
  2–3  Petition print sheet (2-up, letter)
  4+   Supporting docs: canvass guide, fact sheet, tenant explainer,
       social copy, chapter email, Indigenous consultation questions
"""

import os
import subprocess
import tempfile

import markdown
import pypdf
from weasyprint import HTML, CSS

ROOT   = os.path.dirname(__file__)
MODULE = os.path.join(ROOT, "data-centre-regina")

DOCS = [
    "canvass-guide.md",
    "fact-sheet.md",
    "tenant-explainer.md",
    "bell-response.md",
    "social-copy.md",
    "chapter-email.md",
    "indigenous-consultation-questions.md",
]

CSS_STYLE = CSS(string="""
    @page {
        margin: 20mm 18mm 20mm 18mm;
        size: letter;
    }

    body {
        font-family: Helvetica, Arial, sans-serif;
        font-size: 10pt;
        color: #58595B;
        line-height: 1.5;
    }

    h1 {
        font-size: 16pt;
        color: #F58220;
        border-bottom: 2px solid #F58220;
        padding-bottom: 4pt;
        margin-top: 0;
    }

    h2 {
        font-size: 12pt;
        color: #58595B;
        border-left: 4px solid #F58220;
        padding-left: 8pt;
        margin-top: 16pt;
    }

    h3 {
        font-size: 10.5pt;
        font-style: italic;
    }

    p { margin: 6pt 0; }

    blockquote {
        border-left: 3px solid #F58220;
        margin: 8pt 0 8pt 8pt;
        padding-left: 10pt;
        font-style: italic;
    }

    ul, ol { margin: 4pt 0; padding-left: 18pt; }
    li { margin-bottom: 3pt; }

    a { color: #F58220; }

    table {
        border-collapse: collapse;
        width: 100%;
        font-size: 9pt;
        margin: 8pt 0;
    }

    th {
        background: #F58220;
        color: white;
        padding: 4pt 6pt;
        text-align: left;
    }

    td {
        border-bottom: 0.5pt solid #CCCCCC;
        padding: 3pt 6pt;
    }

    hr {
        border: none;
        border-top: 0.5pt solid #CCCCCC;
        margin: 12pt 0;
    }
""")


COVER_HTML = """\
<!DOCTYPE html>
<html>
<body>
<div class="cover">
  <div class="header-bar">
    <div class="campaign">Pause Bell&rsquo;s 300 MW AI Data Centre</div>
    <div class="subtitle">Regina&ndash;Wascana NDP &mdash; CIA Money. MAGA Investors. Our Grid, Our Choice.</div>
  </div>

  <div class="what">
    <p>This package contains organizing assets for the community campaign to pause Bell
    Canada&rsquo;s proposed 300&nbsp;MW AI data centre campus in the RM of Sherwood,
    outside Regina, Saskatchewan (Treaty&nbsp;4 territory). Prepared by Barrett Soron
    for Regina&ndash;Wascana NDP, April 2026.</p>

    <p><strong>Contents:</strong> petition print sheet &middot; canvasser guide &middot;
    fact sheet &middot; tenant explainer (CoreWeave &amp; Cerebras) &middot; social copy
    &middot; chapter email &middot; Indigenous consultation questions</p>
  </div>

  <div class="section-head">Source &amp; Attribution</div>
  <p>All materials are open source and freely adaptable under the
  <a href="https://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0
  International Licence (CC&nbsp;BY&nbsp;4.0)</a>. You may use, reproduce, translate,
  and adapt these materials for any purpose, including commercial use, provided you
  credit <em>Barrett Soron / Regina&ndash;Wascana NDP</em> and link to the source
  repository.</p>

  <p>Source repository:
  <a href="https://github.com/barrettsoron/ndp-eda-toolkit/tree/main/data-centre-regina">
  github.com/barrettsoron/ndp-eda-toolkit/data-centre-regina</a></p>

  <div class="section-head">Factual Claims &amp; Fair Dealing</div>
  <p>Factual claims in these materials are drawn from publicly available sources, including
  corporate filings, press releases, parliamentary records, and published journalism.
  Sources are cited in full in the module README and in the tenant explainer.
  Reproduction of brief excerpts from third-party sources for the purposes of criticism,
  comment, news reporting, and political education is protected under the fair dealing
  provisions of the <em>Copyright Act</em>, RSC 1985, c&nbsp;C-42, s&nbsp;29.</p>

  <div class="section-head">Legal Disclaimer</div>
  <p>These materials are produced for lawful political organizing purposes under the
  <em>Canada Elections Act</em> and applicable provincial legislation. They do not
  constitute legal advice. Organizers are responsible for ensuring their own use of
  these materials complies with applicable law, including electoral financing rules,
  anti-spam legislation (CASL), and privacy obligations under the federal NDP Privacy
  Policy.</p>

  <p>Factual descriptions of corporate ownership, investor relationships, and government
  contracts are based on publicly reported information and are made in good faith.
  Nothing in these materials is intended to defame any individual or organization.
  Political criticism of corporations and their investors is protected expression under
  the <em>Canadian Charter of Rights and Freedoms</em>, s&nbsp;2(b).</p>

  <p>If you identify a factual error, please open an issue at the source repository above.</p>

  <div class="footer">
    Regina&ndash;Wascana NDP &nbsp;&middot;&nbsp; Treaty 4 territory &nbsp;&middot;&nbsp;
    April 2026 &nbsp;&middot;&nbsp;
    <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>
  </div>
</div>
</body>
</html>
"""

COVER_CSS = CSS(string="""
    @page {
        margin: 20mm 18mm 20mm 18mm;
        size: letter;
    }

    body {
        font-family: Helvetica, Arial, sans-serif;
        font-size: 9.5pt;
        color: #58595B;
        line-height: 1.5;
    }

    .header-bar {
        background: #F58220;
        color: white;
        padding: 14pt 16pt 12pt 16pt;
        margin-bottom: 18pt;
    }

    .campaign {
        font-size: 16pt;
        font-weight: bold;
        letter-spacing: 0.02em;
    }

    .subtitle {
        font-size: 8pt;
        margin-top: 4pt;
        opacity: 0.92;
    }

    .what {
        margin-bottom: 14pt;
    }

    .section-head {
        font-size: 10pt;
        font-weight: bold;
        color: #F58220;
        border-bottom: 1pt solid #F58220;
        padding-bottom: 2pt;
        margin: 14pt 0 6pt 0;
    }

    p { margin: 0 0 7pt 0; }

    a { color: #F58220; }

    .footer {
        margin-top: 24pt;
        font-size: 8pt;
        color: #999;
        border-top: 0.5pt solid #CCCCCC;
        padding-top: 6pt;
    }
""")


def make_cover(out_path):
    HTML(string=COVER_HTML).write_pdf(out_path, stylesheets=[COVER_CSS])


def md_to_pdf(md_path, out_path):
    with open(md_path, encoding="utf-8") as f:
        text = f.read()
    html_body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "nl2br"],
    )
    html = f"<!DOCTYPE html><html><body>{html_body}</body></html>"
    HTML(string=html, base_url=MODULE).write_pdf(out_path, stylesheets=[CSS_STYLE])


def merge_pdfs(paths, out_path):
    writer = pypdf.PdfWriter()
    for path in paths:
        reader = pypdf.PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
    with open(out_path, "wb") as f:
        writer.write(f)


def main():
    petition_pdf = os.path.join(MODULE, "data-centre-petition.pdf")
    petition_script = os.path.join(MODULE, "make-petition.py")
    subprocess.run(["uv", "run", "python", petition_script], check=True, cwd=ROOT)

    parts = []

    with tempfile.TemporaryDirectory() as tmp:
        cover_pdf = os.path.join(tmp, "cover.pdf")
        print("  rendering cover…")
        make_cover(cover_pdf)
        parts.append(cover_pdf)

        parts.append(petition_pdf)
        for filename in DOCS:
            md_path  = os.path.join(MODULE, filename)
            out_path = os.path.join(tmp, filename.replace(".md", ".pdf"))
            print(f"  rendering {filename}…")
            md_to_pdf(md_path, out_path)
            parts.append(out_path)

        out = os.path.join(MODULE, "data-centre-package.pdf")
        merge_pdfs(parts, out)

    print(f"Written: {out}")


if __name__ == "__main__":
    main()
