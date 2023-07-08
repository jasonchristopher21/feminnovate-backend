from django.db import transaction, IntegrityError
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest

from rest_framework.exceptions import APIException
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import (
    UserProfile
)

class DuplicateUsernameException(APIException):
    status_code = 400
    default_detail = "Username or email already exists. Please choose a different username/email."
    default_code = "duplicate_username"

@transaction.atomic
def register_user(
    username: str,
    email: str,
    password: str,
    name: str,
) -> dict:

    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.save()

    except IntegrityError:
        raise DuplicateUsernameException()

    user_profile, created = UserProfile.objects.update_or_create(
        user=user,
        defaults={
            'name': name,
            'description': "",
            'picture': "",
        }
    )

    refresh = RefreshToken.for_user(user)

    return {
        'username': user.username,
        'email': user.email,
        'name': user_profile.name,
        'password': user.password,
    }
