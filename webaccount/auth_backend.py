from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.utils.translation import ugettext_lazy as _

from .utils import normalise_email

User = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, email=None, password=None, *args, **kwargs):
        if email is None:
            if 'username' not in kwargs or kwargs['username'] is None:
                return None
            clean_email = normalise_email(kwargs['username'])
        else:
            clean_email = normalise_email(email)

        if '@' not in clean_email:
            return None

        matching_users = User.objects.filter(email__iexact=clean_email)
        authenticated_users = [
            user for user in matching_users if user.check_password(password)]
        if len(authenticated_users) == 1:
            return authenticated_users[0]
        elif len(authenticated_users) > 1:
            raise User.MultipleObjectsReturned(
                _("There are multiple users with the given email address and "
                  "password"))
        return None
