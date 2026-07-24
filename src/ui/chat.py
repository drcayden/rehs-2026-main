import streamlit as st


from src.ai.chat import saving_stream


def show_history():
    # Replay history.
    for msg in st.session_state.messages:
        # 1. Skip system, tool, or empty meta-messages safely
        if msg["role"] == "system":
            continue
        if msg["role"] == "tool" and not st.session_state.get("show_tools", False):
            continue

        # 2. Only render if there is actual content to write
        if msg.get("content"):
            with st.chat_message(msg["role"]):
                # Write the main message content
                st.markdown(msg["content"])

                # 3. INTEGRATION: Render sources if this message has them
                chunks = msg.get("chunks")
                if chunks:
                    with st.expander("📚 Sources"):
                        for c in chunks:
                            # Safely get the score in case it's missing
                            score = c.get("score", 0.0)
                            st.markdown(
                                f"- [{c['title']}]({c['source_url']}) *(score: {score:.3f})*"
                            )


def show_input():
    if prompt := st.chat_input("Ask away..."):
        # init vars
        meta = {}

        # 1. Render user prompt immediately in UI
        st.chat_message("user").write(prompt)

        # 3. Swap the nesting: chat_message MUST be the outer block
        with st.chat_message("assistant"):
            st.write_stream(saving_stream(prompt=prompt, meta=meta))

        # rerun to show chunks
        st.rerun()
