"""UI — RAG orchestration: retrieve, ground, generate.

Factored out of the Streamlit ``app.py`` so the Week 6 eval harness
(``scripts/eval.py``) can import ``answer_question`` and score it WITHOUT
spinning up a UI. Keeping it here is a CONTRACT — see docs/INTERFACES.md.
You may instead keep this logic inline in app.py; if so, mirror this exact
signature so eval.py's import still resolves.

Implementation plan (Week 5):
  1. ``search(question, k)`` for the most relevant chunks (the shared contract).
  2. Build grounded chat messages: system prompt + numbered docs + question.
  3. Call the NRP ``gpt-oss`` chat model with those messages.
  4. Return BOTH the answer text and the chunks used, so the UI can render
     citations and eval.py can check which sources were retrieved.
"""

from __future__ import annotations

from src.embed.search import search


def answer_question(question: str, k: int = 5) -> dict:
    """Answer ``question`` from the NRP docs, with citations.

    CONTRACT (see docs/INTERFACES.md) — returns a dict with EXACTLY these keys:
        {
            "answer": str,         # the model's grounded answer text
            "chunks": list[dict],  # the search() results used as context
                                   # (each is the search() chunk dict:
                                   #  {"text","source_url","title","score"})
        }

    Reference implementation shape (Week 5):
        chunks = search(question, k=k)
        messages = build_grounded_messages(question, chunks)
        resp = client.chat.completions.create(model=LLM_MODEL, messages=messages)
        return {"answer": resp.choices[0].message.content, "chunks": chunks}

    Graceful pre-wiring case: until generation is implemented, retrieval still
    works (or returns [] on an empty collection), so eval.py can already run the
    retrieval half. Return the chunks with an empty answer rather than crashing.
    """
    # TODO(week-05): call the NRP gpt-oss model with grounded messages and
    # return its answer. For now, return retrieval-only so scripts/eval.py and
    # the Week-6 import work before generation is wired up.
    chunks = search(question, k=k)
    return {"answer": "", "chunks": chunks}
