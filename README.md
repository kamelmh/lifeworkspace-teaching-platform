# SIS Prototype — Student Information System

**Version:** 1.0  
**Date:** 2026-07-31  
**Status:** Working Prototype

## Overview

A Streamlit-based Student Information System (SIS) prototype for Algerian public schools. Part of the Ta'allim Education Project.

## Features

### 📊 Dashboard
- Student count by level
- Recent grade activity
- System overview

### 👨‍🎓 Student Management
- Add/edit/delete students
- Filter by level (1AM-4AM)
- Track demographics and contact info

### 📚 Class Management
- Create classes by level
- Assign teachers
- Track schedules and rooms

### 📝 Assessment Engine
- Create grammar/vocabulary assessments
- Set time limits and point values
- Exercise Generator integration (coming soon)

### 📈 Grade Book
- Enter grades per student/assessment
- View grade history
- Calculate percentages

### ⚙️ Settings
- Export data (JSON)
- Clear all data

## Data Storage

All data stored in JSON files in `data/` directory:
- `students.json` — Student records
- `classes.json` — Class definitions
- `assessments.json` — Assessment templates
- `grades.json` — Grade entries

## Installation

```bash
pip install streamlit
```

## Usage

```bash
cd C:\Users\Admin\My Drive\LifeWorkspace\10_Education_Project\SIS_Prototype
streamlit run app.py
```

Then open http://localhost:8501

## Integration Points

### Exercise Generator
- Import exercises from Exercise Generator
- Auto-populate question banks
- Generate tests from topic selection

### Ta'allim Tests
- Link assessments to Ta'allim pilot
- Track student performance on 60 grammar structures
- Generate progress reports

### BTS Knowledge Base
- Connect to BTS course data
- Map curriculum to assessments
- Track student mastery

## Next Steps

1. **Exercise Generator API** — Connect to Exercise Generator module
2. **PDF Export** — Generate printable reports
3. **Multi-user Support** — Teacher/admin roles
4. **Cloud Deployment** — Streamlit Cloud or Heroku

## Architecture

```
SIS_Prototype/
├── app.py              # Main Streamlit app
├── data/               # JSON data storage
│   ├── students.json
│   ├── classes.json
│   ├── assessments.json
│   └── grades.json
└── README.md
```

## Part of Ta'allim Education Project

- **Exercise Generator:** 72 topics, 3 exercise types
- **Ta'allim Tests:** 60 grammar structures, 3 parallel forms
- **SIS:** Student tracking and assessment management

---

**Contact:** MAHI Kamel Abdelghani (kamelmahi71@gmail.com)
