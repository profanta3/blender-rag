import os
import streamlit as st

from rag_app import RagApp

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

header_col, btn_col = st.columns([4, 1], vertical_alignment="bottom")

header_col.title("Chat now with WikiRAG")
if btn_col.button(":red[Clear History]"):
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if "rag_app" not in st.session_state:
    rag_app = RagApp(os.environ["DB_NAME"], os.environ["OPENAI_BASE_URL"])
    st.session_state["rag_app"] = rag_app
else:
    rag_app = st.session_state["rag_app"]


if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.query = prompt
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream, doc = rag_app.search(st.session_state.query)
        st.session_state.latest_rag = doc.text

        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.query = None
