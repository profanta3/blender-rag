import os
import streamlit as st

from rag_app import RagApp


st.title("Chat now with PDFrag")
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if "latest_rag" in st.session_state:
    with st.sidebar:
        st.title("Retreival results")
        st.write(st.session_state.latest_rag)

if "rag_app" not in st.session_state:
    rag_app = RagApp(os.environ["DB_NAME"], "http://localhost:5000/v1")
    st.session_state["rag_app"] = rag_app
else:
    rag_app = st.session_state["rag_app"]

# Accept user input
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
        with st.sidebar:
            st.title("Retrieval results")
            st.write(st.session_state.latest_rag)
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.query = None
