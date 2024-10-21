import os
import streamlit as st

from rag_app import RagApp

st.title("Edit Prompt template")


rag_app = st.session_state["rag_app"]
with st.form("my_form"):
    txt = st.text_area(
        label="Prompt Template",
        value=st.session_state["rag_app"].prompt.template,
        height=400,
        label_visibility="collapsed",
    )

    submitted = st.form_submit_button("Save")
    if submitted:
        st.session_state["rag_app"].prompt.template = txt
        st.toast("Prompt saved!")
