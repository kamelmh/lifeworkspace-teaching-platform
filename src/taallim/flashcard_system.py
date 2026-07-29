"""
Ta'allim Flashcard System
Spaced repetition learning for vocabulary and grammar
Based on SM-2 algorithm (Anki-style)

Usage:
    from flashcard_system import FlashcardDeck, SpacedRepetition

    deck = FlashcardDeck("past_simple")
    deck.add_card("I ______ (go) to school yesterday", "went")

    sr = SpacedRepetition()
    card = sr.get_next_card(deck)
    sr.review(card, quality=5)
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, field, asdict
from enum import IntEnum


class Quality(IntEnum):
    BLACKOUT = 0
    INCORRECT = 1
    HARD = 2
    MEDIUM = 3
    EASY = 4
    PERFECT = 5


@dataclass
class Flashcard:
    front: str
    back: str
    card_id: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    ease_factor: float = 2.5
    interval_days: int = 0
    repetitions: int = 0
    next_review: str = field(default_factory=lambda: datetime.now().isoformat())
    last_review: str = ""
    total_reviews: int = 0
    correct_count: int = 0

    def __post_init__(self):
        if not self.card_id:
            self.card_id = f"card_{hash(self.front + self.back) % 100000:05d}"


class FlashcardDeck:
    def __init__(self, name: str, topic: str = "", level: str = ""):
        self.name = name
        self.topic = topic
        self.level = level
        self.cards: List[Flashcard] = []
        self.created_at = datetime.now().isoformat()
        self.description = ""

    def add_card(self, front: str, back: str, tags: List[str] = None) -> Flashcard:
        card = Flashcard(front=front, back=back, tags=tags or [])
        self.cards.append(card)
        return card

    def add_cards_from_list(self, items: List[Dict[str, str]]) -> int:
        count = 0
        for item in items:
            if "front" in item and "back" in item:
                self.add_card(item["front"], item["back"], item.get("tags", []))
                count += 1
        return count

    def get_due_cards(self) -> List[Flashcard]:
        now = datetime.now()
        due = []
        for card in self.cards:
            try:
                next_review = datetime.fromisoformat(card.next_review)
                if next_review <= now:
                    due.append(card)
            except (ValueError, TypeError):
                due.append(card)
        return due

    def get_stats(self) -> Dict:
        new = learning = mature = due = 0
        now = datetime.now()
        for card in self.cards:
            if card.total_reviews == 0:
                new += 1
            elif card.interval_days < 21:
                learning += 1
            else:
                mature += 1
            try:
                if datetime.fromisoformat(card.next_review) <= now:
                    due += 1
            except (ValueError, TypeError):
                due += 1
        return {"total": len(self.cards), "new": new, "learning": learning, "mature": mature, "due": due}

    def save(self, filepath: str):
        data = {
            "name": self.name, "topic": self.topic, "level": self.level,
            "description": self.description, "created_at": self.created_at,
            "cards": [asdict(card) for card in self.cards]
        }
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, filepath: str) -> "FlashcardDeck":
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        deck = cls(data["name"], data.get("topic", ""), data.get("level", ""))
        deck.created_at = data.get("created_at", "")
        deck.description = data.get("description", "")
        for card_data in data.get("cards", []):
            deck.cards.append(Flashcard(**card_data))
        return deck


class SpacedRepetition:
    def __init__(self):
        self.min_ease = 1.3
        self.max_ease = 3.0

    def review(self, card: Flashcard, quality: Quality) -> Flashcard:
        card.total_reviews += 1
        card.last_review = datetime.now().isoformat()

        if quality >= 3:
            card.correct_count += 1
            if card.repetitions == 0:
                card.interval_days = 1
            elif card.repetitions == 1:
                card.interval_days = 6
            else:
                card.interval_days = int(card.interval_days * card.ease_factor)
            card.repetitions += 1
        else:
            card.repetitions = 0
            card.interval_days = 1

        card.ease_factor += (0.1 - (5 - quality.value) * (0.08 + (5 - quality.value) * 0.02))
        card.ease_factor = max(self.min_ease, min(self.max_ease, card.ease_factor))
        card.next_review = (datetime.now() + timedelta(days=card.interval_days)).isoformat()
        return card

    def get_next_card(self, deck: FlashcardDeck) -> Optional[Flashcard]:
        due = deck.get_due_cards()
        if not due:
            return None
        due.sort(key=lambda c: (c.total_reviews > 0, c.ease_factor))
        return due[0]

    def get_review_session(self, deck: FlashcardDeck, max_cards: int = 20) -> List[Flashcard]:
        due = deck.get_due_cards()
        due.sort(key=lambda c: (c.total_reviews > 0, c.ease_factor))
        return due[:max_cards]
