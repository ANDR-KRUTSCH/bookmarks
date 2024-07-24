from typing import Any

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.http import HttpRequest

from .models import Profile

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request: HttpRequest, username: str | None = None, password: str | None = None, **kwargs: Any) -> AbstractBaseUser | None:
        try:
            user = User.objects.get(email=username)
            if user.check_password(raw_password=password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None
        
    def get_user(self, user_id: int) -> AbstractBaseUser | None:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        

def create_profile(backend, user: User, *args, **kwargs) -> None:
    user.email = ''
    Profile.objects.get_or_create(user=user)