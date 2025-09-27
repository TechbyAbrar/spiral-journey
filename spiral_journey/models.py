from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TimeStampedModel(models.Model):
    """Abstract base for created/updated tracking"""
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class Spiral(TimeStampedModel):
    """Represents a journaling spiral"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="spirals")
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    focus_point = models.CharField(max_length=255)
    duration = models.PositiveIntegerField(default=7)  # days

    def __str__(self):
        return self.title


class SpiralDay(TimeStampedModel):
    """Daily prompt inside a spiral"""
    spiral = models.ForeignKey(Spiral, on_delete=models.CASCADE, related_name="days")
    day_number = models.PositiveIntegerField()
    journal_prompt = models.TextField()
    voice_title = models.CharField(max_length=255, blank=True, null=True)
    voice_drop = models.FileField(
        upload_to="spiral_voice_drops/",  # folder inside MEDIA_ROOT
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("spiral", "day_number")
        ordering = ["day_number"]

    def __str__(self):
        return f"{self.spiral.title} - Day {self.day_number}"
    
    

class SpiralReflection(TimeStampedModel):
    """User's reflection for a specific day in a spiral"""
    spiral = models.ForeignKey(Spiral, on_delete=models.CASCADE, related_name="reflections")
    spiral_day = models.ForeignKey(SpiralDay, on_delete=models.CASCADE, related_name="reflections")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="spiral_reflections")
    text_response = models.TextField()

    class Meta:
        unique_together = ("spiral_day", "user")  # each user can only reflect once per day

    def __str__(self):
        return f"Reflection by {self.user.username} on {self.spiral.title} - Day {self.spiral_day.day_number}"
    
    

from django.utils.translation import gettext_lazy as _

class Soundscape(models.Model):
    class MoodChoices(models.TextChoices):
        ANXIOUS = "anxious", _("Anxious")
        OVERWHELMED = "overwhelmed", _("Overwhelmed")
        CANT_SLEEP = "cant_sleep", _("Can't Sleep")
        NEED_CALM = "need_calm", _("Need Calm")
        STUDY = "study", _("Study")
        RELAX = "relax", _("Relax")
    
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    audio_file = models.FileField(upload_to="soundscapes/")
    duration = models.PositiveIntegerField(help_text="Duration in seconds")
    mood = models.CharField(
        max_length=20,
        choices=MoodChoices.choices,
        db_index=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title
