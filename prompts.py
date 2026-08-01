def fill_blank_prompt(topic_name, level, count):
    return f"""Generate {count} fill-in-the-blank English grammar exercises for {level} level students.

Topic: {topic_name}

Context: These exercises are for Algerian middle school and high school students. Use relatable contexts like school, family, daily life in Algeria, food, weather, and local culture.

For each exercise, provide:
1. A sentence with a blank (use ___ for the blank)
2. The correct answer to fill in the blank
3. An optional hint (e.g., verb form needed)

Return ONLY a valid JSON array. Each element must have: "sentence", "answer", "hint"

Example format:
[
  {{"sentence": "My brother ___ to school every day.", "answer": "goes", "hint": "present simple, third person"}},
  {{"sentence": "We ___ fish on Fridays.", "answer": "eat", "hint": "present simple, first person plural"}}
]

Do NOT include any text outside the JSON array."""


def mcq_prompt(topic_name, level, count):
    return f"""Generate {count} multiple-choice English grammar exercises for {level} level students.

Topic: {topic_name}

Context: These exercises are for Algerian middle school and high school students. Use relatable contexts like school, family, daily life in Algeria, food, weather, and local culture.

For each exercise, provide:
1. A sentence with a blank or a question
2. Four options (A, B, C, D) - only ONE correct
3. The correct answer letter
4. A brief explanation of why it is correct

Return ONLY a valid JSON array. Each element must have: "question", "options" (array of 4 strings), "answer" (letter A/B/C/D), "explanation"

Example format:
[
  {{"question": "She ___ to the market yesterday.", "options": ["go", "goes", "went", "going"], "answer": "C", "explanation": "We use past simple for completed actions in the past."}}
]

Do NOT include any text outside the JSON array."""


def sentence_building_prompt(topic_name, level, count):
    return f"""Generate {count} sentence building exercises for {level} level students.

Topic: {topic_name}

Context: These exercises are for Algerian middle school and high school students. Use relatable contexts like school, family, daily life in Algeria, food, weather, and local culture.

For each exercise, provide:
1. A set of words in random order (a word bank)
2. The correct sentence that can be formed from those words
3. The punctuation needed

Return ONLY a valid JSON array. Each element must have: "words" (array of strings), "correct_sentence", "punctuation"

Example format:
[
  {{"words": ["goes", "Ali", "school", "to", "every", "day"], "correct_sentence": "Ali goes to school every day.", "punctuation": "period"}}
]

Do NOT include any text outside the JSON array."""


def transformation_prompt(topic_name, level, count):
    return f"""Generate {count} sentence transformation exercises for {level} level students.

Topic: {topic_name}

Context: These exercises are for Algerian middle school and high school students. Use relatable contexts like school, family, daily life in Algeria, food, weather, and local culture.

For each exercise, provide:
1. An original sentence
2. Instructions on how to transform it (e.g., "Make it negative", "Turn into a question", "Change to past simple")
3. The correct transformed sentence
4. An explanation of the transformation rule

Return ONLY a valid JSON array. Each element must have: "original", "instruction", "transformed", "explanation"

Example format:
[
  {{"original": "He goes to school.", "instruction": "Make it negative", "transformed": "He does not go to school.", "explanation": "Add 'does not' before the base form of the verb."}}
]

Do NOT include any text outside the JSON array."""


def error_correction_prompt(topic_name, level, count):
    return f"""Generate {count} error correction exercises for {level} level students.

Topic: {topic_name}

Context: These exercises are for Algerian middle school and high school students. Use relatable contexts like school, family, daily life in Algeria, food, weather, and local culture.

For each exercise, provide:
1. A sentence with a grammar error (common mistake Algerian students make)
2. The incorrect word or phrase underlined or highlighted
3. The correct version of the sentence
4. An explanation of the error

Return ONLY a valid JSON array. Each element must have: "incorrect_sentence", "error_part", "correct_sentence", "explanation"

Example format:
[
  {{"incorrect_sentence": "He go to school every day.", "error_part": "go", "correct_sentence": "He goes to school every day.", "explanation": "Third person singular requires -s on the verb in present simple."}}
]

Do NOT include any text outside the JSON array."""


def matching_prompt(topic_name, level, count):
    return f"""Generate {count} matching exercises for {level} level students.

Topic: {topic_name}

Context: These exercises are for Algerian middle school and high school students. Use relatable contexts like school, family, daily life in Algeria, food, weather, and local culture.

For each exercise, provide:
1. A left column item (e.g., a word, phrase, or sentence part)
2. The matching right column item (e.g., definition, translation, or completing phrase)
3. The correct pairing

Return ONLY a valid JSON array. Each element must have: "left", "right"

Example format:
[
  {{"left": "goes", "right": "he/she/it goes"}},
  {{"left": "go", "right": "I/you/we/they go"}}
]

Do NOT include any text outside the JSON array."""


PROMPT_BUILDERS = {
    "fill_in_blank": fill_blank_prompt,
    "multiple_choice": mcq_prompt,
    "sentence_building": sentence_building_prompt,
    "transformation": transformation_prompt,
    "error_correction": error_correction_prompt,
    "matching": matching_prompt,
}


def get_prompt(exercise_type, topic_name, level, count):
    builder = PROMPT_BUILDERS.get(exercise_type)
    if not builder:
        raise ValueError(f"Unknown exercise type: {exercise_type}")
    return builder(topic_name, level, count)
