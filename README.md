# Ta'allim — تعليم

AI-powered English teaching platform for Algerian schools.

## What It Does

| Component | Description |
|-----------|-------------|
| **Exercise Generator** | 6 types (fill-blank, MCQ, sentence building, error correction, matching, translation) — offline + API modes |
| **Flashcard System** | SM-2 spaced repetition (Anki-style) with deck management |
| **MCQ Quiz** | Auto-scored quizzes with explanations |
| **Mind Maps** | Visual HTML concept maps for grammar topics |
| **Assessment System** | Curriculum-aligned test generation (BEM + A1-B2) |
| **Student Dashboard** | Progress tracking across topics |

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
│   └── mindmap_generator.py        # Visual mind map builder
├── data/topics/                    # Topic JSON files
│   ├── A1.json, A2.json, B1.json, B2.json
├── tests/
│   └── test_core.py                # Unit tests
├── pyproject.toml
├── requirements.txt
└── README.md
```

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

## Author

Mahi Kamel Abdelghani — kamelmahi71@gmail.com

## License

MIT
