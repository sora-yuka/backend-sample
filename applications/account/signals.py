from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.base import ModelBase

from applications.userprofile.models import Profile

User = get_user_model()

@receiver([post_save], sender=User)
def create_profile(sender: ModelBase, instance: User, created: bool, **kwargs):
    if created and not instance.is_staff:
        # Creating profile for new user
        Profile.objects.create(owner=instance)
