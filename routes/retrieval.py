import os
import streamlit as st

from models import model
from rag_app import RagApp
from utils import pca
import pandas as pd


st.title("Latest retrieval result")

if "rag_app" not in st.session_state:
    rag_app = RagApp(os.environ["DB_NAME"], os.environ["OPENAI_BASE_URL"])
    st.session_state["rag_app"] = rag_app
else:
    rag_app = st.session_state["rag_app"]


if query := st.chat_input("Perform a DB search"):
    results = rag_app.db_search(query, limit=500)
    st.session_state["latest_rag"] = results[0].text
    st.session_state["retrieval_results"] = results

tab1, tab2 = st.tabs(["Retrieved Text", "PCA plot"])

if "latest_rag" in st.session_state:
    with tab1:
        st.markdown(st.session_state.latest_rag)

# add pca plot for 10 search results
if "retrieval_results" in st.session_state:
    with tab2:
        st.write(
            ":red[Red Dots] are stored db embeddings, the :blue[blue dot] is the used doc for text gen. And :white[white dot] is the input query."
        )
        vectors = [result.vector for result in st.session_state.retrieval_results]

        query_emb = model.generate_embeddings([query])
        pca_data = pca(query_emb + vectors)

        # Create a DataFrame for the PCA data
        df = pd.DataFrame(pca_data, columns=["PC1", "PC2"])

        # Add a column for color
        df["color"] = ["#FF0000"] + ["#FFFFFF"] + ["#0000FF"] * (len(df) - 2)

        # Plot the scatter chart
        st.scatter_chart(df, x="PC1", y="PC2", color="color", use_container_width=True)
else:
    with tab2:
        st.markdown("Please enter a query below to see the PCA plot.")
