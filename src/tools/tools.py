from datetime import datetime
import subprocess

from openai.types.chat import ChatCompletionToolParam

from src.config.config import Config


def multiply(a, b):
    return a * b


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def run_kubectl(args):
    # kubectl args
    parts = args.split()
    if parts[0] not in Config.ALLOWED:
        return f"Refused: only read-only verbs {sorted(Config.ALLOWED)} are allowed."
    cmd = ["kubectl", *parts, "-n", Config.NAMESPACE]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    return (out.stdout or out.stderr or "(no output)")[:3000]


tools: list[ChatCompletionToolParam] = [
    {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "Multiply two numbers exactly.",
            "parameters": {
                "type": "object",
                "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current time.",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_kubectl",
            "description": "Run a READ-ONLY kubectl command (get/describe/logs/top) in the REHS namespace and return its output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "args": {
                        "type": "string",
                        "description": "kubectl subcommand, e.g. 'get pods' or 'get deployments'",
                    }
                },
                "required": ["args"],
            },
        },
    },
]

registry = {
    "multiply": multiply,
    "get_current_time": get_current_time,
    "run_kubectl": run_kubectl,
}
