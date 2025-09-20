from django.contrib import admin
from .models import UserDiscovery, Question, UserAnswer


@admin.register(UserDiscovery)
class UserDiscoveryAdmin(admin.ModelAdmin):
    """Admin panel for User Discovery source"""
    list_display = ("id", "user", "source", "created_at", "updated_at")
    list_filter = ("source", "created_at")
    search_fields = ("user__email", "user__full_name")
    ordering = ("-created_at",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin panel for Questions"""
    list_display = ("id", "text_preview", "created_at")
    search_fields = ("text",)
    ordering = ("-created_at",)

    def text_preview(self, obj):
        return obj.text[:50] + ("..." if len(obj.text) > 50 else "")
    text_preview.short_description = "Question"


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    """Admin panel for User Answers"""
    list_display = ("id", "user", "question_preview", "answer", "created_at")
    list_filter = ("answer", "created_at")
    search_fields = ("user__email", "user__full_name", "question__text")
    ordering = ("-created_at",)

    def question_preview(self, obj):
        return obj.question.text[:50] + ("..." if len(obj.question.text) > 50 else "")
    question_preview.short_description = "Question"
