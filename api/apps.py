from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'


class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend' 

    def ready(self):
        """
        This function runs once when the server starts.
        """
     
        from . import model_loader 
        model_loader.load_all_models()
