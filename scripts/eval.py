"""Week 6 evaluation harness.

Reads eval/questions.jsonl, runs each question through retrieval (and, once it's
wired, the full answer path), and reports how often the right doc came back and
how often the answer was acceptable.

    python scripts/eval.py

This is a STUB. The scoring loop below is the shape from Week 6; fill in the
answer call once you expose one (e.g. answer_question()).
"""

import json
import sys
from pathlib import Path

# Run from anywhere: put the repo root (this file's parent's parent) on the path
# so `python scripts/eval.py` finds the `src/` package without needing `-m`.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.embed.search import search
from src.ui.chat import answer_question


def load_questions(path: str = "eval/questions.jsonl") -> list[dict]:
    """Load one JSON object per line. See eval/questions.jsonl for the format."""
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def main() -> None:
    questions = load_questions()
    # TODO(week-06): split into train/test (e.g. questions[:20], questions[20:])
    # and NEVER tune against the held-out test set.

    scores = {"retrieval_hit": 0, "answer_ok": 0}

    for item in questions:
        chunks = search(item["q"], k=5)
        retrieved_sources = [c["source_url"] for c in chunks]
        if any(item["expected_source"] in s for s in retrieved_sources):
            scores["retrieval_hit"] += 1

        # answer_question returns {"answer": str, "chunks": list[dict]} (see
        # docs/INTERFACES.md). The answer is "" until generation is wired.
        result = answer_question(item["q"], k=5)
        answer = result["answer"]
        # TODO(week-06): judge the answer (eyeball or LLM-as-judge), e.g.:
        #   if answer_is_ok(answer, item["ideal"]): scores["answer_ok"] += 1

    total = len(questions)
    print(f"Retrieval hit-rate: {scores['retrieval_hit']}/{total}")
    print(f"Answers OK:         {scores['answer_ok']}/{total}")


if __name__ == "__main__":
    main()
