# Shared Interfaces — the contracts that make the Week 7 merge possible

> Agreed by the **whole cohort on Monday of Week 5**. Every pair's bot uses these exact
> interfaces, so in Week 7 we can drop the best ingest, the best retrieval, and the best UI —
> from different pairs — into one team bot without rewriting anything. If your code and this file
> disagree, fix one of them. Break a field and your piece can't be merged.

There are exactly three contracts: the **chunk JSON schema** (ingest → embed), the
**`search()` signature** (embed → UI + eval), and the **environment variables**
(everyone → the cluster).

---

## 1. Chunk JSON schema  (ingest produces, embed consumes)

Your ingest step writes one JSON file per chunk to `data/chunks/`:

```
data/chunks/<page-slug>__<chunk-num>.json
```

Each file is a single JSON object with exactly these fields:

```json
{
  "id": "running_gpu-pods__003",
  "source_url": "https://nrp.ai/documentation/userdocs/running/gpu-pods/",
  "title": "Running GPU pods",
  "text": "To request a GPU, add nvidia.com/gpu: 1 to the resources section..."
}
```

| Field | Type | Meaning | Used by embed as |
|---|---|---|---|
| `id` | string | unique, stable id (re-runnable without dup errors) | Chroma document id |
| `source_url` | string | original nrp.ai page | citation link + Chroma metadata |
| `title` | string | page title | citation label + Chroma metadata |
| `text` | string | the chunk's clean text | the embedded document |

Optional (Week 7+): `"ingested_at": "2026-07-21T14:32:00Z"` freshness metadata.
Extra fields are allowed but ignored unless both pairs agree to use them.

---

## 2. `search()` signature  (embed exposes, UI + eval consume)

Lives in `src/embed/search.py`. Import it as:

```python
from src.embed.search import search
```

```python
def search(query: str, k: int = 5) -> list[dict]:
    ...
```

Returns a list of at most `k` dicts, each with **exactly** these keys:

| Key | Type | Meaning |
|---|---|---|
| `text` | str | the chunk text |
| `source_url` | str | original nrp.ai page (for citation) |
| `title` | str | page title (for citation) |
| `score` | float | distance / similarity from Chroma |

Example:

```python
[
  {
    "text": "To request a GPU, add nvidia.com/gpu: 1 ...",
    "source_url": "https://nrp.ai/documentation/userdocs/running/gpu-pods/",
    "title": "Running GPU pods",
    "score": 0.182
  },
  ...
]
```

**Empty-collection rule (required Week 7):** if the Chroma collection is empty or
missing, `search()` returns `[]` — it must NOT raise. The UI renders a friendly
"no docs indexed yet" message on an empty result.

---

## 3. Environment variables  (everyone sets; wired into the cluster in Week 7)

The app reads these from the environment (locally via `.env`; in the cluster via a
ConfigMap + a Secret). See `.env.example`.

| Variable | Source | Example | Notes |
|---|---|---|---|
| `NRP_LLM_TOKEN` | **Secret** | `sk-...` | from https://nrp.ai/llmtoken — never commit it |
| `NRP_LLM_BASE_URL` | ConfigMap | `https://ellm.nrp-nautilus.io/v1` | OpenAI-compatible base URL |
| `LLM_MODEL` | ConfigMap | `gpt-oss` | chat/generation model |
| `EMBEDDING_MODEL` | ConfigMap | `qwen3-embedding` | must match index + query time |

In Kubernetes (Week 7): the three non-secret vars come from `chatbot-config`
(ConfigMap), and `NRP_LLM_TOKEN` comes from the `chatbot-llm-token` Secret. The
deployment loads both via `envFrom`. See `deploy/k8s/`.
