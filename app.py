"""REHS 2026 NRP chatbot — Streamlit chat shell.

This is the FRONT DOOR of the app. Right now it's a plain chat
UI with no retrieval: you type, it echoes a placeholder. Over Weeks 4-5 you turn
it into a RAG chatbot.

Run it:
    streamlit run app.py

Wiring plan:
  - Week 4: connect this to the NRP LLM so it streams a real chat answer.
  - Week 5: add the retrieval step (call search(), build a grounded prompt, show
            citations under the answer).

The retrieval contract you depend on lives in src/embed/search.py and is documented
in docs/INTERFACES.md.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

from src.embed.search import (
    search,  # the shared contract: search(query, k) -> list[dict]
)
from src.ui.chat import answer_question, build_grounded_messages

st.set_page_config(page_title="NRP Chatbot (REHS 2026)", page_icon="🤖")
st.title("NRP Chatbot")
st.caption("Ask about the National Research Platform. Built by REHS 2026.")

# env openai
load_dotenv()
client = OpenAI(
    api_key=os.environ["NRP_LLM_TOKEN"], base_url=os.environ["NRP_LLM_BASE_URL"]
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Replay history.
for message in st.session_state.messages:
    if message["role"] == "system":
        continue  # don't show
    st.chat_message(message["role"]).write(message["content"])

if prompt := st.chat_input("Ask away..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    result = answer_question(prompt, k=5)
    answer = result.get("answer", "")
    chunks = result.get("chunks", [])

    # append msg
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)

    # show citations
    if chunks:
        with st.expander("📚 Sources"):
            for c in chunks:
                st.markdown(
                    f"- [{c['title']}]({c['source_url']})  *(score: {c['score']:.3f})*"
                )
    else:
        st.info("No docs indexed yet — run the ingest + index pipeline first.")
