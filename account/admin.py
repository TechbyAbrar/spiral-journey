from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import UserAuth

@admin.register(UserAuth)
class UserAuthAdmin(UserAdmin):
    """Admin panel customization for UserAuth model"""

    # Fields to display in the user list
    list_display = (
        "user_id", "email", "full_name", "username",
        "is_verified", "is_active", "is_staff", "is_superuser",
        "is_subscribed", "created_at"
    )
    list_filter = ("is_verified", "is_active", "is_staff", "is_superuser", "is_subscribed")
    search_fields = ("email", "full_name", "username", "contanct_no", "country")
    ordering = ("-created_at",)