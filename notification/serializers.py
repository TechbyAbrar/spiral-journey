# notifications/serializers.py
from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "type", "title", "message", "created_at", "updated_at", "is_read", "archived"]
        read_only_fields = ["id", "created_at", "updated_at"]
