"""
Ta'allim MCQ Generator
Multiple Choice Question builder with distractor generation

Usage:
    from mcq_generator import MCQGenerator

    gen = MCQGenerator()
    questions = gen.generate(topic="past_simple", count=5, level="A2")
"""

import json
import os
import random
from typing import List, Dict, Optional


# Algerian curriculum grammar topics with common errors
TOPICS = {
    "past_simple": {
        "name": "Past Simple",
        "rules": [
            "Subject + V2 (past form)",
            "Irregular verbs: go/went, eat/ate, see/saw, take/took",
            "Regular verbs: +ed (walked, played, watched)",
            "Neg: did not + base verb",
            "Q: Did + subject + base verb?"
        ],
        "common_errors": [
            "She goed (wrong - went)",
            "I didn't went (wrong - didn't go)",
            "Did she went? (wrong - did she go?)"
        ]
    },
    "present_perfect": {
        "name": "Present Perfect",
        "rules": [
            "Subject + have/has + V3 (past participle)",
            "Irregular: go/gone, eat/eaten, see/seen",
            "Regular: +ed (walked, played)",
            "For/since/yet/already/just"
        ],
        "common_errors": [
            "She has went (wrong - has gone)",
            "I have eat (wrong - have eaten)",
            "I am knowing (wrong - I know)"
        ]
    },
    "conditionals": {
        "name": "Conditionals",
        "rules": [
            "Zero: If + present, present (facts)",
            "First: If + present, will + base (real future)",
            "Second: If + past, would + base (unreal present)",
            "Third: If + past perfect, would have + V3 (unreal past)"
        ],
        "common_errors": [
            "If I will go (wrong - If I go)",
            "If I would have money (wrong - If I had money)"
        ]
    },
    "passive_voice": {
        "name": "Passive Voice",
        "rules": [
            "Subject + be + V3 (+ by agent)",
            "Present: is/are + V3",
            "Past: was/were + V3",
            "Future: will be + V3"
        ],
        "common_errors": [
            "The book read by me (wrong - is read)",
            "The house was build (wrong - was built)"
        ]
    },
    "reported_speech": {
        "name": "Reported Speech",
        "rules": [
            "S + said (that) + clause",
            "Tense shift: present->past, will->would",
            "Pronoun change: I->he/she, my->his/her",
            "Time shift: now->then, today->that day"
        ],
        "common_errors": [
            "He said me (wrong - he told me / he said to me)",
            "She said that she will come (wrong - would come)"
        ]
    }
}


class MCQGenerator:
    def __init__(self):
        self.topics = TOPICS

    def generate(self, topic: str, count: int = 5, level: str = "A2",
                 api_key: str = None) -> List[Dict]:
        if api_key:
            try:
                return self._generate_with_api(topic, count, level, api_key)
            except Exception:
                pass
        return self._generate_offline(topic, count, level)

    def _generate_offline(self, topic: str, count: int, level: str) -> List[Dict]:
        topic_data = self.topics.get(topic)
        if not topic_data:
            return [{"error": f"Topic '{topic}' not found. Available: {list(self.topics.keys())}"}]

        questions = []
        for i in range(count):
            q = self._make_question(topic_data, i)
            questions.append(q)
        return questions

    def _make_question(self, topic_data: Dict, seed: int) -> Dict:
        rules = topic_data["rules"]
        errors = topic_data.get("common_errors", [])

        templates = [
            {"type": "rule_application", "weight": 40},
            {"type": "error_identification", "weight": 30},
            {"type": "fill_blank", "weight": 30}
        ]

        t = random.choice(templates)

        if t["type"] == "error_identification" and errors:
            return self._error_question(errors, topic_data["name"])
        elif t["type"] == "fill_blank":
            return self._fill_blank_question(topic_data)
        else:
            return self._rule_question(topic_data)

    def _error_question(self, errors: List[str], topic_name: str) -> Dict:
        error = random.choice(errors)
        parts = error.split(" (wrong - ")
        wrong_sentence = parts[0]
        correct_answer = parts[1].rstrip(")") if len(parts) > 1 else "correct form"

        distractors = [
            "Both are correct",
            "Neither is correct",
            "The sentence is correct as written"
        ]

        options = [correct_answer] + distractors[:3]
        random.shuffle(options)
        correct_idx = options.index(correct_answer)

        return {
            "question": f"Which sentence is INCORRECT?",
            "context": wrong_sentence,
            "options": options,
            "correct": correct_idx,
            "explanation": f"In {topic_name}, the correct form is: {correct_answer}",
            "type": "error_identification"
        }

    def _fill_blank_question(self, topic_data: Dict) -> Dict:
        sentences = {
            "past_simple": [
                ("She ______ to school yesterday.", ["went", "goes", "going", "go"], 0),
                ("I ______ (not see) him last week.", ["didn't see", "didn't saw", "don't see", "haven't seen"], 0),
                ("______ you ______ (visit) your grandmother?", ["Did, visit", "Did, visited", "Do, visit", "Have, visited"], 0),
                ("They ______ (play) football after school.", ["played", "play", "playing", "plays"], 0),
                ("We ______ (not eat) lunch yet.", ["didn't eat", "don't eat", "haven't eaten", "didn't ate"], 0)
            ],
            "present_perfect": [
                ("I ______ (visit) Paris twice.", ["have visited", "visited", "am visiting", "visit"], 0),
                ("She ______ (already finish) her homework.", ["has already finished", "already finished", "is already finishing", "already finishes"], 0),
                ("He ______ (not see) that movie yet.", ["hasn't seen", "didn't see", "doesn't see", "isn't seeing"], 0),
                ("______ you ______ (eat) lunch?", ["Have, eaten", "Did, eat", "Are, eating", "Do, eat"], 0),
                ("We ______ (live) here since 2020.", ["have lived", "lived", "are living", "live"], 0)
            ],
            "conditionals": [
                ("If it ______ (rain), I will stay home.", ["rains", "rained", "will rain", "raining"], 0),
                ("If I ______ (be) rich, I would travel the world.", ["were", "am", "will be", "would be"], 0),
                ("If she ______ (study) harder, she would pass.", ["studied", "studies", "would study", "will study"], 0),
                ("If they ______ (arrive) earlier, they would have caught the bus.", ["had arrived", "arrived", "would arrive", "arrive"], 0),
                ("If I ______ (know) his number, I would call him.", ["knew", "know", "would know", "will know"], 0)
            ],
            "passive_voice": [
                ("The book ______ (read) by many students.", ["is read", "reads", "reading", "read"], 0),
                ("The house ______ (build) in 1990.", ["was built", "built", "is built", "building"], 0),
                ("English ______ (speak) worldwide.", ["is spoken", "speaks", "speaking", "spoken"], 0),
                ("The homework ______ (finish) by tomorrow.", ["will be finished", "finishes", "is finished", "finished"], 0),
                ("The cake ______ (eat) by the children.", ["was eaten", "ate", "eating", "eaten"], 0)
            ],
            "reported_speech": [
                ('He said that he ______ (come) yesterday.', ["had come", "came", "comes", "has come"], 0),
                ('She told me that she ______ (be) tired.', ["was", "is", "had been", "has been"], 0),
                ('They said they ______ (finish) the work.', ["had finished", "finished", "finish", "have finished"], 0),
                ('He asked me where I ______ (live).', ["lived", "live", "was living", "had lived"], 0),
                ('She said she ______ (not see) the film.', ["hadn't seen", "didn't see", "hasn't seen", "doesn't see"], 0)
            ]
        }

        topic_name = topic_data["name"].lower().replace(" ", "_")
        sents = sentences.get(topic_name, sentences["past_simple"])
        sent, opts, correct = random.choice(sents)

        return {
            "question": f"Complete the sentence:",
            "context": sent,
            "options": opts,
            "correct": correct,
            "explanation": f"Correct answer: {opts[correct]}",
            "type": "fill_blank"
        }

    def _rule_question(self, topic_data: Dict) -> Dict:
        rules = topic_data["rules"]
        rule = random.choice(rules)

        options_map = {
            "Subject + V2 (past form)": [
                "Subject + V2 (past form)",
                "Subject + V1 (base form)",
                "Subject + will + V1",
                "Subject + is + V-ing"
            ],
            "Subject + have/has + V3 (past participle)": [
                "Subject + have/has + V3 (past participle)",
                "Subject + had + V2",
                "Subject + has + V-ing",
                "Subject + have + V1"
            ],
            "Subject + be + V3 (+ by agent)": [
                "Subject + be + V3 (+ by agent)",
                "Subject + have + V3",
                "Subject + be + V-ing",
                "Subject + V3"
            ],
            "S + said (that) + clause": [
                "S + said (that) + clause",
                "S + tell (that) + clause",
                "S + said to + clause",
                "S + speaks (that) + clause"
            ]
        }

        options = options_map.get(rule, [rule, "None of the above", "All are correct", "Depends on context"])
        correct_idx = 0

        return {
            "question": f"In {topic_data['name']}, which is the correct structure?",
            "context": "",
            "options": options,
            "correct": correct_idx,
            "explanation": f"The correct structure is: {rule}",
            "type": "rule_application"
        }

    def _generate_with_api(self, topic: str, count: int, level: str, api_key: str) -> List[Dict]:
        import anthropic
        topic_data = self.topics.get(topic, {})
        topic_name = topic_data.get("name", topic)

        prompt = f"""Generate {count} multiple choice questions for {topic_name} English grammar.
Level: {level}
For each question provide:
- question: the question text
- context: sentence with blank (if applicable)
- options: array of 4 options
- correct: index of correct answer (0-3)
- explanation: why the answer is correct
- type: "fill_blank" or "error_identification" or "rule_application"

Return as JSON array. Make questions realistic for Algerian students."""

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

    def generate_from_text(self, text: str, count: int = 5, api_key: str = None) -> List[Dict]:
        if not api_key:
            return self._generate_offline("past_simple", count, "A2")

        import anthropic
        prompt = f"""Analyze this English text and generate {count} MCQ questions.
Text: {text[:2000]}

For each question provide:
- question: the question text
- context: sentence with blank (if applicable)
- options: array of 4 options
- correct: index of correct answer (0-3)
- explanation: why the answer is correct
- type: "comprehension" or "vocabulary" or "grammar"

Return as JSON array."""

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
