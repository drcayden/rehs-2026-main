# rehs-nrp-chatbot

The starter skeleton for the **REHS 2026** project: a Retrieval-Augmented Generation
(RAG) chatbot grounded in [National Research Platform (NRP)](https://nrp.ai) docs,
deployed onto the Nautilus Kubernetes cluster.

This repo is **a skeleton, not a solution.** Every file that imports and runs is here
so Day 1 works — but the real implementation is left to you, marked with
`# TODO(week-0X): ...` comments. You write the interesting parts. We wrote the wiring.

---

## What you build over 8 weeks

A question goes in. The bot retrieves the most relevant NRP doc passages, hands them
to an LLM, and answers — with citations. Then you ship it to a public URL.

```
docs ──► ingest ──► chunks ──► embed ──► Chroma
                                           │
                                  search() │
                                           ▼
user ──► UI ──► prompt ──► NRP LLM ──► answer + citations
                                           │
                                 deploy    ▼   Kubernetes
```

**Your pair builds ALL of this** — the whole vertical. (In Week 7 the cohort merges the
best pieces of every pair's bot into one team product.)

---

## Quick start (Day 1)

```bash
git clone https://github.com/sdsc-rehs/rehs-nrp-chatbot.git
cd rehs-nrp-chatbot

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # then paste your token from https://nrp.ai/llmtoken
streamlit run app.py               # opens the (not-yet-wired) chat shell
```

On Day 1 the app runs but doesn't answer from docs yet — that's the whole point of
the next eight weeks.

---

## Repo layout

```
app.py                  Streamlit chat shell (wire RAG in here)
requirements.txt        Pinned dependencies — bump deliberately
.env.example            Copy to .env; never commit .env
src/
  ingest/ingest.py      scrape + clean + chunk NRP docs  -> data/chunks/*.json
  embed/search.py       index chunks in Chroma; expose search(query, k)
  ui/chat.py            answer_question() — the RAG core eval.py imports
scripts/
  ingest.py             Thin runner: python scripts/ingest.py
  eval.py               Week 6 eval harness (reads eval/questions.jsonl)
eval/
  questions.jsonl       Week 6 eval set (3 EXAMPLE rows — replace with your own)
docs/
  INTERFACES.md         THE shared interfaces. Read this Monday of Week 5.
deploy/
  Dockerfile            python:3.12-slim image
  README.md             build/run instructions + common errors
  k8s/                  Kubernetes manifests (Week 7)
```

---

## Week-by-week TODO map

| Week | You do | Files you touch |
|---|---|---|
| 1 | Onboard, clone, first LLM API call | `.env` |
| 2-3 | Learn Python/git/LLM basics, prompt engineering | scratch files |
| 4 | First Streamlit chat app (no RAG yet) | `app.py` |
| 5 | **Your pair builds its OWN full RAG bot.** Agree shared interfaces Monday. | `src/ingest/ingest.py`, `src/embed/search.py`, `src/ui/chat.py`, `app.py` |
| 6 | Improve it + evaluate + the bake-off | `scripts/eval.py`, `eval/questions.jsonl` |
| 7 | Merge the best bots, then deploy to NRP | `deploy/k8s/*.yaml` |
| 8 | Polish, open-source PR, present | everything |

The authoritative contracts between modules live in
[`docs/INTERFACES.md`](docs/INTERFACES.md). When in doubt, that file wins.

---

## Ground rules

- **Never commit `.env` or real tokens.** `.gitignore` already excludes them. If you
  ever push one, rotate it immediately at https://nrp.ai/llmtoken.
- **Hold the contracts in `docs/INTERFACES.md`.** Every pair's bot uses the same interfaces
  so the best pieces can be merged into one team bot in Week 7. Break a field and your piece
  can't be merged.
- Read what AI tools write for you. Boilerplate is fair game; understanding is not optional.

## License

MIT — see [LICENSE](LICENSE).
