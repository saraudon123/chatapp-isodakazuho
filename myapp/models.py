from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    img = models.ImageField(upload_to='media_local/', default="static/default_profile_img.jpg")

class Talk(models.Model):
    message = models.CharField(max_length=100)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = "senddesu")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = "receivedesu")
    time = models.DateTimeField(auto_now_add=True)