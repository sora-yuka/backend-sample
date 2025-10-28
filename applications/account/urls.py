from django.urls import path

from .views import RegisterUserAPIView, TokenObtainPairView, TokenRefreshView, LogoutAPIView


urlpatterns = [
    path("register/", RegisterUserAPIView.as_view()),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutAPIView.as_view()),
]
