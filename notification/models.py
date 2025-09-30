# notifications/models.py
from django.db import models
from django.utils import timezone


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("ACCOUNT", "Account"),
        ("PAYMENT", "Payment"),
        ("SUPPORT", "Support"),
        ("SYSTEM", "System"),
    ]

    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default="SYSTEM")
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    is_read = models.BooleanField(default=False, db_index=True)
    for_admin = models.BooleanField(default=True, db_index=True)
    archived = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_read"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["archived"]),
        ]

    def __str__(self):
        return f"{self.type} | {self.title}"
