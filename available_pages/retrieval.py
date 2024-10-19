import os
import streamlit as st

from rag_app import RagApp

st.title("Latest retrieval result")

if "rag_app" not in st.session_state:
    rag_app = RagApp(os.environ["DB_NAME"], os.environ["OPENAI_BASE_URL"])
    st.session_state["rag_app"] = rag_app
else:
    rag_app = st.session_state["rag_app"]

if "latest_rag" in st.session_state:
    st.markdown(st.session_state.latest_rag)

if query := st.chat_input("Perform a DB search"):
    result = rag_app.db_search_single(query)
    st.session_state.latest_rag = result.text
