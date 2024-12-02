import streamlit as st
from generate_embeddings import load_embeddings
from langchain.embeddings import HuggingFaceEmbeddings
from utils import get_config
from data_collector import fetch_jira_tickets
import numpy as np
import re

# Load embeddings
df, index = load_embeddings()
config = get_config()
st.sidebar.write(f"Connected to Jira Project: {config['project_key']}")

def query_similar_tickets(query, df, index, embedding_model='sentence-transformers/all-mpnet-base-v2', threshold=0.9):
    """Query similar tickets using Hugging Face embeddings."""
    # Instantiate HuggingFaceEmbeddings with the specified model
    
    
    ticket_pattern = r'\b\d{4}\b'
    match = re.search(ticket_pattern, query)
    
    if match:
        # If a ticket number is found, retrieve the ticket's details
        ticket_number = match.group(0)
        print(ticket_number)
        matching_ticket = df[df['key'] == f"TTSD-{ticket_number}"]
        print(matching_ticket)

        if matching_ticket.empty:
            return None, f"No ticket found with the number: {ticket_number}"
        
        # Generate embedding for the matching ticket's summary
        embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        ticket_summary = matching_ticket.iloc[0]['comments']
        query_vector = embeddings.embed_query(ticket_summary)
    else:
        # If no ticket number is found, treat the entire query as the text for similarity search
        embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        query_vector = embeddings.embed_query(query)
    
    # Convert query vector to NumPy array for FAISS
    query_vector = np.array([query_vector], dtype='float32')
    
    # Perform similarity search
    distances, indices = index.search(query_vector, k=10)
    similarities = 1 - distances
    # Filter results based on the similarity threshold
    filtered_results = [
        (sim, idx) for sim, idx in zip(similarities[0], indices[0]) if sim >= threshold
    ]
    
    # Retrieve matching rows from the DataFrame
    if filtered_results:
        results = df.iloc[[idx for _, idx in filtered_results]]
        return results
    else:
        return None

st.title("Jira Ticket Helper with LLM")
st.write("Query historic tickets or find resolutions for new issues.")

query = st.text_input("Enter ticket number...")
if st.button("Search"):
    if query:
        # Query similar tickets
        results = query_similar_tickets(query, df, index)
        st.write("### Similar Tickets:")
        for _, row in results.iterrows():
            st.write(f"**{row['key']}**: {row['summary']}")
            st.write(f"- Status: {row['status']}")
            st.write(f"- Created: {row['created']}")
            st.write(f"- Assignee: {row['assignee']}")
            st.write(f"- Comments: {row['comments']}")
            st.write("---")
    else:
        st.warning("Please enter a query.")
