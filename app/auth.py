"""
Custom authentication backend for login using username or email
"""

from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to find the user by username or email
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)  # Hash the password to reduce timing attack
        except MultipleObjectsReturned:
            # If multiple users are found, try to find the user by username
            # (this is a fallback, not the main logic)
            return UserModel.objects.filter(email=username).order_by('id').first()
        else:
            # If a user is found, check the password
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
