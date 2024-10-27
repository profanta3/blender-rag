import streamlit as st

from ui.rag_app import RagApp

st.title("Edit Prompt template")


rag_app = st.session_state["rag_app"]


template_tab, gen_tab = st.tabs(["Prompt Template", "Generated Prompt"])


def write_latest_query():
    if "query" in st.session_state:
        with st.chat_message("user"):
            st.write(st.session_state.query)


with template_tab:
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

with gen_tab:
    prompt = rag_app.get_latest_prompt()
    if prompt:
        write_latest_query()
        st.code(rag_app.get_latest_prompt(), language="markdown")
    else:
        st.write("No prompt available - please enter a query to generate a prompt.")
