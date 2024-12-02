import streamlit as st
from generate_embeddings import load_embeddings
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from utils import get_config
from data_collector import fetch_jira_tickets

# Load embeddings
df, index = load_embeddings()
config = get_config()
st.sidebar.write(f"Connected to Jira Project: {config['project_key']}")

def query_similar_tickets(query, df, index, embedding_model='text-embedding-ada-002'):
    embeddings = OpenAIEmbeddings(model=embedding_model)
    query_vector = embeddings.embed_text(query)
    distances, indices = index.search([query_vector], k=5)
    results = df.iloc[indices[0]]
    return results

st.title("Jira Ticket Helper with LLM")
st.write("Query historic tickets or find resolutions for new issues.")

query = st.text_input("Describe your issue:")
if st.button("Search"):
    if query:
        results = query_similar_tickets(query, df, index)
        st.write("### Similar Tickets:")
        for _, row in results.iterrows():
            st.write(f"**{row['key']}**: {row['summary']}")
            st.write(f"- Status: {row['status']}")
            st.write(f"- Created: {row['created']}")
            st.write("---")
    else:
        st.warning("Please enter a query.")
