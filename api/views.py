from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from api.serializers import (
    JwtSerializer,
    UserSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
)

# Create your views here.
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def public(request):
#     return JsonResponse({'message': 'Hello from a public endpoint!'})


class PublicView(APIView):

    def get(self, request):
        return Response({
            '1': 'Never gonna give you up, never gonna let you down.',
            '2': 'Never gonna run around and desert you.',
            '3': 'Never gonna make you cry, never gonna say goodbye.',
            '4': 'Never gonna tell a lie and hurt you.'
        })


class RegisterUserView(generics.CreateAPIView):

    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": "Error retrieving user: {}".format(str(e))},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = UserProfileSerializer(user.userprofile)
        return Response(serializer.data)
    

class JwtView(TokenObtainPairView):
    serializer_class = JwtSerializer