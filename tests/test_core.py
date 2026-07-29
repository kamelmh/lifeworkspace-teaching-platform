"""Tests for Ta'allim core components."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def test_topics_load():
    from taallim.topics import get_topics_by_level, LEVELS
    for level in LEVELS:
        topics = get_topics_by_level(level)
        assert len(topics) > 0, f"No topics for {level}"
        for t in topics:
            assert "id" in t
            assert "name" in t
            assert "exercise_types" in t


def test_exercise_generator_offline():
    from taallim.exercise_generator import ExerciseGenerator
    gen = ExerciseGenerator(api_key=None)
    result = gen.generate("present_simple", "fill_in_blank", 5)
    assert "error" not in result
    assert result["count"] == 5
    assert result["source"] == "offline"
    assert len(result["exercises"]) == 5


def test_exercise_generator_mcq():
    from taallim.exercise_generator import ExerciseGenerator
    gen = ExerciseGenerator(api_key=None)
    result = gen.generate("present_simple", "multiple_choice", 5)
    assert "error" not in result
    assert result["count"] == 5
    for ex in result["exercises"]:
        assert "options" in ex
        assert len(ex["options"]) == 4


def test_offline_generator_types():
    from taallim.offline_generator import OfflineGenerator
    gen = OfflineGenerator()
    types = ["fill_in_blank", "multiple_choice", "sentence_building", "error_correction", "matching", "translation"]
    for t in types:
        result = gen.generate(t, "present_simple", 3)
        assert len(result) == 3


def test_mcq_generator():
    from taallim.mcq_generator import MCQGenerator
    gen = MCQGenerator()
    questions = gen.generate("past_simple", count=5)
    assert len(questions) == 5
    for q in questions:
        assert "question" in q
        assert "options" in q
        assert "correct" in q
        assert "explanation" in q


def test_mindmap_generator():
    from taallim.mindmap_generator import MindMapGenerator
    gen = MindMapGenerator()
    mindmap = gen.generate("past_simple")
    assert "root_label" in mindmap
    assert "nodes" in mindmap
    assert mindmap["node_count"] > 0


def test_flashcard_system():
    from taallim.flashcard_system import FlashcardDeck, SpacedRepetition, Quality
    deck = FlashcardDeck("test", "past_simple")
    deck.add_card("I ___ (go) yesterday", "went")
    deck.add_card("She ___ (eat) an apple", "ate")
    assert len(deck.cards) == 2
    sr = SpacedRepetition()
    session = sr.get_review_session(deck, max_cards=2)
    assert len(session) > 0
    sr.review(session[0], Quality.EASY)
