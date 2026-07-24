import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
from src.mix.config import Config


@st.cache_resource
def get_openai_client() -> OpenAI:
    """Cached across all users/reruns."""
    load_dotenv()
    return OpenAI(api_key=os.getenv("NRP_LLM_TOKEN"), base_url=Config.NRP_URL)
