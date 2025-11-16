import os
import google.generativeai as genai
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
# --- THIS IS THE CHANGE ---
from langchain_huggingface import HuggingFaceEmbeddings # Replaced Google with HuggingFace
# --------------------------
from dotenv import load_dotenv
import sys

# Define the paths
PDF_DIR = "knowledge_base/schemes/"
VECTOR_STORE_PATH = "faiss_index_schemes"
# This is a popular, lightweight model that will run locally.
MODEL_NAME = "all-MiniLM-L6-v2" 

def main():
    # 1. Load API Key (still needed for Gemini later, so we check)
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file.")
        sys.exit(1) 
    
    # 2. Load all PDFs
    try:
        loader = PyPDFDirectoryLoader(PDF_DIR)
        documents = loader.load()
        if not documents:
            print(f"No PDF documents found in {PDF_DIR}")
            sys.exit(1)
        print(f"Successfully loaded {len(documents)} document pages.")
    except Exception as e:
        print(f"Error loading PDFs: {e}")
        sys.exit(1)

    # 3. Split the documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    print(f"Split documents into {len(texts)} text chunks.")

    # 4. Create the Embeddings model (Locally)
    try:
        print(f"Loading local embedding model '{MODEL_NAME}'...")
        # --- THIS IS THE CHANGE ---
        # This will download the model (90MB) the first time it runs
        embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
        # --------------------------
        print("Local model loaded successfully.")

    except Exception as e:
        print(f"Error initializing local embeddings model: {e}")
        sys.exit(1)

    # 5. Create and Save the Vector Database (No API calls!)
    try:
        print("Creating vector store... This will use your CPU and may take a few minutes.")
        
        # This now runs 100% locally. No API calls, no rate limits.
        vector_store = FAISS.from_documents(texts, embeddings)
        vector_store.save_local(VECTOR_STORE_PATH)
        
        print("\n" + "="*50)
        print(f" SUCCESS! ")
        print(f" Your knowledge base has been indexed locally and saved to:")
        print(f" {os.path.abspath(VECTOR_STORE_PATH)}")
        print("="*50 + "\n")
        print("You can now run 'process_schemes.py' and start your Django server.")
        
    except Exception as e:
        print(f"\nAn error occurred while creating the vector store: {e}")

if __name__ == "__main__":
    main()