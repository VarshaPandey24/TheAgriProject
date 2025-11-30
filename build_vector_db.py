import os
import google.generativeai as genai
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings 
from dotenv import load_dotenv
import sys

PDF_DIR = "knowledge_base/schemes/"
VECTOR_STORE_PATH = "faiss_index_schemes"
MODEL_NAME = "all-MiniLM-L6-v2" 

def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file.")
        sys.exit(1) 

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

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    print(f"Split documents into {len(texts)} text chunks.")

    try:
        print(f"Loading local embedding model '{MODEL_NAME}'...")
        embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
        print("Local model loaded successfully.")

    except Exception as e:
        print(f"Error initializing local embeddings model: {e}")
        sys.exit(1)
    try:
        print("Creating vector store... This will use your CPU and may take a few minutes.")
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