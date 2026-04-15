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

---

## Adapting for Your EDA

The petition PDFs include placeholder attribution for Vancouver Centre NDP. To adapt for your riding:

1. Open `make-petition.py`
2. Update `ATTRIBUTION` and `FOOTER_RETURN` with your EDA name and contact
3. Run `uv run python make-petition.py`

No design software required.

---

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — free to use, adapt, and share with attribution.

---

Maintained by [@barrettsoron](https://github.com/barrettsoron), membership secretary, Vancouver Centre NDP. Questions: hello@vcndp.ca
