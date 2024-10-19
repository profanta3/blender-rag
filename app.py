import streamlit as st

retrieval_page = st.Page("pages/retrieval.py", title="Retrieval", icon="🔍")
prompt_page = st.Page("pages/prompt.py", title="Prompt", icon="📃")
chat_page = st.Page("pages/chat.py", title="Chat", icon="🤖")

pg = st.navigation([chat_page, retrieval_page, prompt_page])
pg.run()
