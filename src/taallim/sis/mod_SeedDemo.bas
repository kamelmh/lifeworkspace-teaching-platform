Attribute VB_Name = "mod_SeedDemo"
Option Compare Database
Option Explicit

' ============================================================================
'  mod_SeedDemo  —  load convincing demo data into SIS_MVP_Allal.accdb
'  Run from the Immediate window (Ctrl+G):   Call SeedDemoData
'  Safe to re-run: it clears the dynamic tables first, then reloads.
'
'  >>> FIELD-NAME MAP — edit these if your schema differs <<<
'  Tables used: tblTeacher, tblClass, tblStudent, tblEnrollment,
'               tblModule, tblGrade, tblAttendance (+ tblAcademicYear/tblTerm
'               or tblConfig, tblLevel, tblSpecialization, tblDiploma).
'  Assumed key fields:
'    tblStudent : Matricule, LastName_fr, FirstName_fr, LastName_ar,
'                 FirstName_ar, Gender, DOB, PlaceOfBirth, GuardianName,
'                 GuardianPhone, Status            ' <- if yours is EnrollStatus, change SF_STUDSTATUS
'    tblClass   : YearID, LevelID, Name, Track, SpecializationID, DiplomaID, Capacity
'    tblModule  : Name_fr, Name_ar, Coefficient, SpecializationID
'    tblGrade   : StudentID, ModuleID, TermID, CC, Compo
'    tblAttendance: StudentID, ADate, Session, Status
'    tblEnrollment: StudentID, ClassID, YearID, EnrollDate, Status
'  If a table/field name differs, adjust it once here or in the AddNew blocks.
' ============================================================================

Private Const SF_STUDSTATUS As String = "Status"   ' tblStudent status field name
Private Const CUR_YEAR As String = "2026-2027"

' ---- Algerian name pools (Fr | Ar paired by index) ------------------------
Private mLastFr As Variant, mLastAr As Variant
Private mMFr As Variant, mMAr As Variant
Private mFFr As Variant, mFAr As Variant
Private mPOB As Variant

Private Sub InitPools()
    mLastFr = Array("Benali", "Kaddour", "Bouzid", "Cherif", "Meziane", "Brahimi", _
                    "Zerrouki", "Haddad", "Saidi", "Toumi", "Belkacem", "Mansouri")
    mLastAr = Array(ChrW(1576) & ChrW(1606) & " " & ChrW(1593) & ChrW(1604) & ChrW(1610), _
                    "قدور", "بوزيد", "شريف", "مزيان", "براهيمي", _
                    "زروقي", "حداد", "سعيدي", "تومي", "بلقاسم", "منصوري")
    mMFr = Array("Yacine", "Amine", "Mohamed", "Ahmed", "Khaled", "Riad", "Bilal", "Sofiane", "Islam", "Adel")
    mMAr = Array("ياسين", "أمين", "محمد", "أحمد", "خالد", "رياض", "بلال", "سفيان", "إسلام", "عادل")
    mFFr = Array("Nour", "Sara", "Imane", "Lina", "Feriel", "Amira", "Meriem", "Rania", "Asma", "Hadil")
    mFAr = Array("نور", "سارة", "إيمان", "لينا", "فريال", "أميرة", "مريم", "رانيا", "أسماء", "هديل")
    mPOB = Array("El Bayadh", "Alger", "Oran", "Blida", "Sétif", "Constantine", "Tlemcen", "Annaba")
End Sub

' ============================================================================
Public Sub SeedDemoData()
    Dim db As DAO.Database
    On Error GoTo EH
    Set db = CurrentDb
    InitPools
    Randomize 7   ' fixed seed => reproducible demo

    If MsgBox("This DELETES existing students, classes, grades and attendance, " & _
              "then loads demo data. Continue?", vbYesNo + vbExclamation, "Seed demo") = vbNo Then Exit Sub

    db.Execute "DELETE FROM tblAttendance", dbFailOnError
    db.Execute "DELETE FROM tblGrade", dbFailOnError
    db.Execute "DELETE FROM tblEnrollment", dbFailOnError
    db.Execute "DELETE FROM tblStudent", dbFailOnError
    db.Execute "DELETE FROM tblClass", dbFailOnError
    db.Execute "DELETE FROM tblTeacher", dbFailOnError

    Dim yID As Long, t1 As Long
    yID = EnsureYear(db, CUR_YEAR)
    t1 = EnsureTerm(db, "Trimestre 1", yID)

    ' --- teachers ---
    Dim tk As Long, ts As Long, tr As Long
    tk = AddTeacher(db, "Djelloul", "Karim", "0551 23 45 67")
    ts = AddTeacher(db, "Haddad", "Samia", "0661 78 90 12")
    tr = AddTeacher(db, "Brahimi", "Rachid", "0770 11 22 33")

    ' --- classes: 1 academic + 2 vocational (shows the dual track) ---
    Dim cA As Long, cIT As Long, cEL As Long
    cA = AddAcademicClass(db, yID, "1AS-A", EnsureLevel(db, "1AS", "1re année secondaire"), 35)
    cIT = AddVocClass(db, yID, "TS Informatique 1", EnsureSpec(db, "Informatique"), EnsureDiploma(db, "BTS"), 25)
    cEL = AddVocClass(db, yID, "CAP Électricité 1", EnsureSpec(db, "Électricité"), EnsureDiploma(db, "CAP"), 25)

    ' --- demo subjects/modules per class (create + return IDs & coefficients) ---
    Dim acadMods() As Long, acadCoef() As Double
    Dim itMods() As Long, itCoef() As Double
    Dim elMods() As Long, elCoef() As Double
    BuildModules db, "ACAD", acadMods, acadCoef
    BuildModules db, "IT", itMods, itCoef
    BuildModules db, "EL", elMods, elCoef

    ' --- students + enrollments + grades + attendance ---
    Dim seq As Long: seq = 0
    SeedClass db, yID, t1, cA, 12, acadMods, acadCoef, seq
    SeedClass db, yID, t1, cIT, 10, itMods, itCoef, seq
    SeedClass db, yID, t1, cEL, 8, elMods, elCoef, seq

    MsgBox "Demo loaded: 3 classes, " & seq & " students, Term-1 CC/Compo grades, 5 days of attendance.", vbInformation
    Exit Sub
EH:
    MsgBox "Seed error " & Err.Number & ": " & Err.Description & vbCrLf & _
           "(Likely a field-name mismatch — check the MAP block at the top.)", vbCritical
End Sub

' ============================================================================
'  Reference-row helpers (look up, or create a minimal row if missing)
' ============================================================================
Private Function EnsureYear(db As DAO.Database, sLabel As String) As Long
    Dim v: v = DLookup("YearID", "tblAcademicYear", "Label='" & sLabel & "'")
    If Not IsNull(v) Then EnsureYear = v: Exit Function
    Dim rs As DAO.Recordset: Set rs = db.OpenRecordset("tblAcademicYear", dbOpenDynaset)
    rs.AddNew: rs!Label = sLabel: rs!IsCurrent = True: rs.Update
    rs.Bookmark = rs.LastModified: EnsureYear = rs!YearID: rs.Close
End Function

Private Function EnsureTerm(db As DAO.Database, sName As String, yID As Long) As Long
    Dim v: v = DLookup("TermID", "tblTerm", "Name='" & sName & "' AND YearID=" & yID)
    If Not IsNull(v) Then EnsureTerm = v: Exit Function
    Dim rs As DAO.Recordset: Set rs = db.OpenRecordset("tblTerm", dbOpenDynaset)
    rs.AddNew: rs!Name = sName: rs!YearID = yID: rs.Update
    rs.Bookmark = rs.LastModified: EnsureTerm = rs!TermID: rs.Close
End Function

Private Function EnsureLevel(db As DAO.Database, sCode As String, sName As String) As Long
    Dim v: v = DLookup("LevelID", "tblLevel", "Name_fr='" & sCode & "' OR Name_fr='" & sName & "'")
    If Not IsNull(v) Then EnsureLevel = v: Exit Function
    Dim rs As DAO.Recordset: Set rs = db.OpenRecordset("tblLevel", dbOpenDynaset)
    rs.AddNew: rs!Name_fr = sCode: rs!Name_ar = sCode: rs.Update
    rs.Bookmark = rs.LastModified: EnsureLevel = rs!LevelID: rs.Close
End Function

Private Function EnsureSpec(db As DAO.Database, sName As String) As Long
    Dim v: v = DLookup("SpecializationID", "tblSpecialization", "Name_fr='" & sName & "'")
    If Not IsNull(v) Then EnsureSpec = v: Exit Function
    Dim rs As DAO.Recordset: Set rs = db.OpenRecordset("tblSpecialization", dbOpenDynaset)
    rs.AddNew: rs!Name_fr = sName: rs!Name_ar = sName: rs.Update
    rs.Bookmark = rs.LastModified: EnsureSpec = rs!SpecializationID: rs.Close
End Function

Private Function EnsureDiploma(db As DAO.Database, sCode As String) As Long
    Dim v: v = DLookup("DiplomaID", "tblDiploma", "Code='" & sCode & "' OR Name_fr='" & sCode & "'")
    If Not IsNull(v) Then EnsureDiploma = v: Exit Function
    Dim rs As DAO.Recordset: Set rs = db.OpenRecordset("tblDiploma", dbOpenDynaset)
    rs.AddNew: rs!Code = sCode: rs!Name_fr = sCode: rs.Update
    rs.Bookmark = rs.LastModified: EnsureDiploma = rs!DiplomaID: rs.Close
End Function

' ============================================================================
'  Insert helpers (return new AutoNumber IDs)
' ============================================================================
Private Function AddTeacher(db As DAO.Database, sLast As String, sFirst As String, sPhone As String) As Long
    Dim rs As DAO.Recordset: Set rs = db.OpenRecordset("tblTeacher", dbOpenDynaset)
    rs.AddNew: rs!LastName = sLast: rs!FirstName = sFirst: rs!Phone = sPhone: rs.Update
    rs.Bookmark = rs.LastModified: AddTeacher = rs!TeacherID: rs.Close
End Function

Private Function AddAcademicClass(db As DAO.Database, yID As Long, sName As String, lvl As Long, cap As Long) As Long
    Dim rs As DAO.Recordset: Set rs = db.OpenRecordset("tblClass", dbOpenDynaset)
    rs.AddNew
    rs!YearID = yID: rs!Name = sName: rs!Track = "Academic": rs!LevelID = lvl: rs!Capacity = cap
    rs.Update: rs.Bookmark = rs.LastModified: AddAcademicClass = rs!ClassID: rs.Close
End Function

Private Function AddVocClass(db As DAO.Database, yID As Long, sName As String, spec As Long, dip As Long, cap As Long) As Long
    Dim rs As DAO.Recordset: Set rs = db.OpenRecordset("tblClass", dbOpenDynaset)
    rs.AddNew
    rs!YearID = yID: rs!Name = sName: rs!Track = "Vocational"
    rs!SpecializationID = spec: rs!DiplomaID = dip: rs!Capacity = cap    ' remove DiplomaID if absent
    rs.Update: rs.Bookmark = rs.LastModified: AddVocClass = rs!ClassID: rs.Close
End Function

Private Function AddModule(db As DAO.Database, nameFr As String, nameAr As String, coef As Double) As Long
    Dim rs As DAO.Recordset: Set rs = db.OpenRecordset("tblModule", dbOpenDynaset)
    rs.AddNew: rs!Name_fr = nameFr: rs!Name_ar = nameAr: rs!Coefficient = coef: rs.Update
    rs.Bookmark = rs.LastModified: AddModule = rs!ModuleID: rs.Close
End Function

' Build a small subject/module set for a track; return parallel arrays of IDs + coefficients
Private Sub BuildModules(db As DAO.Database, track As String, ByRef ids() As Long, ByRef coefs() As Double)
    Dim fr As Variant, ar As Variant, co As Variant, i As Long
    Select Case track
      Case "ACAD"
        fr = Array("Mathématiques", "Sciences Physiques", "Sciences Naturelles", "Langue Arabe", _
                   "Langue Française", "Langue Anglaise", "Histoire-Géographie", "Éducation Physique")
        ar = Array("الرياضيات", "العلوم الفيزيائية", "علوم الطبيعة والحياة", "اللغة العربية", _
                   "اللغة الفرنسية", "اللغة الإنجليزية", "التاريخ والجغرافيا", "التربية البدنية")
        co = Array(5, 4, 4, 3, 3, 2, 2, 1)
      Case "IT"
        fr = Array("Programmation", "Bases de données", "Réseaux informatiques", "Bureautique", "Anglais technique", "Stage pratique")
        ar = Array("البرمجة", "قواعد البيانات", "الشبكات", "المكتبية", "الإنجليزية التقنية", "التربص التطبيقي")
        co = Array(5, 4, 4, 2, 2, 4)
      Case Else ' EL
        fr = Array("Électrotechnique", "Installations électriques", "Sécurité", "Maths appliquées", "Anglais technique", "Stage pratique")
        ar = Array("الكهرباء التقنية", "التركيبات الكهربائية", "الأمن والوقاية", "الرياضيات التطبيقية", "الإنجليزية التقنية", "التربص التطبيقي")
        co = Array(4, 4, 2, 2, 2, 4)
    End Select
    ReDim ids(LBound(fr) To UBound(fr))
    ReDim coefs(LBound(fr) To UBound(fr))
    For i = LBound(fr) To UBound(fr)
        ids(i) = AddModule(db, CStr(fr(i)), CStr(ar(i)), CDbl(co(i)))
        coefs(i) = CDbl(co(i))
    Next i
End Sub

' ============================================================================
'  Seed one class: students + enrollment + CC/Compo grades + attendance
' ============================================================================
Private Sub SeedClass(db As DAO.Database, yID As Long, termID As Long, classID As Long, _
                      nStud As Long, mods() As Long, coefs() As Double, ByRef seq As Long)
    Dim rsS As DAO.Recordset, rsE As DAO.Recordset, rsG As DAO.Recordset, rsA As DAO.Recordset
    Set rsS = db.OpenRecordset("tblStudent", dbOpenDynaset)
    Set rsE = db.OpenRecordset("tblEnrollment", dbOpenDynaset)
    Set rsG = db.OpenRecordset("tblGrade", dbOpenDynaset)
    Set rsA = db.OpenRecordset("tblAttendance", dbOpenDynaset)

    Dim i As Long, j As Long, d As Long, sid As Long
    For i = 1 To nStud
        seq = seq + 1
        Dim male As Boolean: male = (Rnd < 0.5)
        Dim ni As Long, li As Long
        ni = Int(Rnd * 10): li = Int(Rnd * 12)
        Dim fFr As String, fAr As String, lFr As String, lAr As String
        If male Then fFr = mMFr(ni): fAr = mMAr(ni) Else fFr = mFFr(ni): fAr = mFAr(ni)
        lFr = mLastFr(li): lAr = mLastAr(li)
        Dim ability As Double: ability = 8 + Rnd * 9   ' 8..17 latent ability

        rsS.AddNew
        rsS!Matricule = Format(Year(Date), "0000") & "-" & Format(seq, "0000")
        rsS!LastName_fr = lFr: rsS!FirstName_fr = fFr
        rsS!LastName_ar = lAr: rsS!FirstName_ar = fAr
        rsS!Gender = IIf(male, "M", "F")
        rsS!DOB = DateSerial(2009 - Int(Rnd * 4), 1 + Int(Rnd * 12), 1 + Int(Rnd * 27))
        rsS!PlaceOfBirth = mPOB(Int(Rnd * 8))
        rsS!GuardianName = mMFr(Int(Rnd * 10)) & " " & lFr
        rsS!GuardianPhone = "05" & Format(Int(Rnd * 100000000), "00000000")
        rsS.Fields(SF_STUDSTATUS) = "Active"
        rsS.Update: rsS.Bookmark = rsS.LastModified: sid = rsS!StudentID

        rsE.AddNew
        rsE!StudentID = sid: rsE!ClassID = classID: rsE!YearID = yID
        rsE!EnrollDate = DateSerial(2026, 9, 5): rsE!Status = "Active"
        rsE.Update

        ' grades per module (CC + Compo around ability, clamped 0..20)
        For j = LBound(mods) To UBound(mods)
            rsG.AddNew
            rsG!StudentID = sid: rsG!ModuleID = mods(j): rsG!TermID = termID
            rsG!CC = Clamp20(ability + Noise(2.5))
            rsG!Compo = Clamp20(ability + Noise(3#))
            rsG.Update
        Next j

        ' attendance: 5 school days (Sun 9 Nov -> Thu 13 Nov 2026), mostly Present
        For d = 0 To 4
            rsA.AddNew
            rsA!StudentID = sid
            rsA!ADate = DateSerial(2026, 11, 9) + d
            rsA!Session = "Jour"
            rsA!Status = AttStatus()
            rsA.Update
        Next d
    Next i

    rsS.Close: rsE.Close: rsG.Close: rsA.Close
End Sub

' ---- small numeric helpers ----
Private Function Noise(sd As Double) As Double
    Noise = (Rnd + Rnd + Rnd - 1.5) * sd   ' ~N(0, sd), quick approximation
End Function
Private Function Clamp20(v As Double) As Double
    If v < 0 Then v = 0
    If v > 20 Then v = 20
    Clamp20 = Int(v * 4 + 0.5) / 4          ' round to nearest 0.25
End Function
Private Function AttStatus() As String
    Dim r As Double: r = Rnd
    If r < 0.9 Then AttStatus = "Present" _
    Else If r < 0.95 Then AttStatus = "Absent" _
    Else If r < 0.98 Then AttStatus = "Late" _
    Else AttStatus = "Excused"
End Function
