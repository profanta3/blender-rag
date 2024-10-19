import streamlit as st

retrieval_page = st.Page("routes/retrieval.py", title="Retrieval", icon="🔍")
prompt_page = st.Page("routes/prompt.py", title="Prompt", icon="📃")
chat_page = st.Page("routes/chat.py", title="Chat", icon="🤖")

pg = st.navigation([chat_page, retrieval_page, prompt_page])
pg.run()
