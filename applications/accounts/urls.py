from django.urls import path

from .views import RegisterUserAPIView, TokenObtainPairView, TokenRefreshView, LogoutAPIView
from .oauth_views import GoogleOAuthInitiateView, GoogleOAuthCallbackView


urlpatterns = [
    path("register/", RegisterUserAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutAPIView.as_view()),
    
    path("auth/google/", GoogleOAuthInitiateView.as_view(), name="google_oauth_init"),
    path("auth/google/callback/", GoogleOAuthCallbackView.as_view(), name="google_oauth_callback"),
]
