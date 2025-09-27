from rest_framework import serializers
from spiral_journey.models import SpiralReflection

class VoiceHistorySerializer(serializers.ModelSerializer):
    spiral_title = serializers.CharField(source="spiral.title", read_only=True)
    day_number = serializers.IntegerField(source="spiral_day.day_number", read_only=True)
    voice_title = serializers.CharField(source="spiral_day.voice_title", read_only=True)
    voice_drop = serializers.FileField(source="spiral_day.voice_drop", read_only=True)

    class Meta:
        model = SpiralReflection
        fields = [
            "id", "spiral", "spiral_day",
            "spiral_title", "day_number", "voice_title",
            "voice_drop", "created_at"
        ]
    