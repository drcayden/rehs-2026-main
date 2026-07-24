import base64
import secrets

import streamlit as st

from src.mix.config import Config


def init_state():
    # session vars
    if "cache_salt" not in st.session_state:
        st.session_state.cache_salt = base64.b64encode(secrets.token_bytes(32)).decode()
    if "messages" not in st.session_state:
        st.session_state.messages = Config.DEFAULT_MESSAGES
    if "model" not in st.session_state:
        st.session_state.model = Config.DEFAULT_MODEL
    if "max_tokens" not in st.session_state:
        st.session_state.max_tokens = Config.DEFAULT_TOKENS
    if "temperature" not in st.session_state:
        st.session_state.temperature = Config.DEFAULT_TEMPERATURE
