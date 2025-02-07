from django.urls import path
from .views import ProfileRetrieveAPIView, ProfileUpdateAPIView

urlpatterns = [
    path("", ProfileRetrieveAPIView.as_view()),
    path("update/", ProfileUpdateAPIView.as_view()),
]