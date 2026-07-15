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
import json
import os

import chromadb
from dotenv import load_dotenv
from openai import OpenAI


def embed(text: str) -> list[float]:
    """Return the embedding vector for ``text`` using the NRP embedding model.

    Use the SAME model here as you used to index, or retrieval returns garbage.

        from openai import OpenAI
        client = OpenAI(api_key=TOKEN, base_url=BASE_URL)
        resp = client.embeddings.create(model="qwen3-embedding", input=[text])
        return resp.data[0].embedding
    """
    return (
        client.embeddings.create(model="qwen3-embedding", input=[text])
        .data[0]
        .embedding
    )


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
    res = coll.query(query_embeddings=[embed(query)], n_results=k)

    # Use .get() with a fallback to empty lists to satisfy the type-checker
    documents = res.get("documents") or []
    metadatas = res.get("metadatas") or []
    distances = res.get("distances") or []

    # Ensure we actually got results before indexing [0]
    docs_list = documents[0] if documents else []
    meta_list = metadatas[0] if metadatas else []
    dist_list = distances[0] if distances else []

    return [
        {"text": d, "source_url": m["source_url"], "title": m["title"], "score": s}
        for d, m, s in zip(docs_list, meta_list, dist_list)
    ]


# load json
with open("data/chunks/chunks.json", "r") as f:
    chunks = json.load(f)

# env openai
load_dotenv()
client = OpenAI(
    api_key=os.environ["NRP_LLM_TOKEN"], base_url=os.environ["NRP_LLM_BASE_URL"]
)

# start chromadb
coll = chromadb.PersistentClient(path="./chroma_db").get_or_create_collection(
    "nrp_docs"
)
coll.add(
    ids=[c["id"] for c in chunks],
    documents=[c["text"] for c in chunks],
    embeddings=[embed(c["text"]) for c in chunks],
    metadatas=[{"source_url": c["source_url"], "title": c["title"]} for c in chunks],
)
