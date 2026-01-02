import os
import io
import json
import requests
import numpy as np
from PIL import Image

# Django & DRF
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.views import TokenObtainPairView

# TensorFlow & Keras (CPU Optimized)
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# LangChain & AI
from google import genai
from googleapiclient.discovery import build
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Local Imports
from .models import CropDiagnosis, GovernmentScheme
from .serializers import UserSerializer, MyTokenObtainPairSerializer, GovernmentSchemeSerializer

# --- Configuration & Global State ---
MODEL_DIR = os.path.join(settings.BASE_DIR, 'ml_models')
MODEL_CONFIG = {
    'Rice': {'path': os.path.join(MODEL_DIR, 'rice_model.h5'), 'labels': ['Bacterial leaf blight', 'Brown spot', 'Leaf smut', 'Healthy'], 'input_shape': (224, 224)},
    'Potato': {'path': os.path.join(MODEL_DIR, 'potato_model.h5'), 'labels': ['Early blight', 'Late blight', 'Healthy'], 'input_shape': (224, 224)},
   'input_shape': (224, 224)},
}
CACHE_TTL = 60 * 30
_LOADED_MODELS = {} # Singleton pattern for Keras models
_RAG_CHAIN = None   # Singleton pattern for LangChain

# --- Lazy Loading Helpers ---

def get_rag_chain():
    """Initializes the RAG chain only when the first chat request arrives."""
    global _RAG_CHAIN
    if _RAG_CHAIN is None:
        try:
            print("--- Loading RAG Chain & Embeddings... ---")
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=settings.GEMINI_API_KEY)
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            
            vector_store = FAISS.load_local(
                "faiss_index_schemes", 
                embeddings, 
                allow_dangerous_deserialization=True
            )
            retriever = vector_store.as_retriever(search_kwargs={"k": 3})
            
            prompt = ChatPromptTemplate.from_template("""
                You are "Kisan Mitra," an expert AI assistant for Indian farmers. 
                Answer in simple Hindi using the context.
                Context: {context}
                User Profile: {state}, {district}
                Question: {input}
                Answer (Hindi):
            """)
            
            doc_chain = create_stuff_documents_chain(llm, prompt)
            _RAG_CHAIN = create_retrieval_chain(retriever, doc_chain)
            print("--- RAG Chain loaded successfully! ---")
        except Exception as e:
            print(f"--- CRITICAL: RAG failed to load: {e} ---")
    return _RAG_CHAIN

def predict_crop_disease(crop_name, image_file):
    """Loads specific model on-demand and returns prediction."""
    global _LOADED_MODELS
    config = MODEL_CONFIG.get(crop_name)
    if not config: return None, "Unsupported crop"

    try:
        if crop_name not in _LOADED_MODELS:
            if not os.path.exists(config['path']):
                return None, f"Model file missing for {crop_name}"
            _LOADED_MODELS[crop_name] = load_model(config['path'])
        
        model = _LOADED_MODELS[crop_name]
        img = Image.open(image_file).convert('RGB').resize(config['input_shape'])
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        preds = model.predict(img_array)
        label = config['labels'][np.argmax(preds[0])]
        return label, None
    except Exception as e:
        return None, f"Prediction error: {str(e)}"

# --- Views ---

class HelloView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({'message': 'Kisan Mitra Backend Online! 👋'})

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class WeatherView(APIView):
    permission_classes = [AllowAny]
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        lat, lon, city = request.query_params.get('lat'), request.query_params.get('lon'), request.query_params.get('city')
        if not (lat and lon or city): return Response({"error": "Location required"}, 400)
        
        params = {'appid': settings.OPENWEATHER_API_KEY, 'units': 'metric'}
        if lat: params.update({'lat': lat, 'lon': lon})
        else: params['q'] = city

        try:
            res = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)
            res.raise_for_status()
            data = res.json()
            return Response({
                'city': data.get('name'),
                'temp': data['main']['temp'],
                'desc': data['weather'][0]['description'],
                'humidity': data['main']['humidity']
            })
        except Exception as e:
            return Response({"error": str(e)}, 500)

class CropHealthView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        image_file = request.data.get('image')
        crop_name = request.data.get('crop_name')
        
        if not image_file or not crop_name:
            return Response({"error": "Image and crop name required"}, 400)

        # Handle prediction
        if crop_name in MODEL_CONFIG:
            disease_name, err = predict_crop_disease(crop_name, image_file)
        elif crop_name == 'Other':
            disease_name, err = self.identify_with_gemini_vision(image_file)
        else:
            return Response({"error": "Invalid crop selection"}, 400)

        if err: return Response({"error": err}, 500)
        if "healthy" in disease_name.lower():
            return Response({"disease_name": disease_name, "is_healthy": True})

        # Get AI treatment and YouTube tutorials
        analysis, _ = call_gemini_api(disease_name, request.data.get('district'), request.data.get('state'), request.data.get('lang', 'en'))
        videos, _ = call_youtube_api(disease_name, request.data.get('lang', 'en'))

        # Save diagnosis
        CropDiagnosis.objects.create(
            user=request.user, crop_name=crop_name, disease_name=disease_name,
            district=request.data.get('district'), state=request.data.get('state'),
            symptoms=analysis.get('symptoms'), remedies=analysis.get('remedies')
        )

        return Response({"disease_name": disease_name, "analysis": analysis, "videos": videos})

    def identify_with_gemini_vision(self, image_file):
        try:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            img = Image.open(image_file)
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=["Identify the disease in this crop image. Return only the name.", img]
            )
            return response.text.strip(), None
        except Exception as e:
            return None, str(e)

class SchemeChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        query = request.data.get('query')
        if not query: return Response({"error": "No query"}, 400)

        chain = get_rag_chain()
        if not chain: return Response({"error": "Chatbot offline"}, 503)

        diag = CropDiagnosis.objects.filter(user=request.user).order_by('-created_at').first()
        
        try:
            res = chain.invoke({
                "input": query, 
                "state": diag.state if diag else "India", 
                "district": diag.district if diag else "General"
            })
            return Response({"answer": res.get("answer")})
        except Exception as e:
            return Response({"error": str(e)}, 500)

# --- External API Helpers ---

def call_gemini_api(disease, district, state, lang='en'):
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        prompt = f"Explain symptoms, causes, and remedies for {disease} in {district}, {state}. Language: {lang}. Return JSON with keys: symptoms, causes, remedies."
        response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
        # Clean potential markdown from response
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json), None
    except Exception as e:
        return {"error": "AI unavailable"}, str(e)

def call_youtube_api(disease, lang='en'):
    try:
        youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
        query = f"{disease} agricultural treatment {lang}"
        req = youtube.search().list(q=query, part="snippet", type="video", maxResults=3)
        res = req.execute()
        videos = [{"title": i['snippet']['title'], "id": i['id']['videoId']} for i in res.get('items', [])]
        return videos, None
    except:
        return [], "YouTube error"

class GovernmentSchemeListView(generics.ListAPIView):
    queryset = GovernmentScheme.objects.all().order_by('-last_updated')
    serializer_class = GovernmentSchemeSerializer
    permission_classes = [AllowAny]
