from django.contrib import admin
from .models import Spiral, SpiralDay, SpiralReflection

@admin.register(Spiral)
class SpiralAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "focus_point", "duration", "created_at")
    list_filter = ("focus_point", "duration", "created_at", "user")
    search_fields = ("title", "description", "focus_point", "user__username")
    ordering = ("-created_at",)

@admin.register(SpiralDay)
class SpiralDayAdmin(admin.ModelAdmin):
    list_display = ("id", "spiral", "day_number", "journal_prompt", "is_active", "created_at")
    list_filter = ("spiral", "is_active", "created_at")
    search_fields = ("journal_prompt", "spiral__title")
    ordering = ("spiral", "day_number")

@admin.register(SpiralReflection)
class SpiralReflectionAdmin(admin.ModelAdmin):
    list_display = ("id", "spiral", "spiral_day", "user", "text_response", "created_at")
    list_filter = ("spiral", "spiral_day", "user", "created_at")
    search_fields = ("text_response", "user__username", "spiral__title")
    ordering = ("-created_at",)
