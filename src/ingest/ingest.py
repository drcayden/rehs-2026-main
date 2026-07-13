"""Ingest — scrape, clean, and chunk the NRP docs.

Goal (Week 5): produce >=100 clean text chunks from the NRP docs site, written to
``data/chunks/`` as JSON, one file per chunk.

Approach options (pick one Monday):
  - Easiest: clone nrp-nautilus/documentation (already markdown — no scraping).
  - Web scraping: requests + beautifulsoup4 over nrp.ai/documentation/.
  - Sitemap: parse nrp.ai/sitemap.xml to enumerate pages.

Chunking target: ~500 tokens (~2000 chars) with ~100-token overlap. Keep the
source URL on every chunk so the UI can cite it.

------------------------------------------------------------------------------
CHUNK JSON SCHEMA (the shared contract — see docs/INTERFACES.md):

    # data/chunks/<page-slug>__<chunk-num>.json
    {
        "id":         "running_gpu-pods__003",                       # unique, stable
        "source_url": "https://nrp.ai/documentation/userdocs/running/gpu-pods/",
        "title":      "Running GPU pods",
        "text":       "To request a GPU, add nvidia.com/gpu: 1 ..."
    }

The embed step reads these fields verbatim:
  - id          -> Chroma document id
  - text        -> embedded + stored as the document
  - source_url  -> metadata, surfaced as a citation link
  - title       -> metadata, surfaced as the citation label
Do not rename a field — it's in docs/INTERFACES.md.
------------------------------------------------------------------------------
"""

from __future__ import annotations


def fetch_docs() -> list[dict]:
    """Fetch raw NRP doc pages. Return a list of {url, title, html_or_md}."""
    # TODO(week-05): scrape nrp.ai (or clone the docs repo) and return raw pages.
    raise NotImplementedError("Week 5: implement fetch_docs().")


def clean(raw_page: dict) -> str:
    """Strip nav/menus/HTML cruft from one page; return clean plain text."""
    # TODO(week-05): clean a single page. Watch for "Skip to main content" junk.
    raise NotImplementedError("Week 5: implement clean().")


def chunk(text: str, source_url: str, title: str) -> list[dict]:
    """Split clean text into chunks matching the CHUNK JSON SCHEMA above."""
    # TODO(week-05): split into ~500-token chunks with ~100-token overlap.
    raise NotImplementedError("Week 5: implement chunk().")


def run() -> None:
    """End-to-end pipeline: fetch -> clean -> chunk -> write data/chunks/*.json.

    Called by scripts/ingest.py so the whole thing runs with one command.
    """
    # TODO(week-05): wire fetch_docs -> clean -> chunk and write JSON to data/chunks/.
    raise NotImplementedError("Week 5: implement run().")
