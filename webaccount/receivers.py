from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from webaccount.models import UserProfile

User = get_user_model()


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()


post_save.connect(create_profile, sender=User)
