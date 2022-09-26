from .models import Profiles
from django.core.exceptions import ObjectDoesNotExist


class AuthBackend(object):
    def get_user(self, profile_id):
        try:
            return Profiles.object.get(pk=profile_id)
        except ObjectDoesNotExist:
            return None

    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None:
            return None
        if password is None:
            return None
        try:
            user = Profiles.object.get(email=email)
            if user.check_password(password):
                return user
        except ObjectDoesNotExist:
            return None