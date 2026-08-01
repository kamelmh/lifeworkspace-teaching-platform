import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "topics")

LEVELS = ["A1", "A2", "B1", "B2"]


def _load_level_data(level):
    path = os.path.join(DATA_DIR, f"{level}.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("topics", [])


def get_all_topics():
    all_topics = {}
    for level in LEVELS:
        topics = _load_level_data(level)
        for topic in topics:
            topic["level"] = level
            all_topics[topic["id"]] = topic
    return all_topics


def get_topics_by_level(level):
    level = level.upper()
    topics = _load_level_data(level)
    for t in topics:
        t["level"] = level
    return topics


def get_topic_by_id(topic_id):
    for level in LEVELS:
        topics = _load_level_data(level)
        for t in topics:
            if t["id"] == topic_id:
                t["level"] = level
                return t
    return None


def find_topic_by_name(name):
    name_lower = name.lower()
    for level in LEVELS:
        topics = _load_level_data(level)
        for t in topics:
            if t["name"].lower() == name_lower:
                t["level"] = level
                return t
    for level in LEVELS:
        topics = _load_level_data(level)
        for t in topics:
            if name_lower in t["name"].lower():
                t["level"] = level
                return t
    return None


def list_topics_formatted():
    lines = []
    for level in LEVELS:
        topics = _load_level_data(level)
        lines.append(f"\n{'='*50}")
        lines.append(f"  Level {level} ({len(topics)} topics)")
        lines.append(f"{'='*50}")
        for t in topics:
            types = ", ".join(t.get("exercise_types", []))
            lines.append(f"  {t['name']}")
            lines.append(f"    ID: {t['id']}")
            lines.append(f"    {t['description']}")
            lines.append(f"    Exercise types: {types}")
            lines.append("")
    return "\n".join(lines)
