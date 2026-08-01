import json
import os
import sys
from topics import get_topics_by_level, get_topic_by_id, find_topic_by_name, list_topics_formatted
from offline_generator import OfflineGenerator

EXERCISE_TYPES = [
    "fill_in_blank", "multiple_choice", "sentence_building",
    "transformation", "error_correction", "matching"
]

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "generated")


def _get_api_key():
    return os.environ.get("ANTHROPIC_API_KEY", "")


def _generate_with_api(prompt, api_key):
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )
    text = message.content[0].text
    start = text.find("[")
    end = text.rfind("]") + 1
    if start != -1 and end > start:
        return json.loads(text[start:end])
    return json.loads(text)


class ExerciseGenerator:
    def __init__(self, api_key=None):
        self.api_key = api_key or _get_api_key()
        self.offline = OfflineGenerator()
        self.use_api = bool(self.api_key)

    def generate(self, topic_id, exercise_type, count=10):
        topic = get_topic_by_id(topic_id)
        if not topic:
            return {"error": f"Topic '{topic_id}' not found."}

        if exercise_type not in EXERCISE_TYPES:
            return {"error": f"Unknown type '{exercise_type}'. Use: {', '.join(EXERCISE_TYPES)}"}

        if exercise_type not in topic.get("exercise_types", []):
            return {"error": f"'{exercise_type}' is not recommended for topic '{topic['name']}'."}

        if self.use_api:
            try:
                from prompts import get_prompt
                prompt = get_prompt(exercise_type, topic["name"], topic["level"], count)
                exercises = _generate_with_api(prompt, self.api_key)
                return {
                    "topic": topic["name"],
                    "level": topic["level"],
                    "type": exercise_type,
                    "count": len(exercises),
                    "source": "api",
                    "exercises": exercises
                }
            except Exception as e:
                print(f"[API error: {e}. Falling back to offline mode.]", file=sys.stderr)

        exercises = self.offline.generate(exercise_type, topic_id, count)
        return {
            "topic": topic["name"],
            "level": topic["level"],
            "type": exercise_type,
            "count": len(exercises),
            "source": "offline",
            "exercises": exercises
        }

    def generate_for_level(self, level, exercise_type=None, count=10):
        topics = get_topics_by_level(level)
        if not topics:
            return {"error": f"No topics found for level '{level}'."}

        results = []
        for topic in topics:
            if exercise_type and exercise_type != "all":
                types_to_gen = [exercise_type]
            else:
                types_to_gen = topic.get("exercise_types", [])
            for etype in types_to_gen:
                result = self.generate(topic["id"], etype, count)
                if "error" not in result:
                    results.append(result)
        return results

    def save(self, data, filename=None):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        if not filename:
            import datetime
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"exercises_{ts}.json"
        path = os.path.join(OUTPUT_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return path


def to_markdown(data):
    lines = []
    if isinstance(data, dict) and "exercises" in data:
        data = [data]
    for item in data:
        lines.append(f"# {item['topic']} ({item['level']}) - {item['type'].replace('_', ' ').title()}")
        lines.append(f"Source: {item['source']} | Count: {item['count']}\n")
        for i, ex in enumerate(item["exercises"], 1):
            lines.append(f"**{i}.** ", )
            if item["type"] == "fill_in_blank":
                lines.append(f"  {ex['sentence']}")
                lines.append(f"  **Answer:** {ex['answer']}")
                if ex.get("hint"):
                    lines.append(f"  *Hint:* {ex['hint']}")
            elif item["type"] == "multiple_choice":
                lines.append(f"  {ex['question']}")
                for j, opt in enumerate(ex["options"]):
                    letter = chr(65 + j)
                    marker = " *" if letter == ex["answer"] else ""
                    lines.append(f"    {letter}) {opt}{marker}")
                lines.append(f"  **Answer:** {ex['answer']} - {ex.get('explanation', '')}")
            elif item["type"] == "sentence_building":
                lines.append(f"  Arrange: {ex['words']}")
                lines.append(f"  **Answer:** {ex['correct_sentence']}")
            elif item["type"] == "transformation":
                lines.append(f"  Original: {ex['original']}")
                lines.append(f"  Task: {ex['instruction']}")
                lines.append(f"  **Answer:** {ex['transformed']}")
                lines.append(f"  *Rule:* {ex.get('explanation', '')}")
            elif item["type"] == "error_correction":
                lines.append(f"  Find the error: {ex['incorrect_sentence']}")
                lines.append(f"  **Correct:** {ex['correct_sentence']}")
                lines.append(f"  *Explanation:* {ex.get('explanation', '')}")
            elif item["type"] == "matching":
                lines.append(f"  Match: {ex['left']} <-> {ex['right']}")
            lines.append("")
        lines.append("---\n")
    return "\n".join(lines)


def to_html(data):
    if isinstance(data, dict) and "exercises" in data:
        data = [data]
    html_parts = ["""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>English Exercises</title>
<style>
body{font-family:Arial,sans-serif;max-width:800px;margin:0 auto;padding:20px;line-height:1.6}
h1{color:#2c3e50;border-bottom:2px solid #3498db;padding-bottom:10px}
h2{color:#2980b9;margin-top:30px}
.exercise{background:#f8f9fa;border-left:4px solid #3498db;padding:12px 16px;margin:10px 0;border-radius:4px}
.answer{color:#27ae60;font-weight:bold}
.hint{color:#7f8c8d;font-style:italic}
.option{margin-left:20px}
.correct{background:#d5f5e3;padding:2px 4px;border-radius:3px}
@media print{body{font-size:12pt} .exercise{break-inside:avoid}}</style>
</head><body><h1>English Grammar Exercises</h1>
"""]
    for item in data:
        html_parts.append(f"<h2>{item['topic']} ({item['level']}) - {item['type'].replace('_', ' ').title()}</h2>")
        html_parts.append(f"<p><em>Source: {item['source']} | Count: {item['count']}</em></p>")
        for i, ex in enumerate(item["exercises"], 1):
            html_parts.append('<div class="exercise">')
            html_parts.append(f"<strong>{i}.</strong> ")
            if item["type"] == "fill_in_blank":
                html_parts.append(f"<p>{ex['sentence']}</p>")
                html_parts.append(f"<p class='answer'>Answer: {ex['answer']}</p>")
                if ex.get("hint"):
                    html_parts.append(f"<p class='hint'>Hint: {ex['hint']}</p>")
            elif item["type"] == "multiple_choice":
                html_parts.append(f"<p>{ex['question']}</p>")
                for j, opt in enumerate(ex["options"]):
                    letter = chr(65 + j)
                    cls = ' class="correct"' if letter == ex["answer"] else ""
                    html_parts.append(f"<p class='option'{cls}>{letter}) {opt}</p>")
                html_parts.append(f"<p class='answer'>Answer: {ex['answer']} - {ex.get('explanation', '')}</p>")
            elif item["type"] == "sentence_building":
                html_parts.append(f"<p>Arrange: <strong>{ex['words']}</strong></p>")
                html_parts.append(f"<p class='answer'>Answer: {ex['correct_sentence']}</p>")
            elif item["type"] == "transformation":
                html_parts.append(f"<p>Original: {ex['original']}</p>")
                html_parts.append(f"<p>Task: {ex['instruction']}</p>")
                html_parts.append(f"<p class='answer'>Answer: {ex['transformed']}</p>")
                html_parts.append(f"<p class='hint'>Rule: {ex.get('explanation', '')}</p>")
            elif item["type"] == "error_correction":
                html_parts.append(f"<p>Find the error: {ex['incorrect_sentence']}</p>")
                html_parts.append(f"<p class='answer'>Correct: {ex['correct_sentence']}</p>")
                html_parts.append(f"<p class='hint'>Explanation: {ex.get('explanation', '')}</p>")
            elif item["type"] == "matching":
                html_parts.append(f"<p>Match: <strong>{ex['left']}</strong> &lt;-&gt; {ex['right']}</p>")
            html_parts.append("</div>")
    html_parts.append("</body></html>")
    return "\n".join(html_parts)
