import os
import streamlit as st
from models import Document

from rag_app import RagApp


header_col, btn_col = st.columns([4, 1], vertical_alignment="bottom")

if st.session_state.messages:
    if btn_col.button(":red[Clear History]"):
        st.session_state.messages = []


@st.dialog("Search results", width="large")
def show_search_results(doc_list: list[Document]):
    st.dataframe([d.model_dump(exclude="vector") for d in doc_list])


rag_app = st.session_state["rag_app"]


# Display chat messages from history on app rerun
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "docs" in message:
            st.divider()
            if st.button("Search results", key=f"btn:{idx}"):
                show_search_results(message["docs"])


header_col.title("Chat now with WikiRAG", help=f"Model: {rag_app.get_model()}")


if prompt := st.chat_input("Ask me something about blender..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.query = prompt
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream, docs = rag_app.search(st.session_state.query)
        st.session_state.latest_rag = docs

        response = st.write_stream(stream)
        st.divider()
        if st.button("Search results"):
            show_search_results(docs)
    st.session_state.messages.append(
        {"role": "assistant", "content": response, "docs": docs}
    )
