from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView,
    TokenRefreshView as BaseTokenRefreshView
)

from .serializers import RegisterUserSerializer
from applications.userprofile.models import Profile


User = get_user_model()


class RegisterUserAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request: Request, format=None) -> Response:
        try:
            serializer = RegisterUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        except IntegrityError:
            return Response(data={
                "Message": "Something went wrong while creating user.",
                "Status": status.HTTP_400_BAD_REQUEST,
            }, status=status.HTTP_400_BAD_REQUEST)

        # 'send email' could be here...
        
        return Response(data={
            "Message": "User created successfully.",
            "Status": status.HTTP_201_CREATED,
        }, status=status.HTTP_201_CREATED)
        

class TokenObtainPairView(BaseTokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        """ 
        Custom token obtain view that sets JWT tokens in HTTP-only cookies. 
        """
        try:
            token_response = super().post(request=request, *args, **kwargs)
            token_data = token_response.data
            
            access_token = token_data.get("access")
            refresh_token = token_data.get("refresh")
            
            if not access_token or not refresh_token:
                raise InvalidToken("Token generation failed")
            
            response = Response(
                data={"detail": "Authorization successful"},
                status=status.HTTP_200_OK
            )
            
            self._set_token_cookie(
                response,
                "access_token",
                access_token,
                max_age=settings.SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME").total_seconds()
            )
            
            self._set_token_cookie(
                response,
                "refresh_token",
                refresh_token,
                max_age=settings.SIMPLE_JWT.get("REFRESH_TOKEN_LIFETIME").total_seconds()
            )
            return response
        except TokenError as error:
            raise InvalidToken(detail=error.args[0])
        
    def _set_token_cookie(self, response: Response, key: str, value: str, max_age: int) -> None:
        """Helper method to set cookies"""
        response.set_cookie(
            key=key,
            value=value,
            max_age=int(max_age),
            path="/",
            secure=getattr(settings, "COOKIE_SECURE", False),
            httponly=True,
            samesite="Lax"
        )

class TokenRefreshView(BaseTokenRefreshView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            
            if not refresh_token:
                raise InvalidToken("Refresh token not found in cookies")
            
            mutable_data = request.data.copy()
            mutable_data["refresh"] = refresh_token
            
            request._full_data = mutable_data
            
            token_response = super().post(request, *args, **kwargs)
            token_data = token_response.data
            
            access_token = token_data.get("access")
            
            if not access_token:
                raise InvalidToken("Access token generation failed")
            
            response = Response(
                data={"detail": "Token refreshed successfully"},
                status=status.HTTP_200_OK
            )
            
            response.set_cookie(
                key="access_token",
                value=access_token,
                max_age=int(settings.SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME").total_seconds()),
                path="/",
                secure=getattr(settings, "COOKIE_SECURE", False),
                httponly=FalseTrue,
                samesite="Lax"
            )
            return response
        except TokenError as error:
            raise InvalidToken(detail=error.args[0])


class LogoutAPIView(APIView):
    def post(self, request: Request) -> Response:
        response = Response({"detail": "Logged out successfully"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
