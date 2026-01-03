import os
import json
import requests
import numpy as np
import io
from PIL import Image

# Django & DRF Imports
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

# Internal Project Imports
from .models import CropDiagnosis, GovernmentScheme
from .serializers import UserSerializer, MyTokenObtainPairSerializer, GovernmentSchemeSerializer

import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"
# ML & AI Imports
import tf_keras as keras
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import google.generativeai as genai
from googleapiclient.discovery import build

# LangChain Imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# --- Configuration ---
MODEL_DIR = os.path.join(settings.BASE_DIR, 'ml_models')
MODEL_CONFIG = {
    'Rice': {
        'path': os.path.join(MODEL_DIR, 'rice_model.h5'),
        'labels': ['Bacterial leaf blight', 'Brown spot', 'Leaf smut', 'Healthy'],
        'input_shape': (224, 224)
    },
    'Potato': {
        'path': os.path.join(MODEL_DIR, 'potato_model.h5'),
        'labels': ['Early blight', 'Late blight', 'Healthy'],
        'input_shape': (224, 224)
    },
  
}
CACHE_TTL = 60 * 30
SCHEME_CACHE_TTL = 31536000

# --- Helper Functions ---

def predict_with_custom_model(model_path, image_file, class_labels, input_shape):
    """Loads a Keras model, preprocesses image, predicts, and returns label."""
    try:
        if not os.path.exists(model_path):
            return None, f"Model file not found at {model_path}"

        model = load_model(model_path)
        img_height, img_width = input_shape

        img = Image.open(image_file).convert('RGB')
        img = img.resize((img_width, img_height))

        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions[0])

        if predicted_class_index >= len(class_labels):
            return None, "Prediction index out of bounds."

        return class_labels[predicted_class_index], None
    except Exception as e:
        return None, str(e)

def identify_disease_with_gemini_vision(image_file, crop_name):
    """Uses Gemini multimodal model to identify disease from image."""
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-flash-latest')
        image_bytes = image_file.read()
        image_part = {
            "mime_type": image_file.content_type,
            "data": image_bytes
        }

        prompt = "Identify the crop and primary disease in this image. Respond with ONLY the disease name or 'Healthy'."
        response = model.generate_content([prompt, image_part])
        return response.text.strip(), None
    except Exception as e:
        return None, str(e)

def call_gemini_api(disease_name, district, state, lang_code='en'):
    cache_key = f'gemini_analysis:{disease_name}:{district}:{lang_code}'
    analysis = cache.get(cache_key)
    if analysis:
        return analysis, None

    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-flash-latest')
        target_language = "Hindi" if lang_code == 'hi' else "simple English"
        
        prompt = f"""
        You are an agricultural expert named Kisan Mitra. Disease: {disease_name}. Location: {district}, {state}.
        Provide JSON only: {{"symptoms": [], "causes": [], "remedies": []}} in {target_language}.
        """
        response = model.generate_content(prompt)
        cleaned_text = response.text.strip().lstrip('```json').rstrip('```').strip()
        analysis_json = json.loads(cleaned_text)
        cache.set(cache_key, analysis_json, CACHE_TTL)
        return analysis_json, None
    except Exception as e:
        return None, str(e)

def call_youtube_api(disease_name, lang_code='en'):
    try:
        youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
        query = f"{disease_name} treatment"
        request = youtube.search().list(part="snippet", q=query, type="video", maxResults=5)
        response = request.execute()
        
        videos = []
        for item in response.get('items', []):
            videos.append({
                "title": item['snippet']['title'],
                "videoId": item['id']['videoId'],
                "thumbnailUrl": item['snippet']['thumbnails']['default']['url']
            })
        return videos, None
    except Exception as e:
        return None, str(e)

# --- API Views ---

class HelloView(APIView):
    def get(self, request):
        return Response({'message': 'Hello from your Django Backend! 👋'})

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@method_decorator(cache_page(CACHE_TTL), name='get')
class WeatherView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        city = request.query_params.get('city')

        if not (lat and lon or city):
            return Response({"error": "City or coordinates required."}, status=400)

        params = {'appid': settings.OPENWEATHER_API_KEY, 'units': 'metric'}
        if lat and lon:
            params['lat'], params['lon'] = lat, lon
        else:
            params['q'] = city

        try:
            response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=params)
            response.raise_for_status()
            data = response.json()
            current = data['list'][0]
            return Response({
                'city': data.get('city', {}).get('name'),
                'temperature': current.get('main', {}).get('temp'),
                'description': current.get('weather', [{}])[0].get('description'),
                'humidity': current.get('main', {}).get('humidity'),
                'chance_of_rain': current.get('pop', 0) * 100
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)

@method_decorator(cache_page(CACHE_TTL), name='get')
class NewsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        api_key = settings.NEWS_API_KEY
        base_url = "https://newsapi.org/v2/everything"
    
        page = request.query_params.get('page', 1)
        lang_code = request.query_params.get('lang', 'en') 
        
        params = {
            'apiKey': api_key,
            'q': '"agriculture" AND "India"', 
            'sortBy': 'publishedAt',
            'language': 'en', 
            'pageSize': 10, 
            'page': page
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            news_data = response.json()
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to fetch news data: {e}"}, status=500)
        
        if lang_code != 'en' and news_data.get('articles'):
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel('models/gemini-flash-latest') 

                texts_to_translate = []
                for article in news_data['articles']:
                    texts_to_translate.append({
                        "title": article['title'], 
                        "description": article.get('description', '')
                    })

                target_language = "Hindi" if lang_code == 'hi' else lang_code
                prompt = f"""
                Translate the 'title' and 'description' of each JSON object in the following list into {target_language}.
                Do not translate proper nouns or names.
                Return ONLY a valid JSON list in the exact same format as the input.
                Do not add any other text, markdown, or explanations.

                Input:
                {json.dumps(texts_to_translate, ensure_ascii=False)}

                Translated Output:
                """

                translation_response = model.generate_content(prompt)
                cleaned_response_text = translation_response.text.strip().lstrip('```json').rstrip('```').strip()
                translated_articles = json.loads(cleaned_response_text)

                for i, article in enumerate(news_data['articles']):
                    if i < len(translated_articles):
                        article['title'] = translated_articles[i]['title']
                        article['description'] = translated_articles[i]['description']
            
            except Exception as e:
                print(f"Gemini bundled translation failed: {e}")
        
        return Response(news_data)
    
class CropHealthView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        image_file = request.data.get('image')
        crop_name = request.data.get('crop_name')
        district = request.data.get('district')
        state = request.data.get('state')
        lang_code = request.data.get('lang', 'en')

        if not image_file or not all([crop_name, district, state]):
            return Response({"error": "Missing required fields."}, status=400)

        if crop_name in MODEL_CONFIG:
            cfg = MODEL_CONFIG[crop_name]
            disease, err = predict_with_custom_model(cfg['path'], image_file, cfg['labels'], cfg['input_shape'])
        elif crop_name == 'Other':
            disease, err = identify_disease_with_gemini_vision(image_file, "Other")
        else:
            return Response({"error": "Invalid crop selection."}, status=400)

        if err: return Response({"error": err}, status=500)
        if "healthy" in disease.lower(): return Response({"message": f"{crop_name} is healthy!"})

        analysis, g_err = call_gemini_api(disease, district, state, lang_code)
        videos, y_err = call_youtube_api(disease, lang_code)

        diagnosis = CropDiagnosis(
            user=request.user, image=image_file, crop_name=crop_name,
            disease_name=disease, district=district, state=state,
            symptoms=analysis.get('symptoms'), causes=analysis.get('causes'), remedies=analysis.get('remedies')
        )
        diagnosis.save()

        return Response({
            "disease_name": disease,
            "analysis": analysis,
            "videos": videos,
            "location": f"{district}, {state}"
        })

@method_decorator(cache_page(SCHEME_CACHE_TTL), name='get')
class GovernmentSchemeListView(generics.ListAPIView):
    queryset = GovernmentScheme.objects.all().order_by('-last_updated')
    serializer_class = GovernmentSchemeSerializer
    permission_classes = [AllowAny]

# --- RAG / Chatbot Initialization ---
try:
    CHAT_LLM = ChatGoogleGenerativeAI(model="models/gemini-flash-latest", temperature=0.3)
    CHAT_EMBEDDINGS = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    CHAT_VECTOR_STORE = FAISS.load_local("faiss_index_schemes", CHAT_EMBEDDINGS, allow_dangerous_deserialization=True)
    
    CHAT_PROMPT = ChatPromptTemplate.from_template("""
    You are "Kisan Mitra". Answer in simple Hindi using the context.
    Context: {context}
    User Location: {district}, {state}
    Question: {input}
    """)
    
    doc_chain = create_stuff_documents_chain(CHAT_LLM, CHAT_PROMPT)
    RAG_CHAIN = create_retrieval_chain(CHAT_VECTOR_STORE.as_retriever(search_kwargs={"k": 3}), doc_chain)
except Exception as e:
    print(f"RAG Error: {e}")
    RAG_CHAIN = None

class SchemeChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not RAG_CHAIN: return Response({"error": "Service unavailable"}, status=503)
        query = request.data.get('query')
        if not query: return Response({"error": "No query"}, status=400)

        user = request.user
        last_diag = CropDiagnosis.objects.filter(user=user).order_by('-created_at').first()
        state = last_diag.state if last_diag else "Unknown"
        dist = last_diag.district if last_diag else "Unknown"

        try:
            response = RAG_CHAIN.invoke({"input": query, "state": state, "district": dist})
            return Response({"answer": response.get("answer", "माफ़ कीजिये, जानकारी नहीं मिली।")})
        except Exception as e:
            return Response({"error": str(e)}, status=500)