from tensorflow.keras.models import load_model
from django.conf import settings
import os

# This dictionary will hold your loaded models
MODELS = {}

def load_all_models():
    """
    Loads all 5 models into the global MODELS dictionary.
    This function is called only once when the server starts.
    """
    print("Loading ML models...")
    
    # This points to your 'ml_models' folder at the project root
    base_dir = os.path.join(settings.BASE_DIR, 'ml_models')
    
    # Define your model names and filenames
    model_files = {
        'potato': 'potato_model.h5',
        'rice': 'rice_model.h5',
        'wheat': 'wheat_model.h5',
        'cotton': 'cotton_model.h5',
        'sugarcane': 'sugarcane_model.h5',
    }

    # Loop and load each model
    for crop_name, file_name in model_files.items():
        path = os.path.join(base_dir, file_name)
        try:
            # Load the model and store it in the MODELS dictionary
            MODELS[crop_name] = load_model(path)
            print(f"Successfully loaded model for: {crop_name}")
        except Exception as e:
            # This will tell you if a model fails to load
            print(f"Error loading model {crop_name} from {path}: {e}")
    
    print("All models loaded.")