from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.


class DiscoverySource(models.TextChoices):
    SOCIAL_MEDIA = "social_media", "Social Media"
    ADS = "ads", "Ads"
    APP_STORE = "app_store", "App Store"
    WORD_OF_MOUTH = "word_of_mouth", "Word Of Mouth"
    PODCASTS_MEDIA = "podcasts_media", "Podcasts / Media"
    THERAPIST = "therapist", "Therapist / Medical Professional"
    STREAMING_PLATFORMS = "streaming_platforms", "Streaming Platforms"
    OTHER = "other", "Other"
    
    
class UserDiscovery(models.Model):
    user = models.OneToOneField(User,
        on_delete=models.CASCADE,
        related_name="discovery",
    )
    source = models.CharField(
        max_length=50,
        choices=DiscoverySource.choices,
        default=DiscoverySource.OTHER,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.get_source_display()}"
    
    
    

class Question(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]  # show preview


class AnswerChoice(models.TextChoices):
    YES = "yes", "Yes"
    NO = "no", "No"
    SOMETIMES = "sometimes", "Sometimes"


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    answer = models.CharField(max_length=10, choices=AnswerChoice.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "question")  # prevent duplicate answers

    def __str__(self):
        return f"{self.user.email} - {self.question.text[:30]} - {self.get_answer_display()}"
