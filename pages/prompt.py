import os
import streamlit as st

from rag_app import RagApp

st.title("Edit Prompt template")

if "rag_app" not in st.session_state:
    rag_app = RagApp(os.environ["DB_NAME"], os.environ["OPENAI_BASE_URL"])
    st.session_state["rag_app"] = rag_app
else:
    rag_app = st.session_state["rag_app"]

txt = st.text_area(
    label="Prompt Template",
    value=st.session_state["rag_app"].prompt.template,
    height=400,
)

if txt and txt != st.session_state["rag_app"].prompt.template:
    st.session_state["rag_app"].prompt.template = txt
    st.toast("Prompt saved!")
