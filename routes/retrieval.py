import os
import streamlit as st

from models import model

from utils import pca
import pandas as pd
import plotly.express as px

st.title("Latest retrieval result")


rag_app = st.session_state["rag_app"]

query = st.chat_input("Perform a DB search") or st.session_state.get("query")

if query:
    st.session_state.query = query
    results = rag_app.db_search(query, limit=500)
    st.session_state["latest_rag"] = results[0].text
    st.session_state["retrieval_results"] = results


def write_latest_query():
    if "query" in st.session_state:
        with st.chat_message("user"):
            st.write(st.session_state.query)


tab1, prompt_tab, tab2 = st.tabs(["Retrieved Document", "Generated Prompt", "PCA plot"])

if "latest_rag" in st.session_state:
    with tab1:
        write_latest_query()
        st.code(st.session_state.latest_rag, language="markdown")
else:
    with tab1:
        st.markdown("Please enter a query below to see the retrieval results.")


def plot_pca():
    st.write(
        ":red[Red Dots] are stored db embeddings, the :blue[blue dot] is the used doc for text gen. And :white[white dot] is the input query."
    )
    vectors = [result.vector for result in st.session_state.retrieval_results]

    query_emb = model.generate_embeddings([query])
    pca_data = pca(query_emb + vectors, 3)

    # Create a DataFrame for the PCA data
    df = pd.DataFrame(pca_data, columns=["PC1", "PC2", "PC3"])

    # Add a column for color
    df["color"] = ["#FF0000"] + ["#FFFFFF"] + ["#0000FF"] * (len(df) - 2)
    df["size"] = [5] + [5] + [1] * (len(df) - 2)
    df["text"] = ["Query"] + ["Used Doc"] + [""] * (len(df) - 2)

    fig = px.scatter_3d(
        df, x="PC1", y="PC2", z="PC3", color="color", size="size", text="text"
    )
    st.plotly_chart(fig, use_container_width=True)


# add pca plot for 10 search results
if "retrieval_results" in st.session_state and query:
    with tab2:
        write_latest_query()
        plot_pca()
else:
    with tab2:
        st.markdown("Please enter a query below to see the PCA plot.")
        # button for using latest query
        if "query" in st.session_state:
            st.write("Or use latest query as input:")
            if st.button(f'"{st.session_state.query}"'):
                query = st.session_state.query
                plot_pca()


with prompt_tab:
    prompt = rag_app.get_latest_prompt()
    if prompt:
        write_latest_query()
        st.code(rag_app.get_latest_prompt(), language="markdown")
    else:
        st.write("No prompt available - please enter a query to generate a prompt.")
