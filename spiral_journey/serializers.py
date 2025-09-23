from rest_framework import serializers
from .models import Spiral, SpiralDay


class SpiralDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = SpiralDay
        fields = [
            "id", "day_number", "journal_prompt",
            "voice_drop", "is_active", "created_at", "updated_at",
        ]


class SpiralSerializer(serializers.ModelSerializer):
    days = SpiralDaySerializer(many=True, read_only=True)

    class Meta:
        model = Spiral
        fields = [
            "id", "title", "description", "focus_point", "duration",
            "days", "created_at", "updated_at",
        ]
