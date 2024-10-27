import streamlit as st

from ui.rag_app import RagApp


rag_app: RagApp = st.session_state["rag_app"]

st.title("Settings")
with st.form("my_form"):
    base_url = st.text_input("OpenAI URL", rag_app.get_openai_base_url())

    model_name = st.selectbox(
        "Model", [m.id for m in rag_app.get_available_models().data]
    )

    submitted = st.form_submit_button("Save")
    if submitted:
        rag_app.set_openai_base_url(base_url)
        rag_app.set_model(model_name)
        st.toast("Settings saved!")
