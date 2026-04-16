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
