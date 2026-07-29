# Allal SIS — Demo Kit (Click-through + Talking Points)

*Demo kit for presenting the SIS to Allal: pre-demo checklist, a timed click-through script (run on the interactive mockup), a one-page value/talking-points sheet, and likely-questions answers.*

---

## Pre-demo checklist (5 minutes before)

- [ ] **Rebrand the mockup to Allal** first (name + logo/colours) so it reads as *their* system, not a generic sample.
- [ ] Open the **interactive mockup full-screen** in a browser, resting on the **Dashboard**. It's your most polished, finished-looking asset — demo from it.
- [ ] Know where the **FR ⇄ ع language toggle** is (top-right). This is your first "wow."
- [ ] **Pre-pick two students** to contrast the dual track: one **academic** (e.g., a 1AS student) and one **vocational** (e.g., a BTS Informatique student).
- [ ] **Test Print / PDF once** beforehand so the bulletin export is smooth on the day.
- [ ] (Optional) Have the **Access build** open in the background — you'll point to it at the close as proof this becomes a real app they *own*.
- [ ] **Print the one-page value sheet** (below) to leave behind.
- [ ] Decide your **ask** in advance (a one-trimester pilot with 1–2 classes).

---

## Click-through script (~8 minutes)

*Format: **[DO]** = what to click · **[SAY]** = the line. Build toward the bulletin PDF — that's the moment that sells it.*

**1. Open on the Dashboard — the whole school at a glance (~45s)**
[DO] Land on the dashboard; point to the KPI tiles and the **Academic / Vocational split** donut.
[SAY] *"This is your whole school on one screen — students, classes, today's attendance. And notice it already separates your two tracks: academic and vocational. Hold that thought."*

**2. Flip the language — Arabic, instantly (~30s)**
[DO] Click **FR ⇄ ع**; the interface flips to Arabic, right-to-left.
[SAY] *"One click — the entire system works in Arabic or French, however your teachers and parents prefer. It's built for how Algerian schools actually run, not translated as an afterthought."*

**3. A student's full record (~1 min)**
[DO] Go to **Élèves**, search a name, open the profile.
[SAY] *"Every student in one place — bilingual record, their trimester average, attendance, all live. No more chasing paper files or scattered spreadsheets."*

**4. The dual-track moment — your differentiator (~2 min)**
[DO] Open the **academic** student's bulletin, then the **vocational** student's bulletin.
[SAY] *"Watch what happens. For an academic student, the report card shows subjects and coefficients. For a vocational student, it shows their training **modules** — and even the Ministry line at the top changes to the right ministry. One system runs both your tracks. Most school software does one or the other; this was built for a school like yours that does both."*

**5. Grades enter themselves into the maths (~1 min)**
[DO] Open **Saisie des notes**; type a couple of marks.
[SAY] *"Teachers just enter the contrôle and composition. The subject average, the class average — all calculated instantly, out of 20, with your coefficients. A mark over 20 is simply refused."*

**6. THE WOW — the bulletin, in one click (~2 min)**
[DO] Open a **bulletin**; point to the **weighted general average, class rank, mention**; then click **Imprimer / PDF**.
[SAY] *"Here's the report card — weighted average, rank in class, mention — in the official Algerian format, generated in one click. And it does a **whole class at once**. The hours your staff spend every trimestre computing averages and writing bulletins by hand? Seconds."*

**7. Close — and it's yours (~1 min)**
[DO] (Optional) gesture to the Access build in the background.
[SAY] *"This isn't a website you rent. It becomes an application that lives on your machines, works offline, and belongs to Allal — no subscription, yours to keep and adapt. I built it because I taught here and did the admin here; I know exactly what you need. I'd love to pilot it with one or two classes this trimestre and build it around your feedback."*

---

## One-page value sheet (talking points)

### A management system built *for* Allal — academic + vocational, bilingual, owned.

**The problem you know too well**
Every trimestre: hours computing averages and writing bulletins by hand; grades, attendance and fees scattered across notebooks and spreadsheets; two tracks — academic *and* vocational — tracked separately; Ministry paperwork done from scratch.

**The solution**
One Student Information System that runs your whole school — **Students · Enrollment · Grades · Attendance** — and generates official, bilingual **report cards automatically**.

**Why this one**
1. **Dual-track by design** — academic (1AM → BAC) *and* vocational (4 fields, 22 specializations, CAP/BEP/BTS) in a single system. Rare — most tools do only one.
2. **Bilingual & Algerian** — Arabic/French, right-to-left, marks /20, trimestres, coefficients, matricule, and the familiar bulletin layout.
3. **Bulletins in one click** — weighted average, class rank, mention, exported to PDF for a whole class in seconds — not hours.
4. **You own it** — a Microsoft Access application on *your* machines, **offline, no subscription**, yours to keep and customize.
5. **It grows** — auto Ministry reporting and an AI Curriculum Designer are the next steps.

**Who's behind it**
Kamel Mahi — taught and worked in administration *at Allal*, certified in MS Office instruction, and the builder of *Academix DSS*. This is built by someone who has sat in your chair.

**The ask**
Run a **one-trimestre pilot** with one or two classes. If your staff say *"we need this,"* we scale it — shaped by your feedback.

---

## Likely questions & answers

- **"How much does it cost?"** → *"It's a one-time, affordable price — you own the software, no monthly subscription. Let's agree scope from the pilot, then price it fairly."* (Set your number in advance.)
- **"Is our data safe?"** → *"It stays on your own computers — offline, no cloud required. You control who has the file."*
- **"Will staff need training?"** → *"The forms are simple and bilingual. I'll do a short handover and I'm local — I know the school."*
- **"What if you're not available later?"** → *"You own the file; it's standard Microsoft Access, and it's documented. You're not locked to me."*
- **"Can it handle Ministry reports?"** → *"That's the very next module — the system already separates the two tracks, which is what Ministry reporting needs."*
- **"Does it really do both academic and vocational?"** → *"Yes — I'll show you both report cards live. That's the part no one else offers."*
- **"Can we start small?"** → *"Exactly what I'm proposing — one trimestre, one or two classes."*


---

## 5 · Demo-day readiness runbook

Work top to bottom. Three go/no-go gates at the end decide if you're ready.

**Phase 1 — Data check (~15 min)**
- [ ] Back up the master `.accdb` first (dated copy + USB).
- [ ] Ctrl+G → `Call SeedDemoData` → confirm the prompt.
- [ ] Open **frmDashboard** → ~30 students, 3 classes, an attendance %.
- [ ] Open **frmBulletinPicker** → academic class + Trimestre 1 → **Preview**: marks, weighted average, class rank sensible → then a **vocational** class → bulletin adapts (modules + right ministry).
- [ ] **Export class** → a folder of PDF bulletins; keep it as a day-of fallback.
- ⚠️ **If SeedDemoData errors:** almost certainly a field-name mismatch. Fix the flagged names in `mod_SeedDemo`, or send `mod_CreateTables.bas` for an exact-match rewrite. Never demo on empty tables.

**Phase 2 — Packaging (~20 min)**
- [ ] Debug ▸ Compile → no errors.
- [ ] Startup: Application Title, Display Form = frmDashboard, untick Display Navigation Pane, tick Compact on Close.
- [ ] Close & reopen → launches to dashboard, no nav pane. (Shift on open = your way back in.)
- [ ] Make ACCDE → test it launches clean and a bulletin exports.
- [ ] Trusted Location on the laptop; USB with master `.accdb` + `.accde` + PDF fallback.

**Phase 3 — Rehearsal (~30 min)**
- [ ] Run the click-through twice, aloud, timed (~8 min). Slow on the Arabic toggle and the one-click bulletin.
- [ ] Drill **cost** and **teacher-workload** answers cold.
- [ ] Print the value sheet; lock the pilot ask.
- [ ] Primary surface = the rebranded Allal mockup; the `.accde` is your "you own this" proof.

**✅ Go / no-go gates — all three green:**
1. A bulletin previews correctly with real-looking seeded data.
2. The `.accde` launches clean on the demo laptop.
3. You can answer **cost** and **teacher workload** in one crisp sentence each.


---

Linked from: [[00-MOC-Education]]