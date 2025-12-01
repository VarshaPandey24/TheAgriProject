from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import google.generativeai as genai
import json
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser
from googleapiclient.discovery import build
from .models import CropDiagnosis,GovernmentScheme
from .serializers import UserSerializer, MyTokenObtainPairSerializer, GovernmentSchemeSerializer
from rest_framework import generics, status
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from django.views.decorators.cache import cache_page 
from django.utils.decorators import method_decorator
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import io 
from django.core.cache import cache

MODEL_DIR = os.path.join(settings.BASE_DIR, 'ml_models')
MODEL_CONFIG = {
    'Rice': {
        'path': os.path.join(MODEL_DIR, 'rice_model.h5'),
        'labels': ['Bacterial leaf blight', 'Brown spot', 'Leaf smut', 'Healthy'], 
        'input_shape': (224, 224) 
    },
    'Wheat': {
        'path': os.path.join(MODEL_DIR, 'wheat_model.h5'),
        'labels': ['Leaf Rust', 'Stem Rust', 'Healthy'], 
        'input_shape': (224, 224) 
    },
    'Potato': {
        'path': os.path.join(MODEL_DIR, 'potato_model.h5'),
        'labels': ['Early blight', 'Late blight', 'Healthy'], 
        'input_shape': (224, 224)
    },
    'Cotton': {
        'path': os.path.join(MODEL_DIR, 'cotton_model.h5'),
        'labels': ['diseased cotton leaf', 'diseased cotton plant', 'fresh cotton leaf', 'fresh cotton plant'], 
        'input_shape': (224, 224)
    },
    'Sugarcane': {
        'path': os.path.join(MODEL_DIR, 'sugarcane_model.h5'),
        'labels': ['Mosaic', 'RedRot', 'Rust', 'Yellow', 'Healthy'], 
        'input_shape': (224, 224)
    },
}
CACHE_TTL = 60 * 30

class HelloView(APIView):
    def get(self, request):
        content = {'message': 'Hello from your Django Backend! 👋'}
        return Response(content)

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
            return Response({"error": "City or location coordinates are required."}, status=400)

        api_key = settings.OPENWEATHER_API_KEY
        base_url = "https://api.openweathermap.org/data/2.5/forecast" 

        params = {'appid': api_key, 'units': 'metric'}
        if lat and lon:
            params['lat'] = lat
            params['lon'] = lon
        else:
            params['q'] = city

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if not data.get('list'):
                return Response({"error": "No forecast data found."}, status=404)
            
            current_forecast = data['list'][0]
            pop = current_forecast.get('pop', 0) * 100 

            processed_data = {
                'city': data.get('city', {}).get('name'),
                'temperature': current_forecast.get('main', {}).get('temp'),
                'description': current_forecast.get('weather', [{}])[0].get('description'),
                'main_condition': current_forecast.get('weather', [{}])[0].get('main'),
                'humidity': current_forecast.get('main', {}).get('humidity'),
                'wind_speed': current_forecast.get('wind', {}).get('speed'),
                'chance_of_rain': pop
            }
            return Response(processed_data)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to fetch weather data: {e}"}, status=500)

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

        if not image_file:
            return Response({"error": "No image file provided."}, status=status.HTTP_400_BAD_REQUEST)
        if not all([crop_name, district, state]):
            return Response({"error": "Crop name, district, and state are required."}, status=status.HTTP_400_BAD_REQUEST)

        disease_name = None
        error_message = None

        if crop_name in MODEL_CONFIG:
            model_info = MODEL_CONFIG[crop_name]
            image_file.seek(0)
            disease_name, error_message = predict_with_custom_model(
                model_info['path'],
                image_file,
                model_info['labels'],
                model_info['input_shape']
            )
        elif crop_name == 'Other':
            image_file.seek(0)
            disease_name, error_message = identify_disease_with_gemini_vision(image_file, "Unknown Crop")
        else:
            error_message = f"Invalid crop selected: {crop_name}."
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        if error_message:
            print(f"Error during prediction for {crop_name}: {error_message}")
            return Response({"error": f"Analysis failed: {error_message}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if disease_name is None:
            return Response({"error": "Could not identify disease from image."}, status=status.HTTP_404_NOT_FOUND)
        if "healthy" in disease_name.lower():
            return Response({"message": f"{crop_name} appears healthy!"}, status=status.HTTP_200_OK)

        analysis_data, gemini_error = call_gemini_api(disease_name, district, state, lang_code)
        video_data, youtube_error = call_youtube_api(disease_name, lang_code)
        
        if gemini_error: print(gemini_error); analysis_data = {"error": "Could not fetch detailed analysis."}
        if youtube_error: print(youtube_error); video_data = {"error": "Could not fetch videos."}

        if not gemini_error:
            try:
                image_file.seek(0)
                diagnosis = CropDiagnosis(
                    user=request.user, image=image_file, crop_name=crop_name,
                    disease_name=disease_name, district=district, state=state,
                    symptoms=analysis_data.get('symptoms'),
                    causes=analysis_data.get('causes'), remedies=analysis_data.get('remedies')
                )
                diagnosis.save()
            except Exception as e:
                print(f"Error saving diagnosis to database: {e}")

        final_response = {
            "disease_name": disease_name, "analysis": analysis_data,
            "videos": video_data, "location": f"{district}, {state}"
        }
        return Response(final_response, status=status.HTTP_200_OK)

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
             return None, f"Prediction index out of bounds for labels. Index: {predicted_class_index}, Labels: {len(class_labels)}"

        predicted_label = class_labels[predicted_class_index]
        return predicted_label, None

    except Exception as e:
        return None, f"Error during model prediction: {e}"

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

        prompt = f"Identify the crop and Identify the primary disease visible in this image. Respond with ONLY the most likely disease name (e.g., 'Late blight', 'Leaf Rust') or respond with 'Healthy' if no disease is clearly visible. Do not include any other text or explanation."

        response = model.generate_content([prompt, image_part])
        disease_name = response.text.strip()

        if not disease_name or len(disease_name) > 100:
            return None, "Received invalid response from vision model."

        return disease_name, None
    except Exception as e:
        return None, f"Gemini Vision API error: {e}"


def call_gemini_api(disease_name, district, state, lang_code='en'):
    cache_key = f'gemini_analysis:{disease_name}:{district}:{lang_code}'
    analysis = cache.get(cache_key)
    if analysis:
        print("--- CACHE HIT: Returning fast analysis for Gemini ---")
        return analysis, None
    """Sends the disease name and location to Gemini and returns a detailed analysis."""
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-flash-latest')
        
        target_language = "Hindi" if lang_code == 'hi' else "simple English"
        
        prompt = f"""
        You are an agricultural expert named Kisan Mitra.
        A farmer has identified a crop disease: "{disease_name}".
        The farmer is located in: {district}, {state}, India.

        Provide a detailed, easy-to-understand analysis in {target_language}.
        **Please prioritize remedies (chemical and organic) that are suitable and available
        for the farmer's specific location ({district}, {state}).**
        
        Your response must be ONLY a valid JSON object, with no other text or markdown.
        The JSON object must have these exact keys: "symptoms", "causes", "remedies".
        
        - "symptoms": A list of key visual symptoms (in {target_language}).
        - "causes": A list of common causes (in {target_language}).
        - "remedies": A list of actionable remedies (in {target_language}).
        """
        
        response = model.generate_content(prompt)
        cleaned_text = response.text.strip().lstrip('```json').rstrip('```').strip()
        analysis_json = json.loads(cleaned_text)
        return analysis_json, None
    except Exception as e:
        return None, f"Gemini API error: {e}"  

def call_youtube_api(disease_name, lang_code='en'):
    """Searches YouTube for DD Kisan videos related to the disease."""
    try:
        youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
        
        hindi_search = "upchar" if lang_code == 'hi' else "treatment"
        query = f"{disease_name} {hindi_search}" 

        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=5,
            relevanceLanguage=lang_code,
        )
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
        return None, f"YouTube API error: {e}"
SCHEME_CACHE_TTL = 31536000
   
@method_decorator(cache_page(SCHEME_CACHE_TTL), name='get')
class GovernmentSchemeListView(generics.ListAPIView):
    
    queryset = GovernmentScheme.objects.all().order_by('-last_updated')
    serializer_class = GovernmentSchemeSerializer
    permission_classes = [AllowAny]

try:
    CHAT_LLM = ChatGoogleGenerativeAI(model="models/gemini-flash-latest", temperature=0.3)
    CHAT_EMBEDDINGS = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    CHAT_VECTOR_STORE = FAISS.load_local(
        "faiss_index_schemes", 
        CHAT_EMBEDDINGS, 
        allow_dangerous_deserialization=True
    )
    CHAT_RETRIEVER = CHAT_VECTOR_STORE.as_retriever(search_kwargs={"k": 3}) 

    CHAT_PROMPT_TEMPLATE = """
    You are "Kisan Mitra," an expert AI assistant for Indian farmers. 
    Answer the user's question clearly and politely in simple Hindi.
    You MUST use the following retrieved context to form your answer.
    You MUST take the user's personal profile into account.
    If the context doesn't contain the answer, politely say in Hindi that you do not have that specific information.

    **Retrieved Context:**
    {context}

    **User's Profile:**
    - User's State: {state}
    - User's District: {district}

    **User's Question:**
    {input}

    **Answer (in Hindi):**
    """

    CHAT_PROMPT = ChatPromptTemplate.from_template(CHAT_PROMPT_TEMPLATE)
    document_chain = create_stuff_documents_chain(CHAT_LLM, CHAT_PROMPT)
    RAG_CHAIN = create_retrieval_chain(CHAT_RETRIEVER, document_chain)
    print("--- Live Chatbot RAG Chain loaded successfully. ---")

except Exception as e:
    print(f"--- CRITICAL ERROR loading RAG chain: {e} ---")
    RAG_CHAIN = None

class SchemeChatView(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request, *args, **kwargs):
        if not RAG_CHAIN:
            return Response({"error": "Chatbot is not initialized. Please check server logs."}, 
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

        query = request.data.get('query')
        if not query:
            return Response({"error": "No query provided."}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        last_diagnosis = CropDiagnosis.objects.filter(user=user).order_by('-created_at').first()

        user_state = "Unknown"
        user_district = "Unknown"
        if last_diagnosis:
            user_state = last_diagnosis.state
            user_district = last_diagnosis.district

        try:
            response = RAG_CHAIN.invoke({
                "input": query,
                "state": user_state,
                "district": user_district
            })
            answer = response.get("answer", "माफ़ कीजिये, मुझे इसका जवाब नहीं मिला।")
            return Response({"answer": answer}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error during RAG chain invocation: {e}")
            return Response({"error": "An error occurred while processing your request."}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)