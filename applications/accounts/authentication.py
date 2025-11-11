from typing import Optional, Tuple
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token

User = get_user_model()


class CookiesJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> Optional[Tuple[User, Token]]:
        raw_token = request.COOKIES.get("access_token")
        
        if raw_token:
            validated_token = self.get_validated_token(raw_token=raw_token)
            try:
                return self.get_user(validated_token=validated_token), validated_token
            except AuthenticationFailed as error:
                print("Error occured during login: ", error) # Change into logger
        return None
