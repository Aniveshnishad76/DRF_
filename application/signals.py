from django.core.signals import request_finished
from django.db.models.signals import post_save
from django.dispatch import receiver

from application.models import UserInfo


@receiver(post_save, sender=UserInfo)
def signals(sender, instance, **kwargs):
    instance.is_verified = True
    print("Added Now")
