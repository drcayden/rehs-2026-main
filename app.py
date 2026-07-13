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

from src.embed.search import search  # the shared contract: search(query, k) -> list[dict]

st.set_page_config(page_title="NRP Chatbot (REHS 2026)", page_icon="🤖")
st.title("NRP Chatbot")
st.caption("Ask about the National Research Platform. Built by REHS 2026.")

# TODO(week-04): load env (.env) and build the OpenAI client pointed at NRP_LLM_BASE_URL.
# from dotenv import load_dotenv; load_dotenv()
# client = OpenAI(api_key=os.environ["NRP_LLM_TOKEN"], base_url=os.environ["NRP_LLM_BASE_URL"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Replay history.
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

if prompt := st.chat_input("Ask about NRP..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # TODO(week-05): retrieve relevant docs.
    #   with st.spinner("Searching NRP docs..."):
    #       chunks = search(prompt, k=5)
    chunks = search(prompt, k=5)  # returns [] until retrieval is implemented

    # TODO(week-05): build a grounded prompt that wraps the retrieved chunks, then
    # call the NRP LLM (stream the answer like Week 4). For now, echo a placeholder.
    answer = (
        "RAG isn't wired up yet — this is the starter shell. "
        "TODO(week-05): build the grounded prompt and call the LLM here. "
        f"(retrieved {len(chunks)} chunk(s))"
    )
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)

    # TODO(week-05): show citations from the retrieved chunks.
    if chunks:
        with st.expander("📚 Sources"):
            for c in chunks:
                st.markdown(
                    f"- [{c['title']}]({c['source_url']})  *(score: {c['score']:.3f})*"
                )
    else:
        st.info("No docs indexed yet — run the ingest + index pipeline first.")
