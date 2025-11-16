from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer 
from .models import CropDiagnosis,GovernmentScheme

# This is your original UserSerializer for registration
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# This is the new serializer you just added
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        
        return token
    
class GovernmentSchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernmentScheme
        # Add the new fields
        fields = ['id', 'title', 'summary', 'details', 'eligibility', 'apply_link', 'last_updated']