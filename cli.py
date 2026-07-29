"""CLI entry point for Ta'allim."""

import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="Ta'allim — English teaching tools")
    sub = parser.add_subparsers(dest="command")

    # generate exercises
    gen_p = sub.add_parser("generate", help="Generate exercises")
    gen_p.add_argument("topic", help="Topic ID (e.g. present_simple)")
    gen_p.add_argument("-t", "--type", default="fill_in_blank", help="Exercise type")
    gen_p.add_argument("-n", "--count", type=int, default=10)
    gen_p.add_argument("-l", "--level", help="Force level (A1/A2/B1/B2)")
    gen_p.add_argument("--json", action="store_true", help="Output as JSON")
    gen_p.add_argument("--html", action="store_true", help="Output as HTML")
    gen_p.add_argument("--md", action="store_true", help="Output as Markdown")

    # list topics
    ls_p = sub.add_parser("topics", help="List topics")
    ls_p.add_argument("-l", "--level", help="Filter by level")

    # quiz
    quiz_p = sub.add_parser("quiz", help="Run MCQ quiz")
    quiz_p.add_argument("topic", help="Topic ID")
    quiz_p.add_argument("-n", "--count", type=int, default=10)

    # flashcards
    fc_p = sub.add_parser("flashcards", help="Flashcard deck stats")
    fc_p.add_argument("deck_file", help="Path to deck JSON")

    args = parser.parse_args()

    if args.command == "generate":
        from taallim.exercise_generator import ExerciseGenerator, to_html, to_markdown
        gen = ExerciseGenerator()
        result = gen.generate(args.topic, args.type, args.count)
        if "error" in result:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        if args.html:
            print(to_html([result]))
        elif args.md:
            print(to_markdown([result]))
        elif args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            for i, ex in enumerate(result["exercises"], 1):
                print(f"{i}. {ex}")

    elif args.command == "topics":
        from taallim.topics import get_topics_by_level, LEVELS
        levels = [args.level.upper()] if args.level else LEVELS
        for lv in levels:
            topics = get_topics_by_level(lv)
            print(f"\n{'='*50}")
            print(f"  Level {lv} ({len(topics)} topics)")
            print(f"{'='*50}")
            for t in topics:
                types = ", ".join(t.get("exercise_types", []))
                print(f"  {t['name']} [{t['id']}]")
                print(f"    {t['description']}")
                print(f"    Types: {types}")
                print()

    elif args.command == "quiz":
        from taallim.mcq_generator import MCQGenerator
        gen = MCQGenerator()
        questions = gen.generate(args.topic, count=args.count)
        score = 0
        for i, q in enumerate(questions, 1):
            print(f"\nQ{i}: {q['question']}")
            for j, opt in enumerate(q["options"]):
                print(f"  {chr(65+j)}) {opt}")
            answer = input("Your answer (A/B/C/D): ").strip().upper()
            correct_letter = chr(65 + q["correct"])
            if answer == correct_letter:
                score += 1
                print("  ✓ Correct!")
            else:
                print(f"  ✗ Wrong. Answer: {correct_letter}")
            print(f"  {q['explanation']}")
        print(f"\nScore: {score}/{len(questions)} ({score/len(questions)*100:.0f}%)")

    elif args.command == "flashcards":
        from taallim.flashcard_system import FlashcardDeck
        deck = FlashcardDeck.load(args.deck_file)
        stats = deck.get_stats()
        print(f"Deck: {deck.name}")
        print(f"Cards: {stats['total']}")
        print(f"New: {stats['new']}")
        print(f"Learning: {stats['learning']}")
        print(f"Mature: {stats['mature']}")
        print(f"Due: {stats['due']}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
