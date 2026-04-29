# NDP EDA Toolkit

Organizing assets for NDP electoral district associations — ready to print, share, and adapt for your community.

Each folder is a self-contained campaign module with print materials, canvasser resources, and social copy.

---

## Modules

### [`surveillance-pricing/`](surveillance-pricing/)

Assets for the campaign to ban surveillance pricing (Motion M-30, MP Leah Gazan).

**Surveillance pricing** is when corporations use your personal data — where you live, what you search, how often you shop — to find the maximum price you'll pay, and charge you that. Two people buying the same product can be charged different amounts.

| File | Description |
|------|-------------|
| `surveillance-pricing-petition.pdf` | Print-ready petition, letter size, 2 forms per page (EN) |
| `surveillance-pricing-petition-fr.pdf` | Version française |
| `surveillance-pricing-canvasser-guide.md` | Door-to-door and table talking points |
| `surveillance-pricing-fact-sheet.md` | Leave-behind / table handout |
| `surveillance-pricing-social-copy.md` | Social media copy, 3 formats |
| `surveillance-pricing-chapter-email.md` | Chapter lead outreach email |
| `make-petition.py` | Script to regenerate the English petition PDF |
| `make-petition-fr.py` | Script to regenerate the French petition PDF |

**To regenerate PDFs:**
```bash
uv add reportlab
uv run python make-petition.py
uv run python make-petition-fr.py
```

**E-petition:** [ndp.ca/ban-surveillance-pricing](https://ndp.ca/ban-surveillance-pricing) · [npd.ca/interdire-tarification-surveillance](https://www.npd.ca/interdire-tarification-surveillance)

### [`data-centre-regina/`](data-centre-regina/)

Assets for the community campaign to pause Bell Canada's 300 MW AI data centre in the RM of Sherwood, outside Regina, Saskatchewan (Treaty 4 territory).

**Bell** is building Canada's largest purpose-built AI data centre campus — 160 acres, $1.7 billion — serving American AI companies CoreWeave and Cerebras. NDP Leader Avi Lewis has committed to a [Humans-First AI Policy](https://lewisisleader.ca/ideas/dignified-work) that includes pausing data centre expansion to protect clean water, affordable energy, and community decision-making.

| File | Description |
|------|-------------|
| `petition.md` | Petition copy — physical signature format, NDP privacy footer |
| `canvass-guide.md` | Door-to-door and table talking points, objection handling, data custody |
| `fact-sheet.md` | One-page backgrounder / leave-behind |
| `tenant-explainer.md` | Backgrounder on CoreWeave and Cerebras — origins, military/intelligence ties, investors |
| `social-copy.md` | Social media copy — short (Twitter/X), medium, and long (Facebook/Instagram) |
| `chapter-email.md` | Member email announcing the petition drive |
| `indigenous-consultation-questions.md` | Conversation-starters for organizer to bring to local First Nations contacts |
| `README.md` | Overview, e-petition note, data custody, sources |

**Physical signatures only** for now. See the module README for e-petition guidance.

### [`canada-strong-fund/`](canada-strong-fund/)

Assets for the campaign to fix the Canada Strong Fund — PM Mark Carney's $25-billion arm's-length Crown corporation, announced 2026-04-27.

**The Canada Strong Fund** is being marketed as Canada's first sovereign wealth fund. Its written mandate has no climate conditions, no UNDRIP/FPIC requirements, and no union-content rules — and it's seeded with $25-billion of public money to take minority equity stakes in private projects, alongside Bay Street pension funds and global asset managers. The "Pull a Norway" framing — Avi Lewis's response to the Spring Economic Statement — is the spine of the module: industry profits in, public good out.

| File | Description |
|------|-------------|
| `petition.md` | Petition copy — two demands: reject asset recycling; fund through a windfall profits tax on oil and gas |
| `make-petition.py` | Script to regenerate the petition PDF |
| `csf-organizing-kit.md` | Strategic frame, six-message stack, five demands, one-pager, tactical notes — the load-bearing source document |
| `talking-points.md` | Master message stack referenced by every tactic-specific guide |
| `canvass-guide.md` | Summer street canvassing and tabling |
| `small-group-guide.md` | Kitchen-table / living-room facilitation |
| `letters-to-editor.md` | LTE templates by angle and target outlet |
| `mp-letters.md` | MP letter templates — primary template addresses Hedy Fry (LPC, Vancouver Centre); especially LPC MPs |
| `social-copy.md` | Short, medium, and long format social posts |
| `chapter-email.md` | EDA member outreach |
| `fact-sheet.md` | One-page leave-behind |
| `signals-to-watch.md` | Diagnostic checklist for tracking the fund's design as it's finalised |
| `targets.md` | Institutional and constituency targets |
| `counter-proposal-canada-public-wealth-fund.md` | Inverted-design counter-proposal |
| `README.md` | Overview, scope, branding, sources |

**National policy fight, riding-level tactics.** Most files are stubs pending content extraction from the organizing kit and research note.

---

## Adapting for Your EDA

The petition PDFs include placeholder attribution for Vancouver Centre NDP. To adapt for your riding:

1. Open `make-petition.py`
2. Update `ATTRIBUTION` and `FOOTER_RETURN` with your EDA name and contact
3. Run `uv run python make-petition.py`

No design software required.

---

## Licence

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — free to use, adapt, and share with attribution.

---

Maintained by [@barrettsoron](https://github.com/barrettsoron), membership secretary, Vancouver Centre NDP. Questions: hello@vcndp.ca
