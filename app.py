import os
import streamlit as st

from rag_app import RagApp


if "rag_app" not in st.session_state:
    rag_app = RagApp(os.environ["DB_NAME"], os.environ["OPENAI_BASE_URL"])
    st.session_state["rag_app"] = rag_app
else:
    rag_app = st.session_state["rag_app"]

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# https://discuss.streamlit.io/t/how-to-right-justify-st-chat-message/46794/5
st.markdown(
    """
<style>
    .st-emotion-cache-janbn0 {
        flex-direction: row-reverse;
        text-align: right;
    }
</style>
""",
    unsafe_allow_html=True,
)

retrieval_page = st.Page("routes/retrieval.py", title="Retrieval", icon="🔍")
prompt_page = st.Page("routes/prompt.py", title="Prompt", icon="📃")
chat_page = st.Page("routes/chat.py", title="Chat", icon="🤖")
settings_page = st.Page("routes/settings.py", title="Settings", icon="⚙️")

pg = st.navigation([chat_page, retrieval_page, prompt_page, settings_page])
pg.run()
