# api/scripts/process_schemes.py
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- THIS IS THE FIX ---
# We are changing the import paths to the new, correct locations.
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
# ---------------------

# Import your Django models
# This requires the script to be run with 'manage.py runscript'
from api.models import GovernmentScheme
import sys
import time

# --- CONFIGURATION ---
PDF_DIR = "knowledge_base/schemes/"
VECTOR_STORE_PATH = "faiss_index_schemes"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "models/gemini-flash-latest"

def run():
    print("--- [START] Processing Government Schemes ---")

    # --- 1. Load API Key and Models (Stays the same) ---
    print("Loading API key and models...")
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file.")
        sys.exit(1)
    
    genai.configure(api_key=api_key)
    
    try:
        llm = ChatGoogleGenerativeAI(model=LLM_MODEL, google_api_key=api_key, temperature=0.2)
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        vector_store = FAISS.load_local(
            VECTOR_STORE_PATH, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
        retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        
    except Exception as e:
        print(f"Error loading models or vector store: {e}")
        sys.exit(1)
        
    print("Models and vector store loaded successfully.")

    # --- 2. DEFINE YOUR NEW RAG PROMPT ---
    extraction_prompt = ChatPromptTemplate.from_template(
        """
        You are an expert at reading government documents for farmers.
        Based on the following context, extract the information.
        
        CONTEXT:
        {context}
        
        Based *only* on the context, provide the following in simple English:
        1.  **title**: The official name of the scheme.
        2.  **summary**: A very simple, one-sentence summary explaining what the scheme is.
        3.  **details**: A list of bullet points (as a JSON list of strings) explaining the key benefits and features.
        4.  **eligibility**: A list of bullet points (as a JSON list of strings) explaining who is eligible to apply.
        5.  **apply_link**: The *full* official URL (starting with http or https) for the application or for more information. If no link is found, return an empty string "".
        
        Respond ONLY with a valid JSON object in the following format:
        {{
            "title": "...",
            "summary": "...",
            "details": ["Bullet point 1", "Bullet point 2"],
            "eligibility": ["Eligibility 1", "Eligibility 2"],
            "apply_link": "..."
        }}
        """
    )
    # -------------------------------------

    # Create the RAG chain (Stays the same)
    document_chain = create_stuff_documents_chain(llm, extraction_prompt)
    rag_chain = create_retrieval_chain(retriever, document_chain)
    print("RAG extraction pipeline initialized.")

    # --- 3. Process Each PDF (Stays the same) ---
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
    print(f"Found {len(pdf_files)} PDF files to process.")

    for pdf_filename in pdf_files:
        file_path = os.path.join(PDF_DIR, pdf_filename)
        
        if GovernmentScheme.objects.filter(source_url=file_path).exists():
            print(f"Skipping '{pdf_filename}' (already in database).")
            continue
        
        print(f"Processing new file: '{pdf_filename}'...")
        
        try:
            query = f"Extract the title, summary, details, eligibility, and apply_link from the document {pdf_filename}"
            response = rag_chain.invoke({"input": query})
            answer_json = response.get("answer", "{}")
            cleaned_json_str = answer_json.strip().lstrip('```json').rstrip('```').strip()
            
            if not cleaned_json_str or cleaned_json_str == "{}":
                print(f"  ...Failed: RAG chain returned an empty answer for '{pdf_filename}'.")
                continue

            data = json.loads(cleaned_json_str)
            
            # --- 4. SAVE TO NEW DATABASE FIELDS ---
            GovernmentScheme.objects.create(
                title=data.get("title", f"Unnamed Scheme - {pdf_filename}"),
                summary=data.get("summary", "No summary available."),
                details=data.get("details", []), # Save as JSON list
                eligibility=data.get("eligibility", []), # Save as JSON list
                apply_link=data.get("apply_link", ""), # Save the link
                source_url=file_path
            )
            print(f"  ...Success! Saved '{data.get('title')}' to the database.")
            time.sleep(5) # Delay to avoid rate limits
            
        except json.JSONDecodeError:
            print(f"  ...Failed: Could not decode JSON response from LLM for '{pdf_filename}'.")
            print(f"  ...Response was: {cleaned_json_str}")
        except Exception as e:
            print(f"  ...Failed: An unexpected error occurred for '{pdf_filename}': {e}")
            time.sleep(10)

    print("\n--- [END] Scheme processing complete. ---")