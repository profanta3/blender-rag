import os
import streamlit as st

from rag_app import RagApp

st.title("Edit Prompt template")


rag_app = st.session_state["rag_app"]

txt = st.text_area(
    label="Prompt Template",
    value=st.session_state["rag_app"].prompt.template,
    height=400,
)

if txt and txt != st.session_state["rag_app"].prompt.template:
    st.session_state["rag_app"].prompt.template = txt
    st.toast("Prompt saved!")
