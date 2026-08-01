import random


def _pick(items, count):
    if count >= len(items):
        return items[:]
    return random.sample(items, count)


def _shuffle_and_join(words):
    shuffled = words[:]
    random.shuffle(shuffled)
    return " ".join(shuffled)


class OfflineGenerator:
    def generate(self, exercise_type, topic_id, count):
        method = getattr(self, f"_gen_{exercise_type}", None)
        if not method:
            raise ValueError(f"Unknown exercise type: {exercise_type}")
        return method(topic_id, count)

    def _gen_fill_in_blank(self, topic_id, count):
        from offline_data import FILL_BLANK_BANKS
        bank = FILL_BLANK_BANKS.get(topic_id, [])
        if not bank:
            return self._fallback_fill_blank(topic_id, count)
        items = _pick(bank, count)
        return [{"type": "fill_in_blank", "sentence": s, "answer": a, "hint": h} for s, a, h in items]

    def _gen_multiple_choice(self, topic_id, count):
        from offline_data import MCQ_BANKS
        bank = MCQ_BANKS.get(topic_id, [])
        if not bank:
            return self._fallback_mcq(topic_id, count)
        items = _pick(bank, count)
        return [{"type": "multiple_choice", **item} for item in items]

    def _gen_sentence_building(self, topic_id, count):
        from offline_data import SENTENCE_BUILDING_BANKS
        bank = SENTENCE_BUILDING_BANKS.get(topic_id, [])
        if not bank:
            return self._fallback_sentence_building(topic_id, count)
        items = _pick(bank, count)
        results = []
        for words in items:
            correct = " ".join(words)
            shuffled = _shuffle_and_join(words)
            results.append({
                "type": "sentence_building",
                "words": shuffled,
                "correct_sentence": correct,
            })
        return results

    def _gen_error_correction(self, topic_id, count):
        from offline_data import ERROR_CORRECTION_BANKS
        bank = ERROR_CORRECTION_BANKS.get(topic_id, [])
        if not bank:
            return self._fallback_error_correction(topic_id, count)
        items = _pick(bank, count)
        return [{"type": "error_correction", **item} for item in items]

    def _gen_matching(self, topic_id, count):
        from offline_data import MATCHING_BANKS
        bank = MATCHING_BANKS.get(topic_id, [])
        if not bank:
            return self._fallback_matching(topic_id, count)
        items = _pick(bank, count)
        return [{"type": "matching", **item} for item in items]

    def _gen_transformation(self, topic_id, count):
        from offline_data import TRANSFORMATION_BANKS
        bank = TRANSFORMATION_BANKS.get(topic_id, [])
        if not bank:
            return self._fallback_transformation(topic_id, count)
        items = _pick(bank, count)
        return [{"type": "transformation", **item} for item in items]

    # ---------- fallback generators ----------

    def _fallback_fill_blank(self, topic_id, count):
        templates = [
            ("The students ___ hard for the exam.", "study", "present simple"),
            ("She ___ to school every day.", "goes", "third person"),
            ("We ___ English on Mondays.", "study", "first person plural"),
            ("He ___ not like cold weather.", "does", "negative form"),
            ("___ you speak Arabic at home?", "Do", "question form"),
            ("My mother ___ breakfast at 7.", "makes", "third person"),
            ("The sun ___ in the east.", "rises", "general fact"),
            ("They ___ football after school.", "play", "third person plural"),
            ("I ___ tea in the morning.", "drink", "first person"),
            ("The school ___ at 8 a.m.", "starts", "third person"),
        ]
        items = _pick(templates, count)
        return [{"type": "fill_in_blank", "sentence": s, "answer": a, "hint": h} for s, a, h in items]

    def _fallback_mcq(self, topic_id, count):
        templates = [
            {"question": "She ___ to school every day.", "options": ["go", "goes", "going", "gone"], "answer": "B", "explanation": "Third person singular adds -s."},
            {"question": "We ___ English on Mondays.", "options": ["studies", "studys", "study", "studying"], "answer": "C", "explanation": "First person plural uses base form."},
            {"question": "He ___ a student.", "options": ["am", "is", "are", "be"], "answer": "B", "explanation": "He + is in present simple."},
            {"question": "They ___ not like fish.", "options": ["does", "doesn't", "don't", "isn't"], "answer": "C", "explanation": "Third person plural uses don't."},
            {"question": "I ___ a book yesterday.", "options": ["read", "reads", "readed", "reading"], "answer": "A", "explanation": "Read is the same in past simple."},
            {"question": "She ___ from Algiers.", "options": ["am", "is", "are", "be"], "answer": "B", "explanation": "She + is."},
            {"question": "The children ___ in the park.", "options": ["play", "plays", "played", "playing"], "answer": "C", "explanation": "Past simple adds -ed."},
            {"question": "He ___ speak French.", "options": ["can", "must", "should", "need"], "answer": "A", "explanation": "Can expresses ability."},
            {"question": "We ___ happy today.", "options": ["am", "is", "are", "be"], "answer": "C", "explanation": "We + are."},
            {"question": "___ it rain tomorrow?", "options": ["Will", "Do", "Does", "Is"], "answer": "A", "explanation": "Will for future questions."},
        ]
        items = _pick(templates, count)
        return [{"type": "multiple_choice", **item} for item in items]

    def _fallback_sentence_building(self, topic_id, count):
        templates = [
            ["Ali", "goes", "to", "school", "every", "day."],
            ["We", "study", "English", "on", "Mondays."],
            ["She", "eats", "breakfast", "at", "7", "o'clock."],
            ["They", "play", "football", "after", "school."],
            ["My", "mother", "cleans", "the", "house."],
            ["I", "drink", "tea", "in", "the", "morning."],
            ["He", "does", "not", "like", "fish."],
            ["The", "sun", "rises", "in", "the", "east."],
            ["We", "go", "to", "the", "mosque", "on", "Fridays."],
            ["She", "watches", "TV", "every", "evening."],
        ]
        items = _pick(templates, count)
        results = []
        for words in items:
            correct = " ".join(words)
            shuffled = _shuffle_and_join(words)
            results.append({
                "type": "sentence_building",
                "words": shuffled,
                "correct_sentence": correct,
            })
        return results

    def _fallback_error_correction(self, topic_id, count):
        templates = [
            {"incorrect_sentence": "He go to school every day.", "error_part": "go", "correct_sentence": "He goes to school every day.", "explanation": "Third person singular requires -s."},
            {"incorrect_sentence": "She don't like fish.", "error_part": "don't", "correct_sentence": "She doesn't like fish.", "explanation": "Third person singular uses doesn't."},
            {"incorrect_sentence": "I am student.", "error_part": "am student", "correct_sentence": "I am a student.", "explanation": "Missing article 'a'."},
            {"incorrect_sentence": "We is happy.", "error_part": "is", "correct_sentence": "We are happy.", "explanation": "We + are in present simple."},
            {"incorrect_sentence": "She study English.", "error_part": "study", "correct_sentence": "She studies English.", "explanation": "Third person singular adds -ies."},
            {"incorrect_sentence": "He have a new car.", "error_part": "have", "correct_sentence": "He has a new car.", "explanation": "Third person of have is has."},
            {"incorrect_sentence": "They plays football.", "error_part": "plays", "correct_sentence": "They play football.", "explanation": "Third person plural does not add -s."},
            {"incorrect_sentence": "I go to beach yesterday.", "error_part": "go", "correct_sentence": "I went to the beach yesterday.", "explanation": "Use past simple for past actions."},
            {"incorrect_sentence": "She eated breakfast.", "error_part": "eated", "correct_sentence": "She ate breakfast.", "explanation": "Eat is irregular: eat-ate-eaten."},
            {"incorrect_sentence": "He didn't went to school.", "error_part": "didn't went", "correct_sentence": "He didn't go to school.", "explanation": "After didn't use base form."},
        ]
        items = _pick(templates, count)
        return [{"type": "error_correction", **item} for item in items]

    def _fallback_matching(self, topic_id, count):
        templates = [
            {"left": "I", "right": "first person singular"},
            {"left": "You", "right": "second person"},
            {"left": "He", "right": "third person singular male"},
            {"left": "She", "right": "third person singular female"},
            {"left": "We", "right": "first person plural"},
            {"left": "They", "right": "third person plural"},
            {"left": "am", "right": "used with I"},
            {"left": "is", "right": "used with he/she/it"},
            {"left": "are", "right": "used with you/we/they"},
            {"left": "a", "right": "before consonant sounds"},
        ]
        items = _pick(templates, count)
        return [{"type": "matching", **item} for item in items]

    def _fallback_transformation(self, topic_id, count):
        templates = [
            {"original": "Ali goes to school.", "instruction": "Make it negative", "transformed": "Ali does not go to school.", "explanation": "Add does not before base form."},
            {"original": "She studies English.", "instruction": "Make it a question", "transformed": "Does she study English?", "explanation": "Move does to the beginning."},
            {"original": "I am a student.", "instruction": "Make it negative", "transformed": "I am not a student.", "explanation": "Add not after am."},
            {"original": "He is from Oran.", "instruction": "Make it a question", "transformed": "Is he from Oran?", "explanation": "Move is to the beginning."},
            {"original": "We are happy.", "instruction": "Make it negative", "transformed": "We are not happy.", "explanation": "Add not after are."},
            {"original": "They play football.", "instruction": "Make it negative", "transformed": "They do not play football.", "explanation": "Add do not before base form."},
            {"original": "She drinks tea.", "instruction": "Make it a question", "transformed": "Does she drink tea?", "explanation": "Move does to the beginning."},
            {"original": "He eats breakfast.", "instruction": "Make it negative", "transformed": "He does not eat breakfast.", "explanation": "Add does not before base form."},
            {"original": "We study English.", "instruction": "Add a frequency adverb", "transformed": "We always study English.", "explanation": "Add always after the subject."},
            {"original": "The sun rises in the east.", "instruction": "Make it a question", "transformed": "Does the sun rise in the east?", "explanation": "Move does to the beginning."},
        ]
        items = _pick(templates, count)
        return [{"type": "transformation", **item} for item in items]
