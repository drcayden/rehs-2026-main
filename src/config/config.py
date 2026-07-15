class Config:
    # A private class variable (starts with underscores)
    THINK_STARTED = "Thinking"
    THINK_COMPLETED = " Done\n\n"
    TOOL_USED = "\nExecuting tools (please be patient)\n\n"
    KUBE_ALLOWEDCMD = {"get", "describe", "logs", "top"},
    KUBE_NAMESPACE = "rehs-2026-chatbot"
    