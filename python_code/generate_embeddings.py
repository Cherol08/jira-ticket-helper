# from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from data_collector import fetch_jira_tickets
import faiss
import pickle
import os
from utils import get_config


config = get_config()

def generate_and_store_embeddings(
    df, 
    # text-embedding-3-small
    # text-embedding-3-large
    embedding_model='text-embedding-ada-002', 
    model_path='models/ticket_data.pkl', 
    openai_api_key=config['openai_api_key']
    ):
    
    """Generates embeddings and stores them in FAISS."""
    embeddings = OpenAIEmbeddings(model=embedding_model, openai_api_key=openai_api_key)
    vectors = [embeddings.embed_query(text) for text in df['summary']]
    
    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(vectors)
    
    os.makedirs('models', exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump((df, index), f)

def load_embeddings(model_path='models/ticket_data.pkl'):
    """Load embeddings from file with error handling."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Embeddings file not found: {model_path}")
    
    try:
        with open(model_path, "rb") as f:
            return pickle.load(f)
    except (EOFError, pickle.UnpicklingError):
        raise ValueError(f"Error loading embeddings file: {model_path}. Please regenerate the file.")

print("Fetching Jira tickets...")
df = fetch_jira_tickets()

# Generate embeddings and store them
print("Generating embeddings and saving to 'models/ticket_data.pkl'...")
generate_and_store_embeddings(df, model_path='models/ticket_data.pkl')

print("Embeddings have been successfully generated and stored.")