from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'


class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend' 

    # ADD THIS 'ready' METHOD
    def ready(self):
        """
        This function runs once when the server starts.
        """
        # We must import here to avoid issues
        from . import model_loader 
        
        # Call your loading function
        model_loader.load_all_models()
