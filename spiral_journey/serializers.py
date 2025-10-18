from rest_framework import serializers
from .models import Spiral, SpiralDay, SpiralReflection

class SpiralDaySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    voice_drop = serializers.FileField(required=False, allow_null=True, use_url=True)

    class Meta:
        model = SpiralDay
        fields = [
            "id",
            "day_number",
            "journal_prompt",
            "voice_title",
            "voice_drop",
            "is_active",
            "is_completed",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("created_at", "updated_at")

class SpiralSerializer(serializers.ModelSerializer):
    days = SpiralDaySerializer(many=True, required=False)

    class Meta:
        model = Spiral
        fields = [
            "id",
            "title",
            "description",
            "focus_point",
            "duration",
            "days",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("created_at", "updated_at")

    def to_internal_value(self, data):
        """
        Parse day_X_* keys from form-data and convert to days array.
        """
        data = super().to_internal_value(data)
        days = []

        duration = int(data.get("duration", 7))
        request = self.context.get("request")

        for i in range(1, duration + 1):
            day_number = self.initial_data.get(f"day_{i}_number")
            journal_prompt = self.initial_data.get(f"day_{i}_journal_prompt")
            voice_title = self.initial_data.get(f"day_{i}_voice_title")
            voice_drop = request.FILES.get(f"day_{i}_voice_drop") if request else None

            if day_number is not None:
                days.append({
                    "day_number": int(day_number),
                    "journal_prompt": journal_prompt,
                    "voice_title": voice_title,
                    "voice_drop": voice_drop,
                })

        data["days"] = days
        return data



class SpiralDayUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpiralDay
        fields = ["id", "day_number", "journal_prompt", "voice_title", "voice_drop", "is_completed"]
        read_only_fields = ["id", "day_number", "journal_prompt", "voice_title", "voice_drop"]


class AdminSpiralDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = SpiralDay
        fields = [
            "id",
            "spiral",
            "day_number",
            "journal_prompt",
            "voice_title",
            "voice_drop",
            "is_completed",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "spiral", "created_at", "updated_at"]

        
# parted

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



from .models import Soundscape

class SoundscapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soundscape
        fields = ["id", "title", "description", "audio_file", "duration", "mood", "created_at", "updated_at"]