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

import streamlit as st

from src.ui.chat import show_history, show_input
from src.ui.sidebar import show_sidebar
from src.mix.state import init_state

st.set_page_config(page_title="NRP Chatbot (REHS 2026)", page_icon="🤖")

# session state
init_state()

# show stuff
show_sidebar()
show_history()
show_input()
