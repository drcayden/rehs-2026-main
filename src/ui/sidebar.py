import streamlit as st

from src.mix.config import Config
from src.ai.chat import reset_chat


def show_sidebar():
    # remove the forehead of the sidebar
    st.markdown(
        """
    <style>
    [data-testid="stSidebarHeader"] {
        display: none;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.title("NRP Chatbot")
        st.caption("Ask about the National Research Platform. Built by REHS 2026.")
        st.button("New Chat", on_click=reset_chat)
        st.session_state.llm_model = st.selectbox(
            "Model",
            Config.AVAILABLE_MODELS,
            index=Config.AVAILABLE_MODELS.index(Config.DEFAULT_MODEL)
            if Config.DEFAULT_MODEL in Config.AVAILABLE_MODELS
            else 0,
        )
        st.session_state.temperature = st.slider(
            "Temperature", 0.0, 1.5, Config.DEFAULT_TEMPERATURE
        )
