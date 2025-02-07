from typing import Dict, Any, Optional
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Profile

# Create your tests here.

User = get_user_model()


class ProfileTest(APITestCase):
    base_url = "http://localhost:8000/api/v1/profile/"
    file_path = "./media/default/default-user.jpg"
    
    @property
    def example_bearer_token(self) -> Dict[str, str]:
        """ 
        Getting example bearer token
        """
        user = User.objects.create(
            email="gobfe@evasem.ga",
            password="pExjKAmgself",
        )
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}
    
    def get_upload_photo(self) -> SimpleUploadedFile:
        with open(file=self.file_path, mode="rb") as file:
            return SimpleUploadedFile(
                name="default-user.jpg",
                content=file.read(),
                content_type="image/jpg",
            )
    
    def test_retrieve_profile(self) -> None:
        response = self.client.get(path=self.base_url, data=None, format="json", **self.example_bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get().email, "gobfe@evasem.ga")
        
    def test_update_profile(self) -> None:
        url = self.base_url + "update/"
        data = {"username": "Inez", "pfp": self.get_upload_photo()}
        response = self.client.patch(path=url, data=data, format="multipart", **self.example_bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Profile.objects.get().username)
        
    def tearDown(self):
        import os
        try:
            profile = Profile.objects.get()
            if profile.pfp:
                image_path = profile.pfp.path
                if os.path.exists(image_path):
                    os.remove(image_path)
        except Profile.DoesNotExist:
            pass
        except Exception as e:
            print(f"Error deleting image: {e}")
        finally:
            super().tearDown()