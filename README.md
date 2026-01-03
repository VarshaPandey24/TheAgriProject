🌾 Kisan Mitra (The Farmer's Friend)

Kisan Mitra is an AI-powered, one-stop digital ecosystem designed to empower Indian farmers with data-driven insights. By consolidating crop diagnosis, government scheme navigation, and essential farm resources into a single bilingual platform, we aim to eliminate information fragmentation and reduce yield loss.

🚀 Key Features

🩺 AI Crop Doctor & Custom Model Portfolio

The flagship feature uses a Multi-Model Routing Architecture to ensure precision. Based on the selected crop, the backend invokes specialized deep learning models:

Custom-Trained Models (TensorFlow/Keras):

Rice: Detects Bacterial Leaf Blight, Brown Spot, and Leaf Smut (224x224 input).

Wheat: Detects Leaf Rust and Stem Rust (224x224 input).

Potato: Detects Early Blight and Late Blight (256x256 input).

Cotton: Analyzes leaf and plant health (224x224 input).

Sugarcane: Detects Mosaic, Red Rot, Rust, and Yellow Leaf Disease (224x224 input).

Gemini Vision Fallback: Automatically routes "other" or unidentified crops to the Gemini 2.5 Flash Vision API for instant diagnosis.

Hyper-Local Treatment Plans: Generates actionable remedies using Gemini Text API, tailored specifically to the farmer's district and state.

🤖 RAG-Powered Gov Scheme Chatbot

LangChain Integration: A sophisticated Retrieval-Augmented Generation (RAG) pipeline that turns static PDF documents into an interactive knowledge base.

Vector Intelligence: Uses a FAISS vector store and HuggingFace Embeddings to index official government PDFs.

Conversational Hindi/English: Provides personalized answers to complex scheme questions, bypassing dense legal jargon.

📊 Farmer's Dashboard

The Dashboard serves as the command center for the farmer, providing real-time data and historical insights:

Diagnostic History: A detailed log of all past "Crop Doctor" scans, displaying the specific disease identified by the custom models, along with symptoms, causes, and treatment plans saved in PostgreSQL.

Localized Weather: Hyper-local forecasts including rain probability via OpenWeatherMap API.

Bilingual News Feed: Real-time agricultural news in English and Hindi using NewsAPI and Gemini translation.

Expert Videos: Integrated YouTube tutorials from official sources like DD Kisan, filtered by the identified disease.

🛠️ Tech Stack

Backend: Python, Django REST Framework (DRF), PostgreSQL.

AI/ML: TensorFlow, Keras, Google Gemini API, LangChain, FAISS, Sentence-Transformers (all-MiniLM-L6-v2).

Frontend: React.js, Material UI (MUI), i18next (Bilingual support).

🧠 LangChain Knowledge Base Construction

The "brain" of the Government Scheme Chatbot is built using a Retrieval-Augmented Generation (RAG) architecture. Here is how LangChain processes the documents:

Document Loading: Using PyPDFDirectoryLoader, we ingest multiple official PDF documents describing various government schemes.

Text Splitting: Large PDFs are broken down into smaller, overlapping chunks using the RecursiveCharacterTextSplitter.

Embedding Generation: Each text chunk is converted into a high-dimensional numerical vector using all-MiniLM-L6-v2.

Vector Storage: These vectors are stored in a FAISS index for high-speed semantic searches.

Retrieval & Generation: When a farmer asks a question, LangChain retrieves relevant chunks and the Gemini 2.5 Flash model generates a response based strictly on that context.

⚙️ Installation & Setup

1. Prerequisites

Python 3.10+

Node.js & npm

Gemini API Key, OpenWeatherMap API Key, NewsAPI Key.

2. Backend Setup

cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


3. Frontend Setup

cd frontend
npm install
npm start


4. Environment Variables (.env)

Create a .env file in the backend/ directory:

GEMINI_API_KEY=your_key_here
WEATHER_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
SECRET_KEY=your_django_secret
DEBUG=True


📈 The Data Vision

Kisan Mitra is built as a self-improving ecosystem. Every diagnosis—including the geotagged image, crop type, and identified disease—is saved to our PostgreSQL database. This builds a massive, proprietary dataset of Indian crop health, which is used to continuously re-train our ML models, making the system smarter with every interaction.

Developed with ❤️ for the Indian Farming Community.
