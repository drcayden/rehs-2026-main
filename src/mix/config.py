class Config:
    # src/ui/chat.py
    DEFAULT_MODEL = "gpt-oss"
    MAX_ROUNDS = 2000
    DEFAULT_TOKENS = 200000
    THINK_STARTED = "Thinking"
    THINK_COMPLETED = " Done\n\n"
    TOOL_USED = "\nExecuting tools (please be patient)\n\n"

    # src/embed/search.py
    EMBEDDING_MODEL = "qwen3-embedding"

    # src/sesion/manager.py
    NRP_URL = "https://ellm.nrp-nautilus.io/v1"
    DEFAULT_MESSAGES = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that answers questions about the "
                "National Research Platform (NRP). You have access to the NRP "
                "documentation and can provide citations for your answers."
            ),
        },
        {
            "role": "assistant",
            "content": ("Hey! How can I help?"),
        },
    ]
    AVAILABLE_MODELS = ["gemma", "gpt-oss", "qwen3-small"]
    DEFAULT_TEMPERATURE = 0.7

    # src/tools/tools.py
    ALLOWED = {"get", "describe", "logs", "top"}
    NAMESPACE = "rehs-2026-chatbot"

    # src/ingest/ingest.py
    REPO_URL = "https://gitlab.nrp-nautilus.io/prp/nrp-site"
    REPO_DIRECTORY = "./.temp/nrp-site"
    DOCS_DIRECTORY = "./.temp/nrp-site/src/content/docs/Documentation"
    OUTPUT_FILE = "./data/chunks/chunks.json"
