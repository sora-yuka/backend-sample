from typing import Dict, Any

from rest_framework import serializers
from django.contrib.auth import get_user_model

from applications.userprofile.models import Profile


User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(
        min_length=6, write_only=True, required=True
        )
    
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "password_confirm",
        ]
    
    def validate(self, attrs: Dict[str, str]) -> Dict[str, str]:
        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm")
        
        if password != password_confirm:
            raise serializers.ValidationError({"password_confirm": ["Password do not match."]})
        return attrs
    
    def create(self, validated_data: Dict[str, str]) -> User:
        user = User.objects.create_user(**validated_data)
        return user
    