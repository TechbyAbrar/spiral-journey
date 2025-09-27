from rest_framework import serializers
from account.models import UserAuth
from onboarding.models import UserAnswer


class DashboardUserSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = UserAuth
        fields = [
            "user_id",
            "profile_pic_url",
            "full_name",
            "email",
            "contanct_no",
            "answers",
        ]

    def get_answers(self, obj):
        """Return simple info about answers (for 'View Answer' link)."""
        answers = obj.answers.all()
        return [
            {
                "question": ans.question.text,
                "answer": ans.get_answer_display(),
                "answered_at": ans.created_at,
            }
            for ans in answers
        ]
