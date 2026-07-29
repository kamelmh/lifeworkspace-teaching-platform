# Ed-Tech Roadmap — Dual-Track School System + Taallim

## Executive Summary — One Vision, Two Initiatives

**Mission:** Build *concrete*, AI-powered, bilingual (Arabic / French) education technology for the Algerian market — products that give schools and learners **ownership and lasting value**, not disposable subscription apps.

This roadmap consolidates two threads from earlier working sessions into a single plan:

| # | Initiative | What it is | Stage (as of 28 Jul 2026) |
|---|---|---|---|
| **1** | **Dual-Track School System** *(working name)* | An AI-powered management platform for Algerian private schools that run **both** academic (elementary → BAC) **and** vocational (التكوين المهني) tracks. Grew out of an "MS Access teaching kit" idea. | **SIS MVP built** (13-table Access DB + core forms + seed data) · polished FR/AR mockup + demo kit ready · **demo-gated** (book Allal; remap bulletin) |
| **2** | **Taallim** | An education/learning app (flashcards, MCQ, mind-maps) **+** an academic research paper for the *Multilinguales* journal (ASJP). | **Instruments + analysis complete** · manuscript §1–§3 (EN + FR) · pilot **locked** (2 schools, 1AM–4AM) · **recruitment-gated** |

**The through-line:** both run on the same engine — AI-generated bilingual educational content — and on the same rare founder profile (below). Treated together, Taallim can become the *learning-facing module* of the bigger system, and the research paper becomes *sales credibility*.

> **Current status & the critical path for each track are in the next section (📍).**

## 📍 Current Status & Critical Path (28 Jul 2026)

### Where each track stands

**Taallim paper — instruments DONE; now recruitment-gated.**
- ✅ Manuscript §1–§3 written (EN + FR); grammar-primary / vocabulary-secondary; two-school design.
- ✅ 6 test forms (Grammar A/B/C + Vocabulary A/B/C), A1–B1, counterbalanced, validated & parallel.
- ✅ Teacher questionnaire + interview guide (RQ3).
- ✅ Analysis engine v3 (grammar/55→100, vocab/60→100, H1–H4 + school-robustness) — verified end-to-end.
- ✅ Pilot design locked (D11); specs v3.
- ⛔ **Critical path → secure the two schools + run the ~30-pupil item tryout.** No data can be collected until Allal *and* one El Bayadh public collège commit and consent is in place. Results (§4), Discussion, and submission are all downstream of data.

**Dual-track SIS — MVP built; now demo-gated.**
- ✅ 13-table Access schema; forms (dashboard, student entry, class, grade entry, attendance); seed data; interactive FR/AR mockup; demo kit.
- ⚠️ Bulletin report (Week-3) was specced on the old CC+Compo model — needs remapping to the real ExamType+Grade schema to be demo-solid (S1).
- ⛔ **Critical path → get the demo in front of Allal's director and secure a pilot commitment.** The product is far enough along; the blocker is a booked demo + a clear pricing ask.

### The one move per track this week
1. **Paper:** name and secure the **public collège** (Allal is already the design partner), then schedule the item tryout.
2. **SIS:** lock a **demo date with Allal**, and do the bulletin schema remap just before it.

### Sequencing (solo founder)
Both asks converge on Allal in the same window. Highest-leverage play: **one combined visit to Allal** — run the SIS demo *and* confirm Allal as pilot sitein the same meeting — then chase the public collège separately. The published paper later becomes sales credibility for the SIS; the SIS relationship secures the pilot site. They compound.



### ✅ Locked action plan — 28 Jul 2026 (execution phase; nothing left to author)
**Today (2 sends):**
1. **Direction de l'Éducation** authorisation — fill [adresse] + date, **attach the 1-page protocol summary (PDF) + consent forms**, submit in person or by email.
2. **Allal director message** — fill date, pick a demo slot (this week / next), send by WhatsApp + email.

**This week:**
3. **Name a specific El Bayadh CEM** (nearby, willing English teacher).
4. **Apply the bulletin remap in Access** (`BULLETIN_REMAP.md`) — *first confirm the 5 schema assumptions / that the current seeder writes `ExamType`+`Grade`*, else the bulletin won't match the demo data.
5. **Book the Allal demo** (combined visit: SIS + pilot confirmation).
6. **Print consent forms** (fill [établissement] per school).

**Next 2 weeks:**
7. **~30-student item tryout** on a **non-participating** class (item difficulty / discrimination / KR-20).
8. **Lock final test forms** from the tryout data.
9. **Start the Week-1 pretest** once both schools + consent are secured.

*All authoring is complete; the remaining work is real-world execution. Full kit (both schools, both tracks): roadmap · bulletin remap · pricing (45k DZD) · agenda · printable playbook · consent forms · director message · Direction authorisation + protocol summary.*

## Progress Log

**2026-07-27 (via OpenCode)** — Parallel build: Literature Review drafted (~1,800 words, 27 refs). Decision D10: SIS MVP built in MS Access first. Curriculum Designer blocked until specializations known. Workflow: OpenCode = build · HyperAgent = plan/spec · Obsidian = notes.

**2026-07-27 (later)** — Built the interactive SIS mockup (5 screens, FR⇄AR + RTL, printable bulletin). Placeholder school "El-Amel" → to rebrand to Allal.

**2026-07-27** — Drafted Methodology §3 (standalone); §4/§5 fill-in templates; §6 Conclusion template. Paper shell §1–§6 complete in structure.

**2026-07-27 (Week 1 — OpenCode)** — School confirmed = Allal: 5 levels (1AM→BAC), 4 fields (IT, Commerce, Electricity, Mechanics), 22 specializations, CAP/BEP/BTS. SIS DB = 13 tables via mod_CreateTables.bas + mod_Utils.bas + seed. Q1 (specializations) resolved. Delivered Week-2 Forms Brief.

**2026-07-27 (paper corrections)** — Target language corrected to English (EFL). French §3 translation produced. Compiled EN + FR full manuscripts (with §1/§2 placeholders). Built & tested taallim_analysis.py (auto-generates all §4 tables). Drafted 3 titles + abstract skeleton.

**2026-07-27 (SIS Weeks 2–3)** — Delivered Week-2 forms walkthrough (paste-ready VBA) and Week-3 rptBulletin (queries, report, TermAverage/ClassRank VBA, frmBulletinPicker with PDF export single + whole class). Grade model resolved = CC + Compo → subject mark (CC + Compo×2)/3. Walked through all four forms interactively (frmDashboard done). frmAttendanceRegister completed the MVP feature set.

**2026-07-27 (demo prep)** — Built the Allal SIS Demo Kit (checklist, ~8-min click-through script, one-page value sheet, Q&A). Built mod_SeedDemo.bas (3 classes both tracks, ~30 students, CC/Compo grades, attendance).

**2026-07-27 (bilingual decision — RESOLVED)** — App = bilingual Arabic/French interface; English = target/study language. All HyperAgent docs already consistent; only Kamel's local 03_methodology.md needed the §3.2/§3.4 revert (OpenCode).

**2026-07-27 (paper — GROUND TRUTH + reconciliation)** — Actual §1/§2 uploaded. Study outcome = English GRAMMAR (not vocabulary); RQs = AI-integration / grammar-effectiveness / TEACHER perceptions; setting = El Bayadh, 4 secondary schools, ~120 students + 4 teachers; platform multilingual (Ar/Fr/En), offline, curriculum-aligned (64 grammar topics). Rebuilt + re-exported the EN manuscript (inlined §1/§2 + reconciled §3–§6 + merged 27+6 refs). STILL TO SYNC to grammar/teacher: FR manuscript, standalone §3 (EN+FR), §4/§5 templates, analysis-script labels.

**2026-07-27 (housekeeping)** — Exported EN+FR manuscripts, SIS specs, Week-2/Week-3 walkthroughs, roadmap, and analysis script as Markdown + Word. Repaired the literal-\n rendering glitch in this Progress Log and the Week-3 doc.



**2026-07-27→28 (paper reconciliation — MAJOR)** — Outcome design finalised: GRAMMAR = primary (H1 immediate gain, H2 retention, H3 usage dose–response); VOCABULARY = secondary/exploratory (H4). Both manuscripts (EN + FR) reconciled and mutually consistent (grammar primary, vocabulary secondary, two schools); §3.5/§3.6 rewritten "as built" (EN + FR); TAALLIM_TEST_SPECS → v3 (60 distinct vocabulary words, duplicates removed).

**2026-07-28 (test instruments COMPLETE)** — All 6 achievement-test forms built, validated and made parallel: Grammar A/B/C (55 scored + 5 buffer) and Vocabulary A/B/C (60), each spanning CEFR A1–B1 across 1AM–4AM, counterbalanced for pretest / posttest / delayed. HyperAgent ran a full validation review (coverage, A/B/C difficulty equivalence, distractor quality, cultural fit), caught P0 item bugs plus a file/version mismatch, then rebuilt Grammar Form C and the whole Vocabulary set to a clean 60-distinct-word blueprint (15 words per level). Teacher instruments (RQ3) done: bilingual TAM-based Likert questionnaire + semi-structured interview guide.

**2026-07-28 (analysis engine v3)** — taallim_analysis.py rewritten: ingests raw totals and rescales grammar /55→100 and vocabulary /60→100; grammar-primary (ANCOVA/H1, mixed ANOVA/H2, usage→gain/H3) + vocabulary-secondary (ANCOVA/H4); added a `school` factor and a school-robustness ANCOVA that directly tests the private/public confound. Verified end-to-end on a 120-row synthetic sample.

**2026-07-28 (pilot LOCKED)** — Grade band = 1AM–4AM (all four middle-school levels); site = two schools = Allal (private) + 1 public collège in El Bayadh; ~120 students + 4 teachers; 6-week intervention + 8-week measurement window; intact classes randomly allocated to condition WITHIN each school (removes the private/public confound). Paper cleanup propagated the two-school count through the compiled EN + FR manuscripts (§3.1/§3.3/§3.5/§3.6/§5/§6).

## Founder Profile & Strategic Edge

Your moat is that you combine four things almost no competitor holds at once:

- **Classroom teacher** — taught at a private school (elementary / middle / secondary).
- **School administrator** — worked *inside* administration, so you know the real pain (enrollment, grades, attendance, fees, Ministry reporting).
- **Certified computing instructor** — 6-month certificate تلقين مبادئ الإعلام الآلي (MS Office), qualifying as *agent administrateur*.
- **Database / VBA builder** — built **Academix DSS** (a VBA decision-support system); you can actually *ship* software, not just spec it.
- **Bilingual (Arabic / French)** — can produce localized content in a market where database/ed-tech material is overwhelmingly English-only and generic.

**Reference case:** your former school ("Allal", per prior notes) — a **Ministry-of-Vocational-Training-verified** private school that teaches children academically **and** delivers professional/vocational training. It is simultaneously your design partner and your first customer.

## Initiative 1 — Dual-Track School Management System

### How the idea evolved (narrow → ambitious)
1. **Start:** *"Is there a market for teaching MS Access — something concrete, not just an app people buy once and forget?"*
2. **Product concept:** an **Access Database Starter Kit** — ready-to-use `.accdb` databases + tutorials + VBA automation, sold as *owned* assets.
3. **The real vision (your steer):** stop treating "teaching Access" as the goal and instead **deliver a whole AI-managed system** integrating teachers, administration, and students across **both** academic and vocational tracks, with deep curriculum mapping.

> ⚠️ **Central tension to resolve:** *teaching Access* (a course/kit) vs. *delivering a managed AI platform*. Your latest steer favors the platform — see Decisions (D8) and Open Questions (Q3–Q4).

### Market findings (2026)
| Signal | Finding |
|---|---|
| Tool relevance | MS Access still in active use in 2026; relational DBs ≈ **57%** market share |
| Market size | IT-training market ≈ **$91.85B** (2025), growing **6.2%/yr** |
| Vocational scale (Algeria) | **229** specializations across **20** fields; **291** private vocational schools in Algiers alone |
| Policy tailwind | Gov push for **"skills over volume"**; new **2026 private-school accreditation decree**; **RNFC-2026** framework |
| New 2025–26 specializations | data scientist, 3D graphic design, e-commerce, digital marketing, cybersecurity |
| Competitor gaps | Udemy (57K+ students, 4.8★) = video only · free textbooks = academic, no templates · Tes.com = fragmented · McGraw Hill = US-focused · 130+ templates = generic. **No one offers a complete, Algerian, bilingual, dual-track system.** |

### Product architecture
**A. School-management core (8 modules):** Students · Enrollment · Grades · Attendance · Fees · Staff · Discipline · Inventory.

**B. Curriculum Designer (the core innovation)** — a 4-level engine:
```
FIELD (20) → SPECIALIZATION (229) → MODULE (2,400+) → COMPETENCY (12,000+)
```
| Capability | What it does |
|---|---|
| 229 specs pre-loaded | Every Algerian vocational specialization, ready to use |
| AI generation | "BTS in Cybersecurity, 2 yrs" → modules, competencies, assessment plan; down to weekly lessons |
| RNFC-2026 compliant | New Ministry framework built in |
| Academic ↔ vocational bridges | Links e.g. math → accountancy, physics → electronics |
| Auto Ministry reports | One click → compliance document |
| Custom spec builder | Design new specializations for local market demand |

**The 20 fields (approx. spec counts):** Industry 45+ · Construction 25+ · Electricity 20+ · Mechanics 20+ · IT 15+ · Commerce 15+ · Tourism 10+ · Health 10+ · Agriculture 10+ · Transport 8+ · Textile 8+ · Food 8+ · Arts 8+ · Digital 8+ (new) · Environment 5+ · Chemistry 5+ · Energy 5+ · Security 5+ · Media 5+ · Services 5+.

### Business model (as scoped so far)
*Kit/product pricing (original framing):*
| Product | Price |
|---|---|
| Student Information System | $50–100 |
| Inventory Management Kit | $75–150 |
| School Administration DB | $100–200 |
| CRM for Freelancers | $40–80 |

*Master-plan tiers:* 5 tiers, **$35** (basic) → **$210** (school license). **Year-1 target ≈ 240 sales ≈ $15,000.**

> These numbers reflect the *kit* framing. A managed AI platform likely shifts toward per-school licensing / annual contracts — decide deliberately (Q8).

### Status & artifacts (on your local drive — not yet uploaded here)
- `04_Ideas_&_Projects\MS_Access_School_System\00-MASTER-PLAN.md`
- `...\01-CURRICULUM-DESIGNER.md`

*(I can't read your local drive — re-upload these if you want me to build directly on them.)*

## Initiative 2 — Taallim Platform & Research Paper

### What's built & tested
| File | Purpose | Status |
|---|---|---|
| `taallim_app.py` | Streamlit app, 6 tabs | ✅ Ready |
| `Flashcard_System/flashcard_system.py` | SM-2 spaced repetition | ✅ Tested |
| `MCQ_Generator/mcq_generator.py` | Multiple-choice generator | ✅ Tested |
| `MindMap_Generator/mindmap_generator.py` | Visual concept maps | ✅ Tested |
| `run_taallim.bat` | One-click launcher | ✅ Ready |
| `requirements_taallim.txt` | Dependencies | ✅ Ready |
| `PILOT_EXERCISES.md` | 150+ sample exercises | ✅ Ready |
| `REQUIREMENTS_MAPPING.md` | Ministry requirements mapped | ✅ Complete |

**Run:** `cd ...\10_Education_Project` → `python -m streamlit run taallim_app.py` → `http://localhost:8501`.
*(A prior Unicode/checkmark encoding bug in the MCQ generator was fixed.)*

### The academic paper
- **Target journal:** *Multilinguales* (ASJP — Algerian Scientific Journals Platform). *(spelled "Multilinguelles" in the source.)*
- **Drafted:** introduction (~950 words) + full outline (`ASJP_PAPER_OUTLINE.md`).
- **Planned study:** pilot with **120 students over 6 weeks.**

| # | Paper task | Time | Priority |
|---|---|---|---|
| 1 | Run pilot study (120 students, 6 wks) | 6 wks | High |
| 2 | Draft remaining sections | 2 wks | Medium |
| 3 | Collect & analyze data | 2 wks | Medium |
| 4 | Submit to *Multilinguales* | 1 day | Low |

**Where it stopped:** offered to **test the Streamlit app**, **draft the Literature Review**, or **write the Methodology**.

## Shared Foundations & Synergies

The two initiatives share an engine and can feed each other — one ecosystem, not two disconnected products:

| Shared asset | In the School System | In Taallim |
|---|---|---|
| AI content generation | Curriculum / module / lesson generation | Flashcards, MCQs, mind-maps, exercises |
| Bilingual (Ar/Fr) pipeline | Ministry-facing curricula & reports | Learning content & the paper |
| Spaced repetition (SM-2) | Student learning module inside the ERP | Core of the app |
| Pedagogical credibility | Sales proof to schools | The research paper = academic validation |
| Your former school | First ERP customer / design partner | Pilot site for the 120-student study |

> **Strategic play:** make **Taallim the learning-facing module** of the school system, and use the **published paper as third-party validation** during school sales.

## Decisions Made

| # | Decision | Status |
|---|---|---|
| D1 | Build *concrete*, ownership-based products — not disposable subscription apps | ✅ Firm principle |
| D2 | Target market = Algerian private schools, bilingual Arabic/French | ✅ Firm |
| D3 | Anchor on a **dual-track** (academic + vocational) system — a genuine market gap | ✅ Firm |
| D4 | Curriculum Designer (229 specs, RNFC-2026, AI-generated) is the core differentiator | ✅ Firm |
| D5 | Lead with your former school as design partner + first customer | ✅ Firm |
| D6 | Taallim core components built in Python/Streamlit and validated by tests | ✅ Done |
| D7 | Publish a research paper in *Multilinguales* (ASJP) for credibility | ✅ Committed |
| D8 | Shift emphasis from "teaching MS Access" → "delivering a managed AI system" | 🔄 Leaning, not finalized |
| D9 | Pricing model (one-off kit vs. per-school license) | ❓ Open (see Q8) |


| D10 | **Grammar = primary outcome (H1–H3); vocabulary = secondary/exploratory (H4)** | ✅ Firm |
| D11 | **Pilot locked: 1AM–4AM; two schools — Allal (private) + 1 public collège (El Bayadh); ~120 students + 4 teachers; within-school random allocation of intact classes** | ✅ Firm |
| D12 | **Instruments + analysis complete: 6 parallel A1–B1 test forms, teacher questionnaire + interview guide, analysis script v3 (grammar/55→100, vocab/60→100)** | ✅ Done |
| D13 | **Ship the SIS Student-Information-System wedge first; validate with Allal before building the remaining modules** | ✅ Firm |

## Open Questions

*Updated 28 Jul 2026. Resolved items struck through; live questions grouped by track.*

**✅ Resolved since first draft**
- ~~Q1 — What specializations does Allal offer?~~ → Known: 4 fields (IT, Commerce, Electricity, Mechanics), 22 specializations, CAP/BEP/BTS.
- ~~Q2 — Taallim next step (test app / lit review / methodology)?~~ → Paper is well past this: §1–§3 written, instruments + analysis complete.
- ~~Pilot site & grade band?~~ → Locked (D11): 1AM–4AM, Allal + 1 public collège.
- ~~Grammar vs. vocabulary as the outcome?~~ → Grammar primary, vocabulary secondary/H4 (D10).
- ~~MVP module / wedge?~~ → Student Information System (D13).

**🔴 Paper — live**
- **P1. Which public collège in El Bayadh?** Must be named and its director's agreement secured — this gates the entire pilot.
- **P2. Ethics & consent.** Finalise guardian + student + teacher consent forms (Ar/Fr) and confirm the approval route (school / Ministry / university affiliation).
- **P3. Item tryout.** Run the ~30-pupil tryout (non-participating class) for item difficulty / discrimination / KR-20 *before* the Week-1 pretest — when and where?
- **P4. References & abstract.** A few entries still use "et al." and need full APA author lists; final check of the trilingual abstract (AR).

**🔴 SIS — live**
- **S1. Bulletin schema remap.** The Week-3 bulletin queries/VBA were written for CC + Compo + Coefficient, but the real schema is ExamType + Grade + Hours — remap before the bulletin is demo-solid.
- **S2. Demo date.** When does the click-through actually get in front of Allal's director?
- **S3. Pricing** (was Q8): one-off owned license vs. per-school annual — set a number *before* the demo ask.
- **S4. Curriculum Designer slice.** Load Allal's 22 real specializations to show a live slice at the demo.

**⚪ Strategic — still open**
- **Platform vs. owned/offline** (Q3/Q10): the MVP is Access/owned; decide the scale path (hosted-AI vs. hybrid) deliberately rather than by default.
- **Solo-founder sequencing** (Q9): the paper pilot and the SIS demo compete for the same weeks — sequence intentionally (see Critical Path).
- **Compliance** (Q6/Q7): 2026 accreditation decree requirements + mandatory Ministry report formats/cadence.

## Unified Roadmap & Next Steps

### ✅ Done since first draft
Allal specializations known (Q1) · Taallim paper past "next step" (Q2) · outcome set: grammar primary / vocab secondary (D10) · pilot locked: 2 schools, 1AM–4AM (D11) · 6 test forms + teacher instruments + analysis v3 (D12) · SIS MVP + mockup + demo kit built · manuscripts (EN + FR) reconciled and consistent.

### ⚡ This week — the two gates (detail in 📍 Critical Path)
- [ ] **Paper:** name + secure the El Bayadh **public collège**; schedule the ~30-pupil **item tryout**; finalise **consent** forms (Ar/Fr).
- [ ] **SIS:** book the **Allal demo**; **remap the bulletin** to the real ExamType+Grade schema (S1); set the **pricing** ask (S3).

### Phase — Pilot & Demo (next ~2–4 weeks)
- [ ] One combined Allal visit: run the SIS demo *and* confirm Allal as pilot site #1.
- [ ] Item tryout → lock final forms → begin Week-1 pretest once both schools + consent are ready.
- [ ] Capture the school's change list from the demo.

### Phase — Data & Build-out (~weeks 4–12)
- [ ] 6-week intervention → Week-6 posttest → Week-8 delayed → run `taallim_analysis.py` → fill §4 → finish Discussion + Conclusion → **submit to *Multilinguales***.
- [ ] SIS: bulletin remap; load Allal's 22 real specializations (Curriculum Designer slice); add remaining modules; produce one auto Ministry report.

### Phase — Go-to-market
- [ ] Use the published paper as sales credibility; approach more private schools; finalise pricing/packaging.

## Risks & Considerations

| Risk | Note / mitigation |
|---|---|
| **Scope creep** | The vision grew from "Access kit" to "full AI ERP." Ship the SIS wedge first; don't build all 8 modules before validation. |
| **Solo bandwidth** | Two initiatives + a paper is heavy for one person. Sequence: prototype SIS → validate → expand; let the Taallim pilot double as validation. |
| **Regulatory** | The 2026 accreditation decree + Ministry reporting rules may shift requirements — confirm early (Q6/Q7). |
| **"Concrete vs AI" tension** | Owned/offline (Access) vs. hosted AI platform pull opposite ways; a hybrid (local app + optional AI assist) can satisfy both. |
| **AI reliability** | AI-generated curricula must be checked against RNFC-2026 — keep a human-in-the-loop review step. |
| **Single-customer dependency** | Your former school is design partner *and* first customer; validate with 1–2 more schools before over-fitting. |
| **Monetization** | $15K Year-1 (kit) is modest; a per-school license model may be more sustainable if you choose the platform route. |


---

Linked from: [[00-MOC-Education]]