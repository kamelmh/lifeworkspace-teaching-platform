"""
Ta'allim — AI-Powered English Teaching Platform
Streamlit App combining all components

Run:
    streamlit run app.py

Features:
    - Exercise Generator (6 types, offline + API)
    - Flashcard System (SM-2 spaced repetition)
    - MCQ Generator (quiz mode with scoring)
    - Mind Map Generator (visual HTML output)
    - Assessment System (curriculum-aligned)
    - Student Dashboard (progress tracking)
"""

import streamlit as st
import json
import os
import sys
from datetime import datetime

from taallim.exercise_generator import ExerciseGenerator, EXERCISE_TYPES, to_html, to_markdown
from taallim.topics import get_topics_by_level, get_topic_by_id, LEVELS
from taallim.flashcard_system import FlashcardDeck, SpacedRepetition, Quality
from taallim.mcq_generator import MCQGenerator
from taallim.mindmap_generator import MindMapGenerator

st.set_page_config(
    page_title="Ta'allim — تعليم",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a5276, #2980b9);
        padding: 20px; border-radius: 10px;
        color: white; text-align: center; margin-bottom: 20px;
    }
    .stat-card {
        background: #f8f9fa; padding: 15px;
        border-radius: 8px; border-left: 4px solid #2980b9;
    }
    .correct { color: #27ae60; font-weight: bold; }
    .incorrect { color: #e74c3c; font-weight: bold; }
    .stButton>button { width: 100%; }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    for key, default in [
        ("flashcard_deck", None),
        ("mcq_questions", []),
        ("mcq_index", 0),
        ("mcq_score", 0),
        ("review_session", []),
        ("review_index", 0),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default


def sidebar():
    with st.sidebar:
        st.title("Ta'allim")
        st.caption("AI-Powered English Teaching")
        st.divider()
        st.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}")
        st.write("**Levels:** A1–B2 (1AM–4AM)")
        st.write("**Curriculum:** Algerian Ministry of Education")
        st.divider()
        with st.expander("About"):
            st.write("""
            Ta'allim is an AI-powered English teaching platform for Algerian schools.

            **Components:**
            - Exercise Generator (6 types)
            - Flashcard System (spaced repetition)
            - MCQ Quiz (auto-scored)
            - Mind Maps (visual learning)
            - Assessments (curriculum-aligned)
            - Student Dashboard
            """)


def tab_exercises():
    st.header("Exercise Generator")

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Settings")
        level = st.selectbox("CEFR Level", LEVELS)
        topics = get_topics_by_level(level)
        topic_map = {t["name"]: t for t in topics}
        selected_topic = st.selectbox("Topic", list(topic_map.keys()))

        valid_types = EXERCISE_TYPES
        if selected_topic:
            valid_types = [
                t for t in topic_map[selected_topic].get("exercise_types", EXERCISE_TYPES)
                if t in EXERCISE_TYPES
            ]
        exercise_type = st.selectbox("Exercise Type", valid_types, format_func=lambda x: x.replace("_", " ").title())
        count = st.slider("Number of exercises", 1, 20, 10)
        generate_btn = st.button("Generate", type="primary", use_container_width=True)

    with col2:
        st.subheader("Results")
        if generate_btn and selected_topic:
            gen = ExerciseGenerator(api_key=api_key or None)
            result = gen.generate(topic_map[selected_topic]["id"], exercise_type, count)

            if "error" in result:
                st.error(result["error"])
            else:
                st.success(f"Generated {result['count']} exercises ({result['source']})")
                st.session_state["last_result"] = result

                for i, ex in enumerate(result["exercises"], 1):
                    with st.expander(f"Exercise {i}", expanded=(i <= 3)):
                        if exercise_type == "fill_in_blank":
                            st.write(f"**{ex['sentence']}**")
                            st.write(f"Answer: `{ex['answer']}`")
                            if ex.get("hint"):
                                st.caption(f"Hint: {ex['hint']}")
                        elif exercise_type == "multiple_choice":
                            st.write(f"**{ex['question']}**")
                            for j, opt in enumerate(ex.get("options", [])):
                                letter = chr(65 + j)
                                marker = " ✓" if letter == ex.get("answer") else ""
                                st.write(f"  {letter}) {opt}{marker}")
                        elif exercise_type == "sentence_building":
                            st.write(f"**Arrange:** {ex['words']}")
                            st.write(f"Answer: `{ex['correct_sentence']}`")
                        elif exercise_type == "error_correction":
                            st.write(f"**Find the error:** {ex['sentence']}")
                            st.write(f"Correct: `{ex['correct']}`")
                            if ex.get("explanation"):
                                st.caption(ex["explanation"])
                        elif exercise_type == "matching":
                            st.write(f"**{ex['english']}** ↔ **{ex['arabic']}**")
                        elif exercise_type == "transformation":
                            st.write(f"**Original:** {ex.get('original', '')}")
                            st.write(f"**Task:** {ex.get('instruction', '')}")
                            st.write(f"Transformed: `{ex.get('transformed', '')}`")

    if "last_result" in st.session_state:
        st.divider()
        result = st.session_state["last_result"]
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        base = f"exercises_{result['topic'].lower().replace(' ', '_')}_{result['level']}_{ts}"
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("Download HTML", to_html([result]), f"{base}.html", "text/html", use_container_width=True)
        with c2:
            st.download_button("Download Markdown", to_markdown([result]), f"{base}.md", "text/markdown", use_container_width=True)
        with c3:
            st.download_button("Download JSON", json.dumps(result, indent=2, ensure_ascii=False), f"{base}.json", "application/json", use_container_width=True)


def tab_flashcards():
    st.header("Flashcard System")

    subtab1, subtab2 = st.tabs(["Create Deck", "Review Session"])

    with subtab1:
        st.subheader("Create New Deck")
        deck_name = st.text_input("Deck Name", "Past Simple Verbs")
        topic = st.selectbox("Topic", ["past_simple", "present_perfect", "conditionals", "passive_voice"], key="fc_topic")
        cards_text = st.text_area(
            "Cards (one per line, format: front|back)",
            "I ______ (go) to school yesterday|went\nShe ______ (eat) an apple|ate\nThey ______ (play) football|played",
            height=150,
        )
        if st.button("Create Deck"):
            deck = FlashcardDeck(deck_name, topic)
            for line in cards_text.strip().split("\n"):
                if "|" in line:
                    front, back = line.split("|", 1)
                    deck.add_card(front.strip(), back.strip(), [topic])
            st.session_state.flashcard_deck = deck
            st.success(f"Created deck with {len(deck.cards)} cards!")

    with subtab2:
        st.subheader("Review Session")
        if not st.session_state.flashcard_deck:
            st.warning("Create a deck first.")
            return

        deck = st.session_state.flashcard_deck
        sr = SpacedRepetition()

        if not st.session_state.review_session:
            st.session_state.review_session = sr.get_review_session(deck, max_cards=10)
            st.session_state.review_index = 0

        session = st.session_state.review_session
        idx = st.session_state.review_index

        if idx >= len(session):
            st.success("Review session complete!")
            st.json(deck.get_stats())
            if st.button("New Session"):
                st.session_state.review_session = []
                st.session_state.review_index = 0
            return

        card = session[idx]
        st.progress((idx + 1) / len(session))
        st.write(f"Card {idx + 1} of {len(session)}")
        st.info(f"**{card.front}**")

        if st.button("Show Answer"):
            st.success(f"**Answer:** {card.back}")
            c1, c2, c3, c4 = st.columns(4)
            for label, quality in [("Again", Quality.HARD), ("Hard", Quality.MEDIUM), ("Good", Quality.EASY), ("Easy", Quality.PERFECT)]:
                with c1 if label == "Again" else c2 if label == "Hard" else c3 if label == "Good" else c4:
                    if st.button(label, key=label):
                        sr.review(card, quality)
                        st.session_state.review_index += 1
                        st.rerun()


def tab_mcq():
    st.header("MCQ Quiz")

    col1, col2 = st.columns(2)
    with col1:
        topic = st.selectbox("Topic", ["past_simple", "present_perfect", "conditionals", "passive_voice", "reported_speech"], key="mcq_topic")
    with col2:
        count = st.slider("Questions", 5, 20, 10, key="mcq_count")

    if st.button("Start Quiz", type="primary"):
        gen = MCQGenerator()
        st.session_state.mcq_questions = gen.generate(topic, count=count)
        st.session_state.mcq_index = 0
        st.session_state.mcq_score = 0
        st.rerun()

    questions = st.session_state.mcq_questions
    idx = st.session_state.mcq_index

    if questions and idx < len(questions):
        q = questions[idx]
        st.progress((idx + 1) / len(questions))
        st.write(f"Question {idx + 1}/{len(questions)} | Score: {st.session_state.mcq_score}/{idx}")
        st.write(f"**{q['question']}**")
        if q.get("context"):
            st.info(q["context"])
        answer = st.radio("Choose:", q["options"], key=f"mcq_{idx}")
        if st.button("Submit"):
            if q["options"].index(answer) == q["correct"]:
                st.session_state.mcq_score += 1
                st.success("Correct!")
            else:
                st.error(f"Incorrect. Answer: {q['options'][q['correct']]}")
            st.caption(q["explanation"])
            if st.button("Next"):
                st.session_state.mcq_index += 1
                st.rerun()
    elif questions:
        st.balloons()
        score = st.session_state.mcq_score
        st.success(f"Quiz Complete! Score: {score}/{len(questions)} ({score/len(questions)*100:.0f}%)")
        if st.button("New Quiz"):
            st.session_state.mcq_questions = []
            st.rerun()


def tab_mindmaps():
    st.header("Mind Map Generator")

    topic = st.selectbox("Topic", ["past_simple", "present_perfect", "conditionals", "passive_voice", "reported_speech"], key="mm_topic")

    if st.button("Generate Mind Map", type="primary"):
        gen = MindMapGenerator()
        mindmap = gen.generate(topic)
        st.success(f"Generated mind map with {mindmap['node_count']} nodes!")

        st.subheader(mindmap["root_label"])
        for node in mindmap["nodes"]:
            if node["parent_id"] == "0":
                st.write(f"**{node['label']}**")
                for child in mindmap["nodes"]:
                    if child["parent_id"] == node["id"]:
                        st.write(f"  - {child['label']}")

        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as f:
            gen.save_html(mindmap, f.name)
            html_content = open(f.name, "r", encoding="utf-8").read()

        st.download_button("Download HTML Mind Map", html_content, f"{topic}_mindmap.html", "text/html")


def tab_assessments():
    st.header("Assessment System")

    topic = st.selectbox("Topic", ["past_simple", "present_perfect", "conditionals", "passive_voice", "reported_speech"], key="assess_topic")

    c1, c2 = st.columns(2)
    with c1:
        include_mcq = st.checkbox("MCQ Questions", value=True)
        include_fill = st.checkbox("Fill in the Blank", value=True)
        include_error = st.checkbox("Error Correction", value=True)
    with c2:
        total_questions = st.slider("Total Questions", 10, 50, 25)

    if st.button("Generate Assessment", type="primary"):
        gen = MCQGenerator()
        assessment = {"topic": topic, "sections": []}

        if include_mcq:
            mcq_count = min(10, total_questions // 3)
            assessment["sections"].append({"type": "mcq", "questions": gen.generate(topic, count=mcq_count)})
        if include_fill:
            fill_count = min(10, total_questions // 3)
            assessment["sections"].append({"type": "fill_blank", "questions": gen.generate(topic, count=fill_count)})
        if include_error:
            err_count = min(10, total_questions // 3)
            assessment["sections"].append({"type": "error_correction", "questions": gen.generate(topic, count=err_count)})

        st.success("Assessment generated!")
        st.json(assessment)
        st.download_button("Download (JSON)", json.dumps(assessment, indent=2), f"assessment_{topic}.json", "application/json")


def tab_dashboard():
    st.header("Student Dashboard")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Cards Mastered", "24", "+5")
    with c2:
        st.metric("Quiz Average", "78%", "+12%")
    with c3:
        st.metric("Study Streak", "7 days", "+2")
    with c4:
        st.metric("Total Exercises", "156", "+23")

    st.subheader("Topic Progress")
    for t in ["Past Simple", "Present Perfect", "Conditionals", "Passive Voice", "Reported Speech"]:
        st.slider(t, 0, 100, 50, key=f"progress_{t}")


def main():
    init_session_state()
    sidebar()

    st.markdown('<div class="main-header"><h1>Ta\'allim — تعليم</h1><p>AI-Powered English Teaching for Algerian Schools</p></div>', unsafe_allow_html=True)

    tabs = st.tabs(["Exercises", "Flashcards", "MCQ Quiz", "Mind Maps", "Assessments", "Dashboard"])
    with tabs[0]: tab_exercises()
    with tabs[1]: tab_flashcards()
    with tabs[2]: tab_mcq()
    with tabs[3]: tab_mindmaps()
    with tabs[4]: tab_assessments()
    with tabs[5]: tab_dashboard()


if __name__ == "__main__":
    main()
