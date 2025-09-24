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
        

from .models import SpiralReflection

class SpiralReflectionSerializer(serializers.ModelSerializer):
    spiral = serializers.PrimaryKeyRelatedField(queryset=Spiral.objects.all())
    spiral_day = serializers.PrimaryKeyRelatedField(queryset=SpiralDay.objects.all())

    class Meta:
        model = SpiralReflection
        fields = ["id", "spiral", "spiral_day", "text_response", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        # Ensure the spiral_day belongs to the spiral
        if attrs["spiral_day"].spiral.id != attrs["spiral"].id:
            raise serializers.ValidationError("The spiral_day does not belong to the given spiral.")
        return attrs
