from django.urls import path

from .views import RegisterView,WeatherView,NewsView,CropHealthView,CropHealthView,GovernmentSchemeListView,SchemeChatView



urlpatterns = [  
    path('register/', RegisterView.as_view(), name='register'), 
    path('weather/', WeatherView.as_view(), name='weather'),
    path('news/', NewsView.as_view(), name='news'),
    path('crop-health/', CropHealthView.as_view(), name='crop_health'),
    path('schemes/',GovernmentSchemeListView.as_view(),name='scheme_list'),
    path('chat/', SchemeChatView.as_view(), name='chat'),
]