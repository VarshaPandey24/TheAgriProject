from django.db import models
from django.contrib.auth.models import User

class CropDiagnosis(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='crop_images/')
    crop_name = models.CharField(max_length=100)
    disease_name = models.CharField(max_length=255)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    symptoms = models.JSONField(null=True, blank=True)
    causes = models.JSONField(null=True, blank=True)
    remedies = models.JSONField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop_name} - {self.disease_name} ({self.user.username})"

class GovernmentScheme(models.Model):
    title = models.CharField(max_length=255, unique=True)
    summary = models.CharField(max_length=1000, blank=True) 
    details = models.JSONField(null=True, blank=True) 
    eligibility = models.JSONField(null=True, blank=True)
    apply_link = models.URLField(max_length=500, blank=True)
    source_url = models.CharField(max_length=500, unique=True)   
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title