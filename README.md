# 🌾 Kisan Mitra (The Farmer's Friend)

**Kisan Mitra** is an AI-powered, one-stop digital ecosystem designed to empower Indian farmers with data-driven insights. By consolidating crop diagnosis, government scheme navigation, and essential farm resources into a single bilingual platform (Hindi & English), it helps reduce information fragmentation and minimize yield loss.

---

## 🚀 Key Features

### 🩺 AI Crop Doctor & Custom Model Portfolio
A **Multi-Model Routing Architecture** ensures high-precision crop disease detection.

**Custom-Trained Models (TensorFlow/Keras):**
- **Rice:** Bacterial Leaf Blight, Brown Spot, Leaf Smut (224×224)
- **Potato:** Early Blight, Late Blight (256×256)
  
**Gemini Vision Fallback**
- Routes unidentified crops to **Gemini 2.5 Flash Vision API** for instant diagnosis.

**Hyper-Local Treatment Plans**
- Actionable remedies via **Gemini Text API**, tailored to district & state.

---

### 🤖 RAG-Powered Government Scheme Chatbot
- **LangChain**-based Retrieval-Augmented Generation (RAG)
- **FAISS** vector store + **HuggingFace Embeddings**
- Converts official government PDFs into an interactive knowledge base
- Conversational answers in **Hindi & English**

---

### 📊 Farmer’s Dashboard
- **Diagnostic History:** Past scans with disease, symptoms, causes & treatments (PostgreSQL)
- **Localized Weather:** Hyper-local forecasts via **OpenWeatherMap API**
- **Bilingual News Feed:** Real-time agri news (English & Hindi) using **NewsAPI** + Gemini
- **Expert Videos:** Curated YouTube content (e.g., DD Kisan), filtered by disease

---

## 🛠️ Tech Stack

**Backend:** Python, Django REST Framework (DRF), PostgreSQL  
**AI/ML:** TensorFlow, Keras, Google Gemini API, LangChain, FAISS, Sentence-Transformers (all-MiniLM-L6-v2)  
**Frontend:** React.js, Material UI (MUI), i18next

---

## 🧠 LangChain Knowledge Base (RAG)

1. **Document Loading:** `PyPDFDirectoryLoader`
2. **Text Splitting:** `RecursiveCharacterTextSplitter`
3. **Embeddings:** `all-MiniLM-L6-v2`
4. **Vector Store:** FAISS
5. **Retrieval & Generation:** Gemini 2.5 Flash grounded on retrieved context
---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- Node.js & npm
- API Keys: Gemini, OpenWeatherMap, NewsAPI

### Backend
bash
cd backend
python -m venv venv
Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

### Frontend 
cd frontend
npm install
npm start

###DashBoard
![Farmer Dashboard1](pictures/dashboard1.png)
![Farmer Dashboard2](pictures/dashboard2.png)

## 📈 Data Vision

Kisan Mitra is designed as a **self-improving AI ecosystem**.

- Every crop diagnosis stores:
  - Geotagged crop image
  - Crop type
  - Identified disease
- All records are securely saved in **PostgreSQL**
- This continuously growing dataset enables:
  - Retraining of custom ML models
  - Improved accuracy over time
  - India-specific crop intelligence

---

## ❤️ Mission

Our mission is to **empower Indian farmers through technology** by providing:
- Accurate, accessible, and localized agricultural intelligence
- Bilingual support to bridge the digital divide
- AI-driven solutions that reduce crop loss and improve livelihoods

**Built with ❤️ for the Indian Farming Community.**
