from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model

from petstagram.accounts.utils import send_welcome_email

PetstagramUser = get_user_model()


@receiver(post_save, sender=PetstagramUser)
def create_petstagram_user(sender, instance, created, **kwargs):
    if created:
        send_welcome_email(instance.email, instance.username)


@receiver(post_save, sender=PetstagramUser)
def save_petstagram_user(sender, instance, **kwargs):
    # Disconnect the signal to avoid recursion
    post_save.disconnect(save_petstagram_user, sender=PetstagramUser)
    instance.save()
    # Reconnect the signal
    post_save.connect(save_petstagram_user, sender=PetstagramUser)

