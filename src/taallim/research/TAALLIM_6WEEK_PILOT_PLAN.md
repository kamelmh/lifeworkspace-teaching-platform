# Ta'allim — 6-Week Pilot Plan (2 Schools)

## 0 · Site & scope (LOCKED)

**Pilot site — LOCKED:** two schools in El Bayadh:
- **Allal** (private vocational) — you're known there; easy access; private setting
- **1 public collège** in El Bayadh — public setting; standard middle-school context

This gives private + public representation while keeping recruitment manageable. Manuscript §1.6/§3.3 already updated to match.

**Scope discipline:** the platform is *designed* for all three cycles, but this pilot **empirically validates the middle-school level only**. Every results/claim sentence stays middle-school-scoped; primary/secondary = planned extensions.

**Outcome:** grammar = primary (H1 immediate, H2 retention, H3 dose–response); vocabulary = secondary/exploratory (H4). Target content: 60 grammar structures + 60 vocabulary items.

## 1 · Participants & assignment

- **~120 middle-school students** (Arabic L1; EFL) in intact classes; assign **at the class level** to **Experimental** (Ta'allim) vs **Control** (traditional), aiming ~60/60.
- **4 teachers** (RQ3) — the ones teaching the participating classes.
- Record demographics (age, gender, prior English exposure, device access) + a short placement check.
- Because assignment is by class/school (clustering), note it as a design constraint; inspect intraclass correlation and report a multilevel robustness check if material.
- **Baseline equivalence:** confirm no pretest difference between groups (independent-samples *t*).

## 2 · Ethics & consent

- Secure **institutional approval** from the school director(s) before Week 1.
- **Informed consent:** guardian consent + student assent (minors), and **separate teacher consent**.
- Bilingual (Arabic/French) consent forms; voluntary participation; right to withdraw without penalty.
- **Data protection:** anonymise (use matricule-style codes, not names, in the dataset); store securely; offline where possible.
- **Equity:** give the control group access to Ta'allim after the delayed post-test.

## 3 · Instruments (prepare before Week 1)

- **Grammar test (primary)** — 3 counterbalanced parallel forms (A/B/C) over the targeted grammar structures; expert-validated; pilot-tested on ~30 non-participants for difficulty/discrimination + form equivalence; report KR-20 / Cronbach's α (≥ .70).
- **Vocabulary test (secondary)** — parallel forms over the 60 target items (receptive + productive).
- **Teacher questionnaire** (adoption / satisfaction / perceived utility, Likert) + **semi-structured interview guide**, in Arabic/French.
- **Usage analytics** exported from Ta'allim (items reviewed, session regularity, MCQ accuracy, maps).
- ⚠️ Getting the parallel-form tests written + validated is the critical-path item — start it now (I can draft the item specs).

## 4 · Week-by-week timeline

| Week | Activity |
|---|---|
| **Wk 0 (prep)** | Ethics approval; consent collected; devices/Ta'allim installed; teacher training (~1–2 h); orientation for the experimental classes |
| **Wk 1** | **Pretest** (grammar + vocabulary, Form A) + baseline questionnaire, both groups |
| **Wks 2–5** | **Intervention:** experimental group uses Ta'allim ~4 sessions/wk (20–25 min) on the shared target content; control covers the *same* content by traditional instruction, equal time. Log usage + teacher session notes |
| **Wk 6** | **Immediate post-test** (Form B), both groups; **teacher questionnaire + interviews** |
| **Wk 8 (Wk 6 + 2)** | **Delayed post-test** (Form C), both groups; no Ta'allim access in the interim |

*Total: 6-week programme + a 2-week retention gap.*

## 5 · Data collection & entry

- Enter scores into the **wide CSV** `taallim_analysis.py` expects — one row per student: `student_id, group, pretest, posttest, delayed`, usage columns for the experimental group, and questionnaire subscales.
- Keep grammar and vocabulary as **two datasets** (same structure) so each runs through the script independently (grammar = primary, vocabulary = H4).
- Anonymise IDs at entry. Double-key or spot-check ~10% of entries for accuracy.
- Transcribe teacher interviews promptly (Wk 6–7).

## 6 · Analysis (uses the script you have)

- Run `taallim_analysis.py` on the grammar dataset → §4.1 descriptives/assumptions, §4.2 ANCOVA (H1), §4.3 mixed ANOVA (H2); repeat on the vocabulary dataset → §4.3b (H4). Usage→gain correlations/regression inform H3.
- Teacher questionnaire + interviews → **reflexive thematic analysis** (RQ3).
- Paste the generated tables into §4; write §5 interpretation against your cited literature; finalise §6.
- Report effect sizes (partial η², Cohen's *d*) + 95% CIs; α = .05.

## 7 · Risks & contingencies

| Risk | Mitigation |
|---|---|
| School approval slips | Have the outreach + demo ready; propose a single-class minimum viable pilot |
| Attrition / absences | Over-recruit slightly; use available-case analysis + report attrition |
| Unequal content/time between groups | Give control the *same* target items and equal minutes; document it |
| Test practice effects | Counterbalanced parallel forms A/B/C |
| Novelty/Hawthorne | Acknowledge as a limitation; keep control engaged normally |
| Device/connectivity gaps | Ta'allim runs offline — confirm on the school's machines in Wk 0 |

## 8 · Timeline to submission

- **Now → Wk 0:** lock the site, secure approval, build + validate the tests, run the outreach/demo.
- **Wks 1–8:** run the pilot (above).
- **Wks 9–10:** analyse, populate §4/§5/§6, finalise trilingual abstracts + references.
- **Wk 10–11:** internal proofread (FR fluency pass already done), format to *Multilinguales* style, submit via ASJP.

**Critical path = school approval + validated tests.** Both can start today; the 6-week clock only begins once they're in place.


---

Linked from: [[00-MOC-Education]]