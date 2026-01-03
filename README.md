# 🌾 Kisan Mitra (The Farmer's Friend)

**Kisan Mitra** is an AI-powered, one-stop digital ecosystem designed to empower Indian farmers with data-driven insights. By consolidating crop diagnosis, government scheme navigation, and essential farm resources into a single bilingual platform (Hindi & English), it helps reduce information fragmentation and minimize yield loss.

---

## 🚀 Key Features

### 🩺 AI Crop Doctor & Custom Model Portfolio
A **Multi-Model Routing Architecture** ensures high-precision crop disease detection.

**Custom-Trained Models (TensorFlow/Keras):**
- **Rice:** Bacterial Leaf Blight, Brown Spot, Leaf Smut (224×224)
- **Wheat:** Leaf Rust, Stem Rust (224×224)
- **Potato:** Early Blight, Late Blight (256×256)
- **Cotton:** Leaf & plant health analysis (224×224)
- **Sugarcane:** Mosaic, Red Rot, Rust, Yellow Leaf Disease (224×224)

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
