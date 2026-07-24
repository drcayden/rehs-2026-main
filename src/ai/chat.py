"""UI — RAG orchestration: retrieve, ground, generate.

Factored out of the Streamlit ``app.py`` so the Week 6 eval harness
(``scripts/eval.py``) can import ``answer_question`` and score it WITHOUT
spinning up a UI. Keeping it here is a CONTRACT — see docs/INTERFACES.md.
You may instead keep this logic inline in app.py; if so, mirror this exact
signature so eval.py's import still resolves.

Implementation plan (Week 5):
  1. ``search(question, k)`` for the most relevant chunks (the shared contract).
  2. Build grounded chat messages: system prompt + numbered docs + question.
  3. Call the NRP ``gpt-oss`` chat model with those messages.
  4. Return BOTH the answer text and the chunks used, so the UI can render
     citations and eval.py can check which sources were retrieved.
"""

from __future__ import annotations
import json
from typing import Any
import streamlit as st

from src.ai.client import get_openai_client
from src.mix.config import Config
from src.ai.search import search
from src.ai.tools import registry, tools


def reset_chat():
    st.session_state.messages = None


def build_grounded_messages(question: str, chunks: list[dict]) -> None:
    """Builds a list of messages that ground the question in the retrieved chunks.

    CONTRACT (see docs/INTERFACES.md) — each message dict MUST have exactly:
        {
            "role":    str,  # "system" or "user"
            "content": str,  # the message text
        }

    Reference implementation shape (Week 5):
        system_msg = {"role": "system", "content": SYSTEM_PROMPT}
        numbered_docs = "\n\n".join(
            f"[{i+1}] {c['title']} ({c['source_url']}):\n{c['text']}"
            for i, c in enumerate(chunks)
        )
        user_msg = {
            "role": "user",
            "content": f"{numbered_docs}\n\nQuestion: {question}\nAnswer:"
        }
        return [system_msg, user_msg]
    """
    # build message
    context = "\n\n---\n\n".join(f"[Source: {c['title']}]\n{c['text']}" for c in chunks)
    grounded = f"""
Use the NRP documentation below to answer. If the docs don't contain the answer, say so honestly. Use your tools whenever possible. For testing purposes only you may also answer multiplication questions.
DEFAULT NAMESPACE: {Config.NAMESPACE}
DOCS:
{context}
QUESTION: {question}
    """
    # append message
    st.session_state.messages.append({"role": "system", "content": grounded})


def saving_stream(prompt: str, k: int = 5, meta: dict | None = None):
    """Streams the answer text chunk by chunk in real time while handling tool calls."""
    # 2. Mutate UI state BEFORE the stream starts!
    st.session_state.messages.append({"role": "user", "content": prompt})

    if meta is None:
        meta = {}

    chunks = search(prompt, k=k)
    meta["chunks"] = chunks
    build_grounded_messages(prompt, chunks)

    # get client
    client = get_openai_client()

    for _ in range(Config.MAX_ROUNDS):
        stream = client.chat.completions.create(
            model=st.session_state.llm_model,
            messages=st.session_state.messages,
            tools=tools,
            stream=True,
            extra_body={"cache_salt": st.session_state.cache_salt},
        )

        turn_content = ""
        tool_calls_buffer = {}

        for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta

            # 1. Yield text content tokens instantly in real time
            if delta.content:
                turn_content += delta.content
                yield delta.content

            # 2. Accumulate streaming tool call deltas (if any)
            if delta.tool_calls:
                for tc_delta in delta.tool_calls:
                    idx = tc_delta.index
                    if idx not in tool_calls_buffer:
                        tool_calls_buffer[idx] = {
                            "id": "",
                            "type": "function",
                            "function": {"name": "", "arguments": ""},
                        }
                    if tc_delta.id:
                        tool_calls_buffer[idx]["id"] += tc_delta.id
                    if tc_delta.function and tc_delta.function.name:
                        tool_calls_buffer[idx]["function"]["name"] += (
                            tc_delta.function.name
                        )
                    if tc_delta.function and tc_delta.function.arguments:
                        tool_calls_buffer[idx]["function"]["arguments"] += (
                            tc_delta.function.arguments
                        )

        # Save assistant text chunk to context if present
        assistant_msg: dict[str, Any] = {"role": "assistant"}

        # add chunks
        assistant_msg["chunks"] = chunks

        if turn_content:
            assistant_msg["content"] = turn_content

        # Handle tool calls if the model invoked tools
        if tool_calls_buffer:
            formatted_tool_calls = list(tool_calls_buffer.values())
            assistant_msg["tool_calls"] = formatted_tool_calls
            st.session_state.messages.append(assistant_msg)

            for call in formatted_tool_calls:
                fn = registry[call["function"]["name"]]
                args = json.loads(call["function"]["arguments"])
                result = fn(**args)
                st.session_state.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call["id"],
                        "content": str(result),
                    }
                )
        else:
            # If no tool calls occurred, message turn is final
            if turn_content:
                st.session_state.messages.append(assistant_msg)
            break
