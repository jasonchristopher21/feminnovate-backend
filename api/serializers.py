from rest_framework import serializers, exceptions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User

from api.logic.user_management import register_user, update_user

from api.models import (
    Company,
    UserProfile,
    Job
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


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'picture', 'website']


class UserRegistrationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=155)
    username = serializers.CharField(max_length=155)
    email = serializers.EmailField(max_length=155)
    password = serializers.CharField(max_length=155)

    def create(self, validated_data):
        user_details = register_user(**validated_data)
        # user_details.pop('password', None)
        refresh = RefreshToken.for_user(User.objects.get(
            username=user_details.get('username')))
        user_details['refresh'] = str(refresh)
        user_details['access'] = str(refresh.access_token)
        return user_details

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)
        representation['refresh'] = instance.get('refresh')
        representation['access'] = instance.get('access')
        return representation


class UserUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=155)
    email = serializers.EmailField(max_length=155)
    password = serializers.CharField(max_length=155)
    description = serializers.CharField(max_length=155, allow_blank=True)
    picture = serializers.URLField(max_length=155, allow_blank=True)

    def create(self, validated_data):
        user = validated_data.pop('user')
        user_details = update_user(user, **validated_data)
        return user_details


class JwtSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Get password, and usernaem (or email)
        password = attrs.get("password")
        username = attrs.get("username")

        # set user to None
        user = None

        # check if user exists with email addr / username
        if "@" in username:
            user = User.objects.filter(email=username).first()
        else:
            user = User.objects.filter(username=username).first()

        # raise an authentication faled error if user is None
        if user is None:
            raise exceptions.AuthenticationFailed(detail="User not found")

        else:
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)

                return {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'username': user.username,
                    'email': user.email,
                }
            else:
                raise exceptions.AuthenticationFailed(detail="Wrong Password")


class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'responsibilities', 'qualifications', 'company', 'salary',
                  'location', 'is_active']
        read_only_fields = ['company', 'is_active']        

class JobListSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'description', 'company', 'salary', 'location', 'is_active']
        read_only_fields = ['company', 'is_active']     