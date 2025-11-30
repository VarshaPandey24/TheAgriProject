from tensorflow.keras.models import load_model
from django.conf import settings
import os

MODELS = {}

def load_all_models():
    """
    Loads all 5 models into the global MODELS dictionary.
    This function is called only once when the server starts.
    """
    print("Loading ML models...")
    
    base_dir = os.path.join(settings.BASE_DIR, 'ml_models')
    
    model_files = {
        'potato': 'potato_model.h5',
        'rice': 'rice_model.h5',
    }

    for crop_name, file_name in model_files.items():
        path = os.path.join(base_dir, file_name)
        try:
            MODELS[crop_name] = load_model(path)
            print(f"Successfully loaded model for: {crop_name}")
        except Exception as e:
            print(f"Error loading model {crop_name} from {path}: {e}")
    
    print("All models loaded.")