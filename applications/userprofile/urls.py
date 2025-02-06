from django.urls import path
from .views import OwnProfileRetrieveAPIView

urlpatterns = [
    path("", OwnProfileRetrieveAPIView.as_view()),
]