"""Ta'allim — AI-powered English teaching platform for Algerian schools."""

__version__ = "1.0.0"

from taallim.exercise_generator import ExerciseGenerator, EXERCISE_TYPES
from taallim.topics import get_topics_by_level, get_topic_by_id, LEVELS
from taallim.flashcard_system import FlashcardDeck, SpacedRepetition, Quality
from taallim.mcq_generator import MCQGenerator
from taallim.mindmap_generator import MindMapGenerator
