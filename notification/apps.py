from django.apps import AppConfig

class NotificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notification'

    def ready(self):
        # if you have signals for notifications specific events, import them here
        try:
            import notification.signals  # noqa: F401
        except Exception:
            # don't break admin if signals error
            pass