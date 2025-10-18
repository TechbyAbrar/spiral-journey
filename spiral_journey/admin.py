from django.contrib import admin
from .models import Spiral, SpiralDay, SpiralReflection


class SpiralDayInline(admin.TabularInline):
    model = SpiralDay
    extra = 1
    fields = ("day_number", "journal_prompt", "voice_title", "voice_drop", "is_active", "is_completed")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Spiral)
class SpiralAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "duration", "created_at", "updated_at")
    list_filter = ("created_at", "user")
    search_fields = ("title", "description", "focus_point", "user__username", "user__email")
    inlines = [SpiralDayInline]
    ordering = ("-created_at",)


@admin.register(SpiralDay)
class SpiralDayAdmin(admin.ModelAdmin):
    list_display = ("spiral", "day_number", "voice_title", "is_active", "is_completed", "created_at")
    list_filter = ("is_active", "is_completed", "created_at")
    search_fields = ("spiral__title", "voice_title", "journal_prompt")
    ordering = ("spiral", "day_number")


@admin.register(SpiralReflection)
class SpiralReflectionAdmin(admin.ModelAdmin):
    list_display = ("id", "spiral", "spiral_day", "user", "text_response", "created_at")
    list_filter = ("spiral", "spiral_day", "user", "created_at")
    search_fields = ("text_response", "user__username", "spiral__title")
    ordering = ("-created_at",)
