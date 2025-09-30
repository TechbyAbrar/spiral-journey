# notifications/admin.py
from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "title", "is_read", "archived", "created_at")
    list_filter = ("type", "is_read", "archived", "created_at")
    search_fields = ("title", "message")
    ordering = ("-created_at",)
