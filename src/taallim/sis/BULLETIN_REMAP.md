# SIS — rptBulletin remap to the REAL schema (ExamType + Grade + Hours)

*Rewrites the Week-3 bulletin queries + VBA from the old **CC+Compo+Coefficient+TermID** model to the confirmed real schema: `tblGrade` = **ExamType + Grade**, `tblModule` = **Hours** (no Coefficient), **no `tblTerm`** (term/year live in `tblConfig`), `tblClass` = ClassName/SpecID/AcademicYear (no `Track`), `tblStudent.DateOfBirth`. Only the schema-dependent parts change; the report *layout* (§3 of the original) stays, with three textbox-expression swaps noted in §4.*

---

## 0 · ⚠️ Confirm these 5 things before piloting the remap

The remap is built on the schema you documented, but these specifics weren't in any file I can read. Confirm (or paste `mod_CreateTables.bas` and I'll lock them exactly):

1. **ExamType values** — I assume `tblGrade.ExamType` holds the strings **`"CC"`** and **`"Compo"`**, one row of each per student×module. If they're `"Contrôle"`/`"Composition"` (or there can be several CC rows), tell me — the pivot in §1 adapts in one place.
2. **Term/period** — I assume the DB holds **one active term** and `tblGrade` has **no** term column (so no term filter; the term label is read from `tblConfig`). If `tblGrade` has a `Period`/`TermLabel` column, it goes back into the `WHERE`.
3. **Module weight** — I use **`tblModule.Hours`** as the coefficient. Confirm there's no separate `Coefficient` (if there is, swap the field name in §2/§3 — one spot each).
4. **Academic vs Vocational** — real `tblClass` has no `Track`, so I derive it as **`SpecID Is Null → Academic, else Vocational`**. Confirm academic classes have a null `SpecID` (and are linked by level).
5. **tblConfig shape** — I assume a key/value table with columns **`SettingKey` / `SettingValue`** and keys **`CurrentTerm`**, **`CurrentYear`**. Tell me the real column/key names if different.

> **Seeder consistency (10-second check):** open your *current* `mod_SeedDemo.bas` and confirm it writes `tblGrade` rows as `ExamType` + `Grade` (not `CC`/`Compo`). If it still writes `CC`/`Compo`, the DB won't match this bulletin — resync the seeder first. (The copy in HyperAgent's workspace is the old one; don't use it as reference.)

---

## 1 · NEW helper — `qryGradeMark` (pivot ExamType rows → CC/Compo columns)

Because a subject's two marks are now **two rows** (`ExamType`), first fold them back into one row per student×module. Save as **`qryGradeMark`**:

```sql
SELECT g.StudentID, g.ModuleID,
       Avg(IIf(g.ExamType='CC',    g.Grade, Null)) AS CC,
       Avg(IIf(g.ExamType='Compo', g.Grade, Null)) AS Compo
FROM tblGrade AS g
GROUP BY g.StudentID, g.ModuleID;
```
`Avg(IIf(...))` ignores Nulls, so this also handles a module with **several** CC entries (their mean) and a single Compo. If a mark type is missing, its column is Null.

---

## 2 · Helper — `qryGradeWeighted` (replaces `qryGradeCoef`)

Exposes each subject's computed **Mark** next to its **Weight = Hours**, for the average/rank functions. Save as **`qryGradeWeighted`**:

```sql
SELECT gm.StudentID, gm.ModuleID,
       ((gm.CC + gm.Compo*2)/3) AS Mark,
       m.Hours AS Weight
FROM qryGradeMark AS gm
INNER JOIN tblModule AS m ON gm.ModuleID = m.ModuleID
WHERE gm.CC Is Not Null AND gm.Compo Is Not Null;
```
Subject mark rule **(CC + Compo×2)/3** lives here (and in §3) — change it once if your school weights differently. The `WHERE` keeps partially-graded subjects out of the weighted mean so numerator and denominator stay aligned.

---

## 3 · Report source — `qryBulletin` (real schema; no TermID; Track derived; Hours weight)

Drives the report detail rows, filtered to the student chosen on the picker. Save as **`qryBulletin`**:

```sql
SELECT s.StudentID, s.Matricule,
       s.LastName_fr, s.FirstName_fr, s.LastName_ar, s.FirstName_ar,
       c.ClassName,
       IIf(c.SpecID Is Null, "Academic", "Vocational") AS Track,
       m.Name_fr AS Subject, m.Name_ar AS SubjectAr,
       m.Hours AS Weight,
       gm.CC, gm.Compo,
       ((gm.CC + gm.Compo*2)/3) AS Mark,
       (((gm.CC + gm.Compo*2)/3) * m.Hours) AS WeightedPoints
FROM ((((qryGradeMark AS gm
     INNER JOIN tblModule AS m ON gm.ModuleID = m.ModuleID)
     INNER JOIN tblStudent AS s ON gm.StudentID = s.StudentID)
     INNER JOIN tblEnrollment AS e ON s.StudentID = e.StudentID)
     INNER JOIN tblClass AS c ON e.ClassID = c.ClassID)
WHERE gm.StudentID = [Forms]![frmBulletinPicker]![cboStudent];
```
Changes vs. the old query: no `tblTerm` join and **no `TermID` filter** (single active term); **`Track` is derived** from `SpecID`; the weight column is **`Hours`** (aliased `Weight`); marks come from the `qryGradeMark` pivot. It drives the report from subjects that have grades — if you want ungraded subjects to appear as blank rows, we need the class→module list (depends on how modules attach to classes; tell me and I'll add it).

---

## 4 · Report layout — three expression swaps only

The original §3 layout stands. Update just these controls (they referenced `Coef`/`TermID`/`cboTerm`):

- **Weight column** — bind the old *Coef* textbox to **`Weight`** (label it *Coef.* / *المعامل* as before; it now shows hours-as-coefficient).
- **General average** `txtGeneralAvg` → `=Sum([WeightedPoints])/Sum([Weight])` (was `/Sum([Coef])`).
- **Rank** `txtRank` → **`=ClassRank([StudentID])`** (TermID param dropped — §5).
- **Title** `txtTitle` → **`="Bulletin de Notes — " & CfgValue("CurrentTerm")`** (was `& cboTerm`).
- **Footer avg (exact match to rank)** — if you bind the footer to VBA, use **`=TermAverage([StudentID])`**.

Unchanged: the Ministry line still keys off `[Track]` (`=IIf([Track]="Vocational","Ministère de la Formation et de l'Enseignement Professionnels","Ministère de l'Éducation Nationale")`), the appreciation/mention/decision expressions, and the RTL settings.

---

## 5 · VBA — drop TermID; add a tblConfig reader

Replace the old `TermAverage`/`ClassRank` and add `CfgValue` (standard module, e.g. `mod_Utils`):

```vba
Public Function CfgValue(ByVal pKey As String) As String
    CfgValue = Nz(DLookup("SettingValue", "tblConfig", "SettingKey='" & pKey & "'"), "")
End Function

Public Function TermAverage(ByVal pStudentID As Long) As Double
    Dim tp As Variant, tc As Variant
    tp = DSum("[Mark]*[Weight]", "qryGradeWeighted", "StudentID=" & pStudentID)
    tc = DSum("[Weight]",        "qryGradeWeighted", "StudentID=" & pStudentID)
    If Nz(tc, 0) = 0 Then TermAverage = 0 Else TermAverage = Nz(tp, 0) / tc
End Function

Public Function ClassRank(ByVal pStudentID As Long) As String
    Dim clsID As Long, myAvg As Double, better As Long, total As Long
    Dim rs As DAO.Recordset
    clsID = Nz(DLookup("ClassID", "tblEnrollment", "StudentID=" & pStudentID), 0)
    If clsID = 0 Then ClassRank = "-": Exit Function
    myAvg = TermAverage(pStudentID)
    Set rs = CurrentDb.OpenRecordset( _
        "SELECT StudentID FROM tblEnrollment WHERE ClassID=" & clsID, dbOpenSnapshot)
    Do While Not rs.EOF
        If TermAverage(rs!StudentID) > myAvg Then better = better + 1
        total = total + 1
        rs.MoveNext
    Loop
    rs.Close
    ClassRank = (better + 1) & " / " & total
End Function
```
Only change vs. the old code: the **`TermID` parameter is gone** everywhere (single active term), and the weight field is **`Weight`** (Hours) from `qryGradeWeighted`.

---

## 6 · Picker form + PDF export (`frmBulletinPicker`)

Drop `cboTerm` (or make it a read-only label = `CfgValue("CurrentTerm")`). Combos: `cboClass` (from `tblClass`, display `ClassName`), `cboStudent` (from `tblStudent`, optionally filtered by `cboClass`).

```vba
Private Sub cmdPreview_Click()
    If IsNull(Me.cboStudent) Then MsgBox "Choisir un élève.", vbExclamation: Exit Sub
    DoCmd.OpenReport "rptBulletin", acViewPreview
End Sub

Private Sub cmdExportPDF_Click()
    Dim mat As String, fnm As String
    If IsNull(Me.cboStudent) Then MsgBox "Choisir un élève.", vbExclamation: Exit Sub
    mat = Nz(DLookup("Matricule", "tblStudent", "StudentID=" & Me.cboStudent), Me.cboStudent)
    fnm = CurrentProject.Path & "\Bulletin_" & mat & ".pdf"
    DoCmd.OutputTo acOutputReport, "rptBulletin", acFormatPDF, fnm, True
    MsgBox "Bulletin exporté : " & fnm
End Sub

Private Sub cmdExportClass_Click()
    Dim rs As DAO.Recordset, folder As String, mat As String, fnm As String
    If IsNull(Me.cboClass) Then MsgBox "Choisir une classe.", vbExclamation: Exit Sub
    folder = CurrentProject.Path & "\Bulletins_" & Replace(Nz(CfgValue("CurrentTerm"), "T"), " ", "_") & "\"
    If Dir(folder, vbDirectory) = "" Then MkDir folder
    Set rs = CurrentDb.OpenRecordset( _
        "SELECT StudentID FROM tblEnrollment WHERE ClassID=" & Me.cboClass, dbOpenSnapshot)
    Do While Not rs.EOF
        Me.cboStudent = rs!StudentID: Me.Refresh: DoEvents
        mat = Nz(DLookup("Matricule", "tblStudent", "StudentID=" & rs!StudentID), rs!StudentID)
        fnm = folder & "Bulletin_" & mat & ".pdf"
        DoCmd.OutputTo acOutputReport, "rptBulletin", acFormatPDF, fnm, False
        rs.MoveNext
    Loop
    rs.Close
    MsgBox "Bulletins générés dans : " & folder
End Sub
```

---

## 7 · Done-when

- [ ] `qryGradeMark` returns one row per student×module with sensible `CC`/`Compo` from the `ExamType` rows.
- [ ] Pick a student → **Preview** shows subjects, the **Hours-weighted** general average, correct **rank**, and mention.
- [ ] **Export PDF** writes `Bulletin_<matricule>.pdf`; **Export class** writes one per enrolled student.
- [ ] Ministry line flips correctly for an academic vs. a vocational class (via derived `Track`).
- [ ] The 5 assumptions in §0 are confirmed against `mod_CreateTables.bas`, and the current seeder writes `ExamType`/`Grade`.


---

Linked from: [[00-MOC-Education]]