"""Embed — retrieval over the NRP doc chunks.

This module exposes ONE function the rest of the system depends on: ``search``.
The UI calls it; Week 6's eval harness calls it. Its signature and return
shape are a CONTRACT — see docs/INTERFACES.md. Do not change them without telling
the other pairs.

Implementation plan (Week 5):
  1. Read chunks (data/chunks/*.json).
  2. Embed each chunk's text with the NRP ``qwen3-embedding`` model.
  3. Index them in a local Chroma collection ("./chroma_db", collection "nrp_docs").
  4. Implement ``search`` to embed the query and return the k nearest chunks.

The indexing code typically lives in scripts/ (e.g. scripts/index.py) and runs once;
this file only needs the query-time ``search`` and a shared ``embed`` helper.
"""

from __future__ import annotations


def embed(text: str) -> list[float]:
    """Return the embedding vector for ``text`` using the NRP embedding model.

    Use the SAME model here as you used to index, or retrieval returns garbage.

        from openai import OpenAI
        client = OpenAI(api_key=TOKEN, base_url=BASE_URL)
        resp = client.embeddings.create(model="qwen3-embedding", input=[text])
        return resp.data[0].embedding
    """
    # TODO(week-05): call the NRP qwen3-embedding model and return the vector.
    raise NotImplementedError("Week 5: implement embed().")


def search(query: str, k: int = 5) -> list[dict]:
    """Return the ``k`` chunks most relevant to ``query``.

    CONTRACT (see docs/INTERFACES.md) — each returned dict MUST have exactly:
        {
            "text":       str,    # the chunk text
            "source_url": str,    # original nrp.ai page, for citation
            "title":      str,    # page title, for citation
            "score":      float,  # distance/similarity from Chroma
        }

    Reference implementation shape (Week 5):
        q_vec = embed(query)
        results = coll.query(query_embeddings=[q_vec], n_results=k)
        return [
            {"text": doc, "source_url": meta["source_url"],
             "title": meta["title"], "score": dist}
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            )
        ]

    Graceful empty case (required by Week 7): if the Chroma collection is empty
    or does not exist yet, return ``[]`` — DO NOT crash. The UI shows a friendly
    "no docs indexed yet" message when this returns an empty list.
    """
    # TODO(week-05): implement real retrieval against Chroma.
    # Returning [] keeps the app (and the eval harness) importable and runnable
    # before retrieval is wired up, and is also the correct empty-collection answer.
    return []
