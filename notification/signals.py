# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from notification.services import NotificationService

User = get_user_model()

@receiver(post_save, sender=User)
def notify_admin_on_new_user(sender, instance, created, **kwargs):
    if created:
        NotificationService.create_admin_notification(
            type_="ACCOUNT",
            title="New Account Created",
            message=f"A new account has been created: {getattr(instance, 'email', str(instance))}"
        )
