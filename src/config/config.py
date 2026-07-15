class Config:
    NRP_LLM_BASE_URL = "https://ellm.nrp-nautilus.io/v1"
    LLM_MODEL = "gpt-oss"
    EMBEDDING_MODEL = "qwen3-embedding"

    # src/ui/chat.py
    MAX_ROUNDS = 20

    # src/tools/tools.py
    ALLOWED = {"get", "describe", "logs", "top"}
    NAMESPACE = "rehs-2026-chatbot"
