from rest_framework import serializers
from .models import UserDiscovery, DiscoverySource


class UserDiscoverySerializer(serializers.ModelSerializer):
    source_display = serializers.CharField(source="get_source_display", read_only=True)

    class Meta:
        model = UserDiscovery
        fields = ["id", "source", "source_display", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at", "source_display"]

    def create(self, validated_data):
        user = self.context["request"].user
        # Ensure one-to-one constraint
        discovery, _ = UserDiscovery.objects.update_or_create(
            user=user,
            defaults=validated_data,
        )
        return discovery




from .models import Question, UserAnswer

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "text"]


class UserAnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.ReadOnlyField(source="question.text")

    class Meta:
        model = UserAnswer
        fields = ["id", "question", "question_text", "answer", "created_at"]
        read_only_fields = ["id", "question_text", "created_at"]
