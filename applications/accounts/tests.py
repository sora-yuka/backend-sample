from typing import Dict, Any, Optional
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from applications.userprofile.models import Profile

# Create your tests here.

User = get_user_model()


class AccountTest(APITestCase):
    base_url = "http://localhost:8000/api/v1/account/"
    
    @property 
    def example_bearer_token(self) -> Dict[str, str]:
        """ 
        Getting example bearer token 
        """
        user = User.objects.create(
            email="mafmowiw@ejehot.tv",
            password="ARObPUSjgKfWP",
        )
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}
    
    def test_create_account(self) -> None:
        """ 
        Test account creation functionality.
        """
        url = self.base_url + "register/"
        data = {
            "email": "wel@az.as", 
            "password": "mBhLhCgBMgnQIyXim", 
            "password_confirm": "mBhLhCgBMgnQIyXim",
        }
        response = self.client.post(path=url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "wel@az.as")
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.get().username, "wel@az.as")
        
    def test_login_account(self) -> None:
        """ 
        Test account log in functionality.
        """
        url = self.base_url + "login/"
        data = {"email": "rineku@lolkoah.dz", "password": "XDDyxi"}
        User.objects.create_user(**data)
        response = self.client.post(path=url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    