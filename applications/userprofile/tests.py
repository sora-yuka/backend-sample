from typing import Dict, Any, Optional
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile

# Create your tests here.

User = get_user_model()


class ProfileTest(APITestCase):
    base_url = "http://localhost:8000/api/v1/profile/"
    
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
    
    def test_retrieve_profile(self) -> None:
        response = self.client.get(path=self.base_url, data=None, format="json", **self.example_bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get().email, "gobfe@evasem.ga")