import os
import streamlit as st

from rag_app import RagApp


rag_app: RagApp = st.session_state["rag_app"]

st.title("Settings")

if base_url := st.text_input("OpenAI URL", rag_app.get_openai_base_url()):
    rag_app.set_openai_base_url(base_url)

    st.toast(f"URL successfully set to {base_url}")

if model_name := st.selectbox(
    "Model", [m.id for m in rag_app.get_available_models().data], key="model_name"
):
    rag_app.set_model(model_name)
    st.toast(f"Model set to {model_name}")
