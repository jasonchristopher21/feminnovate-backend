from rest_framework import serializers
from django.contrib.auth.models import User

from api.logic.register_user import register_user

from api.models import (
    UserProfile
)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = UserProfile
        fields = ['user', 'name', 'description', 'picture']

class UserRegistrationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=155)
    username = serializers.CharField(max_length=155)
    email = serializers.EmailField(max_length=155)
    password = serializers.CharField(max_length=155)

    def create(self, validated_data):
        user_details = register_user(**validated_data)
        return user_details