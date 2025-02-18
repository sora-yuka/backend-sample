from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Profile(models.Model):
    owner = models.OneToOneField(to=User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, blank=True)
    pfp = models.ImageField(upload_to=f"pfp/", blank=True)
            
    def __str__(self) -> str:
        return f"{self.username} | {self.owner}"