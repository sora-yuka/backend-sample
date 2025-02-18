from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, GenericAPIView

from .models import Profile
from .serializers import ProfileSerializers

# Create your views here.


class RetrieveProfileAction(GenericAPIView):
    serializer_class = ProfileSerializers
    queryset = Profile.objects.all()
    
    def get_object(self) -> Profile:
        user = self.request.user
        profile = Profile.objects.get(owner=user.id)
        return profile


class ProfileRetrieveAPIView(RetrieveProfileAction, RetrieveAPIView):
    pass
    
    
class ProfileUpdateAPIView(RetrieveProfileAction, UpdateAPIView):
    pass
    
    
class ProfileListAPIView(ListAPIView):
    serializer_class = ProfileSerializers
    queryset = Profile.objects.all()