from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView

from .models import Profile
from .serializers import ProfileSerializers

# Create your views here.


class OwnProfileRetrieveAPIView(RetrieveAPIView):
    serializer_class = ProfileSerializers
    queryset = Profile.objects.all()
    
    def get_object(self) -> Profile:
        user = self.request.user
        profile = Profile.objects.get(owner=user.id)
        return profile