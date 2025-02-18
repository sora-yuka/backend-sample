from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .serializers import RegisterUserSerializer
from applications.userprofile.models import Profile

# Create your views here.


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