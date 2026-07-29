# Ta'allim — تعليم

AI-powered English teaching platform for Algerian schools.

## What It Does

| Component | Description |
|-----------|-------------|
| **Exercise Generator** | 6 types (fill-blank, MCQ, sentence building, error correction, matching, transformation) — offline + API modes |
| **Flashcard System** | SM-2 spaced repetition (Anki-style) with deck management |
| **MCQ Quiz** | Auto-scored quizzes with explanations |
| **Mind Maps** | Visual HTML concept maps for grammar topics |
| **Assessment System** | Curriculum-aligned test generation (BEM + A1-B2) |
| **Student Dashboard** | Progress tracking across topics |
| **SIS** | Student Information System — dual-track bulletins, attendance, bilingual (FR/AR) |
| **Research** | Pilot study materials — manuscripts, analysis scripts, outreach templates |

## Quick Start

```bash
# Install
pip install -e .

# Run the web app
streamlit run app.py

# Or use the CLI
taallim topics                    # list all topics
taallim generate present_simple   # generate exercises
taallim quiz past_simple          # interactive quiz
```

## Curriculum Coverage

Aligned to the Algerian Ministry of Education curriculum:

| Level | Year | Topics | Exercise Types |
|-------|------|--------|----------------|
| A1 | 1AM | 16 topics | 6 types |
| A2 | 2AM | 15 topics | 6 types |
| B1 | 3AM | 14 topics | 6 types |
| B2 | 4AM | 14 topics | 6 types |

**64 topics** across 4 levels, **275+ exercises** ready offline.

## Project Structure

```
lifeworkspace-teaching-platform/
├── app.py                          # Streamlit web app (entry point)
├── cli.py                          # CLI entry point
├── src/taallim/                    # Python package
│   ├── __init__.py
│   ├── exercise_generator.py       # Core exercise engine (offline + API)
│   ├── offline_generator.py        # Offline exercise generation
│   ├── offline_data.py             # Question banks (1190 lines)
│   ├── topics.py                   # Topic data loader
│   ├── prompts.py                  # API prompt templates
│   ├── flashcard_system.py         # SM-2 spaced repetition
│   ├── mcq_generator.py            # MCQ quiz engine
│   ├── mindmap_generator.py        # Visual mind map builder
│   ├── sis/                        # Student Information System
│   │   ├── Allal_SIS_Demo_Kit.md   # Demo script + talking points
│   │   ├── SIS_MVP_Build_Spec.md   # 13-table schema, forms, VBA
│   │   ├── SIS_PRICING.md          # 45,000 DZD founding price
│   │   ├── sis_mockup.html         # Interactive FR/AR mockup
│   │   ├── BULLETIN_REMAP.md       # Grade model (CC + Compo)
│   │   └── ED_TECH_ROADMAP.md      # Unified roadmap
│   └── research/                   # Pilot study materials
│       ├── Taallim_Manuscript_EN_FINAL.md
│       ├── Taallim_Manuscrit_FR_FINAL.md
│       ├── taallim_analysis.py     # ANCOVA + stats
│       ├── sample_pilot_data.csv
│       ├── TAALLIM_TEST_SPECS.md   # 60-item test blueprint
│       ├── TAALLIM_SCHOOL_OUTREACH.md
│       ├── TAALLIM_6WEEK_PILOT_PLAN.md
│       └── TAALLIM_TEACHER_INSTRUMENTS_RQ3.md
├── data/topics/                    # Topic JSON files
│   ├── A1.json, A2.json, B1.json, B2.json
├── tests/
│   └── test_core.py                # Unit tests
├── pyproject.toml
├── requirements.txt
└── README.md
```

## SIS (Student Information System)

Dual-track school management for Algerian private schools:

| Feature | Description |
|---------|-------------|
| **Dual-track bulletins** | Academic + vocational in one system |
| **Bilingual** | French ⇄ Arabic toggle, RTL support |
| **Grade model** | CC + Compo, weighted averages, class rank |
| **Attendance** | Daily tracking per class |
| **One-click PDF** | Official Algerian bulletin format |
| **Pricing** | 45,000 DZD founding / 75,000 DZD list |

See `src/taallim/sis/` for demo kit, build spec, and pricing.

## Research & Publication

Pilot study for the Multilinguelles / ASJP journal:

- **EN manuscript** — §1–§6, grammar = primary outcome
- **FR manuscript** — §1/§2 translated
- **Analysis script** — ANCOVA, mixed ANOVA, correlations
- **Test instruments** — 6 parallel forms (Grammar A/B/C + Vocabulary A/B/C)
- **Outreach templates** — FR/AR emails for school directors
- **6-week pilot plan** — Allal + 1 public collège

See `src/taallim/research/` for all materials.

## API Mode (Optional)

Set `ANTHROPIC_API_KEY` environment variable for AI-generated exercises:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
streamlit run app.py
```

Without an API key, the platform uses pre-built offline question banks (no internet required).

## Export Formats

Exercises can be exported as:
- **HTML** — printable, styled worksheets
- **Markdown** — for Obsidian/notes
- **JSON** — for programmatic use

## Built For

- **Algerian middle school teachers** (1AM–4AM)
- **Private school English programs**
- **Tutoring and homework generation**
- **BEM exam preparation**
- **School administration** (SIS)

## Author

Mahi Kamel Abdelghani — kamelmahi71@gmail.com

## License

MIT
