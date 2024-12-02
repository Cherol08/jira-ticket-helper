from langchain.embeddings import HuggingFaceEmbeddings
from data_collector import fetch_jira_tickets
import faiss
import pickle
import os
import numpy as np
from utils import get_config

def generate_and_store_embeddings(
    df, 
    embedding_model='sentence-transformers/all-mpnet-base-v2', 
    model_path='models/ticket_data.pkl'
    ):
    
    """Generates embeddings and stores them in FAISS."""
    # Instantiate HuggingFaceEmbeddings with the specified model
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
    
    # Generate embeddings for each text in the DataFrame's 'summary' column
    vectors = embeddings.embed_documents(df['comments'].tolist())
    vectors = np.array(vectors, dtype="float32")
    
    # Create a FAISS index and add the embeddings
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    
    # Ensure the 'models' directory exists
    os.makedirs('models', exist_ok=True)
    
    # Save the DataFrame and FAISS index to a file
    with open(model_path, "wb") as f:
        pickle.dump((df, index), f)

def load_embeddings(model_path='models/ticket_data.pkl'):
    """Load embeddings from file with error handling."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Embeddings file not found: {model_path}")
    
    try:
        with open(model_path, "rb") as f:
            df, index = pickle.load(f)
            return df, index
    except (EOFError, pickle.UnpicklingError):
        raise ValueError(f"Error loading embeddings file: {model_path}. Please regenerate the file.")




print("Fetching Jira tickets...")
df = fetch_jira_tickets()

# Generate embeddings and store them
print("Generating embeddings and saving to 'models/ticket_data.pkl'...")
generate_and_store_embeddings(df)

print("Embeddings have been successfully generated and stored.")
