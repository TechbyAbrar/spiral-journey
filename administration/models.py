# admin/models.py
from django.db import models
from django.conf import settings

class AdminUser(models.Model):
    ROLE_CHOICES = (
        ("superadmin", "Super Admin"),
        ("staff", "Staff"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="admin_profile"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Admin User"
        verbose_name_plural = "Admin Users"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} ({self.role})"
