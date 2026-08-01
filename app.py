#!/usr/bin/env python3
"""
SIS (Student Information System) — Streamlit Prototype
For Algerian public school teachers

Usage:
    cd C:/Users/Admin/My Drive/LifeWorkspace/10_Education_Project/SIS_Prototype
    streamlit run app.py
"""

import streamlit as st
import json
import os
import sys
import io
from datetime import datetime, date

# --- Page Config ---
st.set_page_config(
    page_title="SIS - Student Information System",
    page_icon="🏫",
    layout="wide",
)

# --- Data Storage ---
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

def load_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(filename, data):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# --- Initialize Data ---
for key, filename in [("students", "students.json"), ("classes", "classes.json"),
                       ("assessments", "assessments.json"), ("grades", "grades.json"),
                       ("users", "users.json")]:
    if key not in st.session_state:
        st.session_state[key] = load_data(filename)

# --- Auth System ---
def check_login(username, password):
    user = st.session_state.users.get(username)
    if user and user.get("password") == password:
        return user
    return None

def create_user(username, password, role, display_name):
    if username in st.session_state.users:
        return False
    st.session_state.users[username] = {
        "password": password,
        "role": role,
        "display_name": display_name,
        "created": str(date.today()),
    }
    save_data("users.json", st.session_state.users)
    return True

# --- Session State for Auth ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

# --- Login Page ---
if not st.session_state.logged_in:
    st.title("🏫 SIS - Student Information System")
    st.subheader("Login")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", type="primary")
            
            if submitted:
                user = check_login(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.current_user = {"username": username, **user}
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    
    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("Choose Username*")
            new_password = st.text_input("Choose Password*", type="password")
            display_name = st.text_input("Display Name*")
            role = st.selectbox("Role*", ["teacher", "admin"])
            
            submitted = st.form_submit_button("Register", type="primary")
            
            if submitted:
                if not all([new_username, new_password, display_name]):
                    st.error("All fields are required!")
                elif len(new_password) < 4:
                    st.error("Password must be at least 4 characters")
                else:
                    if create_user(new_username, new_password, role, display_name):
                        st.success("Account created! Please login.")
                    else:
                        st.error("Username already exists")
    
    st.stop()

# --- Logged In ---
user = st.session_state.current_user
role = user.get("role", "teacher")

# --- Sidebar ---
st.sidebar.title("🏫 SIS")
st.sidebar.write(f"Welcome, **{user.get('display_name', user.get('username'))}**")
st.sidebar.write(f"Role: **{role.title()}**")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.rerun()

st.sidebar.divider()

# Navigation based on role
if role == "admin":
    page = st.sidebar.radio(
        "Navigate to:",
        ["📊 Dashboard", "👨‍🎓 Students", "📚 Classes", "📝 Assessments",
         "📈 Grade Book", "📄 Reports", "👥 Users", "⚙️ Settings"]
    )
else:
    page = st.sidebar.radio(
        "Navigate to:",
        ["📊 Dashboard", "👨‍🎓 Students", "📚 Classes", "📝 Assessments",
         "📈 Grade Book", "📄 Reports"]
    )

# --- Constants ---
LEVELS = ["1AM", "2AM", "3AM", "4AM"]
GENDERS = ["M", "F"]

# --- Exercise Generator Integration ---
try:
    from exercise_generator import ExerciseGenerator, EXERCISE_TYPES
    from topics import get_topics_by_level, get_topic_by_id, LEVELS as GEN_LEVELS
    EX_GEN_AVAILABLE = True
except ImportError:
    EX_GEN_AVAILABLE = False
    EXERCISE_TYPES = ["fill_in_blank", "multiple_choice", "sentence_building",
                      "transformation", "error_correction", "matching"]
    GEN_LEVELS = ["A1", "A2", "B1", "B2"]

# --- PDF Export ---
def generate_student_report(student_id, student, grades):
    """Generate a simple text report for a student"""
    report = []
    report.append("=" * 50)
    report.append("STUDENT REPORT CARD")
    report.append("=" * 50)
    report.append(f"Name: {student.get('name', 'N/A')}")
    report.append(f"Name (Arabic): {student.get('name_arabic', 'N/A')}")
    report.append(f"Level: {student.get('level', 'N/A')}")
    report.append(f"Class: {student.get('class_id', 'N/A')}")
    report.append(f"Date: {date.today().strftime('%Y-%m-%d')}")
    report.append("")
    report.append("-" * 50)
    report.append("GRADES")
    report.append("-" * 50)
    
    student_grades = [g for g in grades.values() if g.get("student_id") == student_id]
    
    if not student_grades:
        report.append("No grades recorded yet.")
    else:
        total_score = 0
        total_possible = 0
        
        for grade in student_grades:
            score = grade.get("score", 0)
            total = grade.get("total", 0)
            pct = (score / total * 100) if total > 0 else 0
            total_score += score
            total_possible += total
            
            report.append(f"Date: {grade.get('date', 'N/A')}")
            report.append(f"Assessment: {grade.get('assessment_title', 'N/A')}")
            report.append(f"Score: {score}/{total} ({pct:.0f}%)")
            if grade.get("comments"):
                report.append(f"Comments: {grade['comments']}")
            report.append("")
        
        if total_possible > 0:
            overall_pct = (total_score / total_possible * 100)
            report.append("-" * 50)
            report.append(f"OVERALL: {total_score}/{total_possible} ({overall_pct:.0f}%)")
    
    report.append("=" * 50)
    return "\n".join(report)

def generate_class_report(class_id, class_info, students, grades):
    """Generate a report for a class"""
    report = []
    report.append("=" * 50)
    report.append("CLASS REPORT")
    report.append("=" * 50)
    report.append(f"Class: {class_info.get('name', 'N/A')}")
    report.append(f"Level: {class_info.get('level', 'N/A')}")
    report.append(f"Teacher: {class_info.get('teacher', 'N/A')}")
    report.append(f"Date: {date.today().strftime('%Y-%m-%d')}")
    report.append("")
    
    class_students = {k: v for k, v in students.items() if v.get("class_id") == class_id}
    report.append(f"Total Students: {len(class_students)}")
    report.append("")
    report.append("-" * 50)
    report.append("STUDENT GRADES")
    report.append("-" * 50)
    
    for student_id, student in class_students.items():
        student_grades = [g for g in grades.values() if g.get("student_id") == student_id]
        
        if student_grades:
            total_score = sum(g.get("score", 0) for g in student_grades)
            total_possible = sum(g.get("total", 0) for g in student_grades)
            pct = (total_score / total_possible * 100) if total_possible > 0 else 0
            report.append(f"{student.get('name', 'N/A')}: {total_score}/{total_possible} ({pct:.0f}%)")
        else:
            report.append(f"{student.get('name', 'N/A')}: No grades")
    
    report.append("=" * 50)
    return "\n".join(report)

# --- Dashboard ---
if page == "📊 Dashboard":
    st.title("📊 School Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Students", len(st.session_state.students))
    with col2:
        st.metric("Total Classes", len(st.session_state.classes))
    with col3:
        st.metric("Assessments", len(st.session_state.assessments))
    with col4:
        st.metric("Grade Entries", len(st.session_state.grades))
    
    st.divider()
    
    st.subheader("Recent Activity")
    if st.session_state.grades:
        recent = sorted(st.session_state.grades.values(),
                       key=lambda x: x.get("date", ""), reverse=True)[:5]
        for grade in recent:
            st.write(f"- {grade.get('student_name', 'Unknown')} scored "
                     f"{grade.get('score', 0)}/{grade.get('total', 0)} on "
                     f"{grade.get('assessment_title', 'Unknown')}")
    else:
        st.info("No grade entries yet.")
    
    st.subheader("Students by Level")
    level_counts = {}
    for student in st.session_state.students.values():
        level = student.get("level", "Unknown")
        level_counts[level] = level_counts.get(level, 0) + 1
    
    if level_counts:
        for level, count in sorted(level_counts.items()):
            st.write(f"**{level}**: {count} students")
    else:
        st.info("No students registered yet.")

# --- Students ---
elif page == "👨‍🎓 Students":
    st.title("👨‍🎓 Student Management")
    
    tab1, tab2 = st.tabs(["📋 List Students", "➕ Add Student"])
    
    with tab1:
        if st.session_state.students:
            level_filter = st.selectbox("Filter by Level", ["All"] + LEVELS)
            
            filtered = st.session_state.students
            if level_filter != "All":
                filtered = {k: v for k, v in filtered.items() if v.get("level") == level_filter}
            
            st.write(f"**{len(filtered)} students**")
            
            for student_id, student in filtered.items():
                with st.expander(f"{student.get('name', 'Unknown')} ({student.get('level', 'N/A')})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Name (AR):** {student.get('name_arabic', 'N/A')}")
                        st.write(f"**DOB:** {student.get('date_of_birth', 'N/A')}")
                        st.write(f"**Gender:** {student.get('gender', 'N/A')}")
                    with col2:
                        st.write(f"**Class:** {student.get('class_id', 'N/A')}")
                        st.write(f"**Parent Contact:** {student.get('parent_contact', 'N/A')}")
                        st.write(f"**Enrolled:** {student.get('enrollment_date', 'N/A')}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"📄 Report", key=f"rpt_{student_id}"):
                            report = generate_student_report(student_id, student, st.session_state.grades)
                            st.download_button(
                                f"Download Report for {student.get('name')}",
                                report,
                                file_name=f"report_{student_id}.txt",
                                mime="text/plain",
                                key=f"dl_{student_id}",
                            )
                    with col2:
                        if role == "admin" and st.button(f"🗑️ Delete", key=f"del_{student_id}"):
                            del st.session_state.students[student_id]
                            save_data("students.json", st.session_state.students)
                            st.rerun()
        else:
            st.info("No students registered yet.")
    
    with tab2:
        st.subheader("Add New Student")
        
        with st.form("add_student"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name (English)*")
                name_arabic = st.text_input("Full Name (Arabic)")
                dob = st.date_input("Date of Birth", value=date(2010, 1, 1))
                gender = st.selectbox("Gender*", GENDERS)
            
            with col2:
                level = st.selectbox("Level*", LEVELS)
                class_id = st.text_input("Class ID (e.g., 2AM-A)")
                parent_contact = st.text_input("Parent Phone")
                enrollment_date = st.date_input("Enrollment Date", value=date.today())
            
            medical_notes = st.text_area("Medical Notes (optional)")
            
            submitted = st.form_submit_button("Add Student", type="primary")
            
            if submitted:
                if not name:
                    st.error("Name is required!")
                else:
                    student_id = f"STU-{len(st.session_state.students) + 1:04d}"
                    st.session_state.students[student_id] = {
                        "name": name,
                        "name_arabic": name_arabic,
                        "date_of_birth": str(dob),
                        "gender": gender,
                        "level": level,
                        "class_id": class_id,
                        "parent_contact": parent_contact,
                        "enrollment_date": str(enrollment_date),
                        "medical_notes": medical_notes,
                    }
                    save_data("students.json", st.session_state.students)
                    st.success(f"Student {name} added!")
                    st.rerun()

# --- Classes ---
elif page == "📚 Classes":
    st.title("📚 Class Management")
    
    tab1, tab2 = st.tabs(["📋 List Classes", "➕ Add Class"])
    
    with tab1:
        if st.session_state.classes:
            for class_id, cls in st.session_state.classes.items():
                with st.expander(f"{cls.get('name', 'Unknown')} - {cls.get('level', 'N/A')}"):
                    st.write(f"**Teacher:** {cls.get('teacher', 'N/A')}")
                    st.write(f"**Schedule:** {cls.get('schedule', 'N/A')}")
                    st.write(f"**Room:** {cls.get('room', 'N/A')}")
                    
                    students_in_class = [s for s in st.session_state.students.values()
                                        if s.get("class_id") == class_id]
                    st.write(f"**Students:** {len(students_in_class)}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"📄 Class Report", key=f"rpt_class_{class_id}"):
                            report = generate_class_report(class_id, cls,
                                                          st.session_state.students,
                                                          st.session_state.grades)
                            st.download_button(
                                f"Download Report for {cls.get('name')}",
                                report,
                                file_name=f"class_report_{class_id}.txt",
                                mime="text/plain",
                                key=f"dl_class_{class_id}",
                            )
                    with col2:
                        if role == "admin" and st.button(f"🗑️ Delete", key=f"del_class_{class_id}"):
                            del st.session_state.classes[class_id]
                            save_data("classes.json", st.session_state.classes)
                            st.rerun()
        else:
            st.info("No classes created yet.")
    
    with tab2:
        st.subheader("Add New Class")
        
        with st.form("add_class"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Class Name (e.g., 2AM-A)*")
                level = st.selectbox("Level*", LEVELS)
            
            with col2:
                teacher = st.text_input("Teacher Name")
                schedule = st.text_input("Schedule (e.g., Mon/Wed 8-10)")
                room = st.text_input("Room")
            
            submitted = st.form_submit_button("Add Class", type="primary")
            
            if submitted:
                if not name:
                    st.error("Class name is required!")
                else:
                    class_id = name.upper().replace(" ", "-")
                    st.session_state.classes[class_id] = {
                        "name": name,
                        "level": level,
                        "teacher": teacher,
                        "schedule": schedule,
                        "room": room,
                    }
                    save_data("classes.json", st.session_state.classes)
                    st.success(f"Class {name} created!")
                    st.rerun()

# --- Assessments ---
elif page == "📝 Assessments":
    st.title("📝 Assessment Engine")
    
    tab1, tab2, tab3 = st.tabs(["📋 List Assessments", "➕ Create Assessment", "🔗 Exercise Generator"])
    
    with tab1:
        if st.session_state.assessments:
            for assess_id, assess in st.session_state.assessments.items():
                with st.expander(f"{assess.get('title', 'Unknown')} ({assess.get('type', 'N/A')})"):
                    st.write(f"**Level:** {assess.get('level', 'N/A')}")
                    st.write(f"**Items:** {len(assess.get('items', []))}")
                    st.write(f"**Total Points:** {assess.get('total_points', 0)}")
                    st.write(f"**Time Limit:** {assess.get('time_limit_minutes', 0)} min")
                    
                    if assess.get("items"):
                        st.write("**Items Preview:**")
                        for i, item in enumerate(assess["items"][:3], 1):
                            st.write(f"  {i}. {item.get('question', item.get('sentence', 'N/A'))}")
                    
                    if role == "admin" and st.button(f"🗑️ Delete", key=f"del_assess_{assess_id}"):
                        del st.session_state.assessments[assess_id]
                        save_data("assessments.json", st.session_state.assessments)
                        st.rerun()
        else:
            st.info("No assessments created yet.")
    
    with tab2:
        st.subheader("Create New Assessment")
        
        with st.form("add_assessment"):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("Assessment Title*")
                assess_type = st.selectbox("Type*", ["grammar", "vocabulary", "mixed"])
                level = st.selectbox("Level*", LEVELS)
            
            with col2:
                time_limit = st.number_input("Time Limit (minutes)", value=60, min_value=10, max_value=180)
                total_points = st.number_input("Total Points", value=20, min_value=1, max_value=100)
            
            submitted = st.form_submit_button("Create Assessment", type="primary")
            
            if submitted:
                if not title:
                    st.error("Title is required!")
                else:
                    assess_id = f"ASS-{len(st.session_state.assessments) + 1:04d}"
                    st.session_state.assessments[assess_id] = {
                        "title": title,
                        "type": assess_type,
                        "level": level,
                        "items": [],
                        "total_points": total_points,
                        "time_limit_minutes": time_limit,
                        "created_date": str(date.today()),
                    }
                    save_data("assessments.json", st.session_state.assessments)
                    st.success(f"Assessment '{title}' created!")
                    st.rerun()
    
    with tab3:
        st.subheader("🔗 Exercise Generator Integration")
        
        if not EX_GEN_AVAILABLE:
            st.warning("Exercise Generator not found. Make sure it's in the Education_Project folder.")
            st.code("Expected path: ../Exercise_Generator/", language="text")
        else:
            st.success("Exercise Generator connected!")
            
            # Select assessment to populate
            if st.session_state.assessments:
                assess_select = st.selectbox(
                    "Select Assessment to Populate",
                    list(st.session_state.assessments.keys()),
                    format_func=lambda x: st.session_state.assessments[x].get("title", x),
                )
            else:
                st.info("Create an assessment first, then populate it with exercises.")
                assess_select = None
            
            col1, col2 = st.columns(2)
            
            with col1:
                gen_level = st.selectbox("CEFR Level", GEN_LEVELS)
                gen_type = st.selectbox("Exercise Type", EXERCISE_TYPES)
            
            with col2:
                gen_count = st.number_input("Exercises per Topic", value=5, min_value=1, max_value=20)
                # Load topics for selected level
                try:
                    available_topics = [t["name"] for t in get_topics_by_level(gen_level)]
                except:
                    available_topics = []
                gen_topics = st.multiselect(
                    "Select Topics (leave empty for all)",
                    available_topics,
                )
            
            if st.button("🔗 Generate & Import", type="primary"):
                with st.spinner("Generating exercises..."):
                    gen = ExerciseGenerator()
                    result = gen.generate_for_level(gen_level, gen_type, gen_count)
                    
                    # Filter by selected topics if any
                    if gen_topics:
                        result = [r for r in result if r.get("topic") in gen_topics]
                    
                    if result:
                        all_items = []
                        for r in result:
                            if "error" not in r:
                                for ex in r.get("exercises", []):
                                    item = {
                                        "question": ex.get("question", ex.get("sentence", "")),
                                        "answer": ex.get("answer", ""),
                                        "options": ex.get("options", []),
                                        "type": ex.get("type", gen_type),
                                        "topic": r.get("topic", ""),
                                        "points": 1,
                                    }
                                    all_items.append(item)
                        
                        if all_items and assess_select:
                            assessment = st.session_state.assessments[assess_select]
                            assessment["items"].extend(all_items)
                            save_data("assessments.json", st.session_state.assessments)
                            st.success(f"Imported {len(all_items)} exercises into '{assessment.get('title')}'!")
                        elif all_items:
                            st.info(f"Generated {len(all_items)} exercises. Create an assessment first to import.")
                        else:
                            st.warning("No exercises generated.")
                    else:
                        st.error("Failed to generate exercises.")

# --- Grade Book ---
elif page == "📈 Grade Book":
    st.title("📈 Grade Book")
    
    tab1, tab2 = st.tabs(["📋 View Grades", "➕ Enter Grades"])
    
    with tab1:
        if st.session_state.grades:
            student_names = {k: v.get("name", k) for k, v in st.session_state.students.items()}
            
            if student_names:
                selected_student = st.selectbox("Select Student",
                    ["All"] + list(student_names.values()))
                
                filtered = st.session_state.grades
                if selected_student != "All":
                    student_id = [k for k, v in student_names.items() if v == selected_student][0]
                    filtered = {k: v for k, v in filtered.items() if v.get("student_id") == student_id}
                
                st.write(f"**{len(filtered)} grade entries**")
                
                for grade_id, grade in filtered.items():
                    score = grade.get("score", 0)
                    total = grade.get("total", 0)
                    pct = (score / total * 100) if total > 0 else 0
                    
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    with col1:
                        st.write(f"**{grade.get('student_name', 'Unknown')}** - "
                                f"{grade.get('assessment_title', 'Unknown')}")
                    with col2:
                        st.write(f"{score}/{total}")
                    with col3:
                        st.write(f"{pct:.0f}%")
                    with col4:
                        st.write(grade.get("date", "N/A"))
            else:
                st.info("No students registered yet.")
        else:
            st.info("No grades entered yet.")
    
    with tab2:
        st.subheader("Enter New Grade")
        
        if st.session_state.students and st.session_state.assessments:
            with st.form("add_grade"):
                col1, col2 = st.columns(2)
                
                with col1:
                    student_id = st.selectbox("Student*",
                        list(st.session_state.students.keys()),
                        format_func=lambda x: st.session_state.students[x].get("name", x))
                    
                    assessment_id = st.selectbox("Assessment*",
                        list(st.session_state.assessments.keys()),
                        format_func=lambda x: st.session_state.assessments[x].get("title", x))
                
                with col2:
                    score = st.number_input("Score*", value=0, min_value=0, max_value=100)
                    total = st.number_input("Total Points", value=20, min_value=1, max_value=100)
                    grade_date = st.date_input("Date", value=date.today())
                
                comments = st.text_area("Comments (optional)")
                
                submitted = st.form_submit_button("Add Grade", type="primary")
                
                if submitted:
                    student_name = st.session_state.students[student_id].get("name", student_id)
                    assessment_title = st.session_state.assessments[assessment_id].get("title", assessment_id)
                    
                    grade_id = f"GRD-{len(st.session_state.grades) + 1:04d}"
                    st.session_state.grades[grade_id] = {
                        "student_id": student_id,
                        "student_name": student_name,
                        "assessment_id": assessment_id,
                        "assessment_title": assessment_title,
                        "score": score,
                        "total": total,
                        "date": str(grade_date),
                        "comments": comments,
                    }
                    save_data("grades.json", st.session_state.grades)
                    st.success(f"Grade added for {student_name}!")
                    st.rerun()
        else:
            st.warning("Please add students and assessments first.")

# --- Reports ---
elif page == "📄 Reports":
    st.title("📄 Reports & Export")
    
    tab1, tab2 = st.tabs(["👨‍🎓 Student Reports", "📚 Class Reports"])
    
    with tab1:
        if st.session_state.students:
            student_id = st.selectbox(
                "Select Student",
                list(st.session_state.students.keys()),
                format_func=lambda x: st.session_state.students[x].get("name", x),
                key="rpt_student",
            )
            
            student = st.session_state.students[student_id]
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Name:** {student.get('name', 'N/A')}")
                st.write(f"**Level:** {student.get('level', 'N/A')}")
                st.write(f"**Class:** {student.get('class_id', 'N/A')}")
            with col2:
                student_grades = [g for g in st.session_state.grades.values()
                                if g.get("student_id") == student_id]
                st.write(f"**Total Assessments:** {len(student_grades)}")
                if student_grades:
                    total_score = sum(g.get("score", 0) for g in student_grades)
                    total_possible = sum(g.get("total", 0) for g in student_grades)
                    pct = (total_score / total_possible * 100) if total_possible > 0 else 0
                    st.write(f"**Overall:** {total_score}/{total_possible} ({pct:.0f}%)")
            
            report = generate_student_report(student_id, student, st.session_state.grades)
            
            st.download_button(
                "📥 Download Report (TXT)",
                report,
                file_name=f"report_{student.get('name', student_id).replace(' ', '_')}.txt",
                mime="text/plain",
            )
        else:
            st.info("No students registered yet.")
    
    with tab2:
        if st.session_state.classes:
            class_id = st.selectbox(
                "Select Class",
                list(st.session_state.classes.keys()),
                format_func=lambda x: st.session_state.classes[x].get("name", x),
                key="rpt_class",
            )
            
            class_info = st.session_state.classes[class_id]
            
            st.write(f"**Class:** {class_info.get('name', 'N/A')}")
            st.write(f"**Level:** {class_info.get('level', 'N/A')}")
            st.write(f"**Teacher:** {class_info.get('teacher', 'N/A')}")
            
            report = generate_class_report(class_id, class_info,
                                          st.session_state.students,
                                          st.session_state.grades)
            
            st.download_button(
                "📥 Download Class Report (TXT)",
                report,
                file_name=f"class_report_{class_id}.txt",
                mime="text/plain",
            )
        else:
            st.info("No classes created yet.")

# --- Users (Admin only) ---
elif page == "👥 Users" and role == "admin":
    st.title("👥 User Management")
    
    if st.session_state.users:
        for username, user_data in st.session_state.users.items():
            with st.expander(f"{username} ({user_data.get('role', 'N/A')})"):
                st.write(f"**Display Name:** {user_data.get('display_name', 'N/A')}")
                st.write(f"**Role:** {user_data.get('role', 'N/A')}")
                st.write(f"**Created:** {user_data.get('created', 'N/A')}")
                
                if username != user.get("username"):
                    new_role = st.selectbox("Change Role", ["teacher", "admin"],
                                          index=0 if user_data.get("role") == "teacher" else 1,
                                          key=f"role_{username}")
                    if st.button(f"Update Role", key=f"update_{username}"):
                        st.session_state.users[username]["role"] = new_role
                        save_data("users.json", st.session_state.users)
                        st.success(f"Updated {username} to {new_role}")
                        st.rerun()
    else:
        st.info("No users registered yet.")

# --- Settings ---
elif page == "⚙️ Settings":
    st.title("⚙️ Settings")
    
    st.subheader("Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export All Data"):
            export_data = {
                "students": st.session_state.students,
                "classes": st.session_state.classes,
                "assessments": st.session_state.assessments,
                "grades": st.session_state.grades,
                "export_date": str(datetime.now()),
            }
            st.json(export_data)
            
            st.download_button(
                "📥 Download JSON",
                json.dumps(export_data, indent=2, ensure_ascii=False),
                file_name=f"sis_export_{date.today()}.json",
                mime="application/json",
            )
    
    with col2:
        if role == "admin" and st.button("🗑️ Clear All Data", type="secondary"):
            st.session_state.students = {}
            st.session_state.classes = {}
            st.session_state.assessments = {}
            st.session_state.grades = {}
            save_data("students.json", {})
            save_data("classes.json", {})
            save_data("assessments.json", {})
            save_data("grades.json", {})
            st.success("All data cleared!")
            st.rerun()
    
    st.divider()
    
    st.subheader("About")
    st.write("**SIS Prototype v2.0**")
    st.write("Student Information System for Algerian public schools")
    st.write("Built with Streamlit")
    st.write("Part of the Ta'allim Education Project")
    st.write("")
    st.write("**Features:**")
    st.write("- Student management with Arabic names")
    st.write("- Class organization by level (1AM-4AM)")
    st.write("- Assessment engine with Exercise Generator integration")
    st.write("- Grade book with percentage calculation")
    st.write("- Student and class report export")
    st.write("- Multi-user support (teacher/admin roles)")

# --- Footer ---
st.sidebar.divider()
st.sidebar.caption("SIS Prototype v2.0")
st.sidebar.caption("Part of Ta'allim Education Project")
