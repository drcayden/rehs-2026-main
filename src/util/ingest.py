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
import json
import os
from pathlib import Path
import re

from bs4 import BeautifulSoup
import git
import markdown

from src.mix.config import Config


def fetch_docs() -> int:
    """Fetch raw NRP doc pages. Return a list of {url, title, html_or_md}."""
    try:
        # Clones the repo into the specified directory
        git.Repo.clone_from(Config.REPO_URL, Config.REPO_DIRECTORY)
        return 0
    except git.GitCommandError as e:
        print(f"git error: {e}")
        return 1


def clean(md: str) -> str:
    """Strip nav/menus/HTML cruft from one page; return clean plain text."""
    # Convert markdown to HTML
    html = markdown.markdown(md)
    # Parse HTML and extract plain text
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ")
    # Normalize whitespace (remove double spaces, extra newlines)
    clean_text = re.sub(r"\s+", " ", text).strip()
    return clean_text


def chunk(base_docs_dir) -> list[dict]:
    """Split clean text into chunks matching the CHUNK JSON SCHEMA above."""
    base_path = Path(base_docs_dir)
    chunks = []
    page_num = 1

    target_files = list(base_path.rglob("*.md")) + list(base_path.rglob("*.mdx"))

    # Recursively find all markdown files in the directory
    for file_path in target_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Extract Title
        match = re.search(r"^#\s+(.*)", content, flags=re.MULTILINE)
        if match:
            title = match.group(1).strip()
        else:
            title = file_path.stem.replace("-", " ").title()

        # 2. Generate ID (Lowercase title, spaces to underscores, plus page num)
        safe_title = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")
        doc_id = f"{safe_title}__{page_num:03d}"

        # 3. Generate Source URL
        rel_path = file_path.relative_to(base_path)
        url_path = rel_path.with_suffix("")  # Removes the .md extension
        url_path_str = str(url_path).replace(
            "\\", "/"
        )  # Ensure forward slashes for URLs
        source_url = f"https://nrp.ai/documentation/{url_path_str}/"

        # 4. Clean Text
        clean_text = clean(content)

        # Assemble the JSON object
        chunk = {
            "id": doc_id,
            "source_url": source_url,
            "title": title,
            "text": clean_text,
        }
        chunks.append(chunk)
        page_num += 1

    return chunks


def run() -> None:
    """End-to-end pipeline: fetch -> clean -> chunk -> write data/chunks/*.json.

    Called by scripts/ingest.py so the whole thing runs with one command.
    """
    # fetch repo
    git_result = fetch_docs()
    if git_result != 0:
        print("git fetch failed. try again later.")
        return

    # set up
    if not os.path.exists(Config.DOCS_DIRECTORY):
        print("something went wrong. try again later.")
    else:
        results = chunk(Config.DOCS_DIRECTORY)

        # Write output to JSON
        with open(Config.OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)

        print("done")
