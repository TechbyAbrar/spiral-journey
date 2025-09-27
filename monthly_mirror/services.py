from django.utils import timezone
from datetime import timedelta
from spiral_journey.models import SpiralReflection

class VoiceHistoryService:
    @staticmethod
    def get_monthly_voice_history(user):
        one_month_ago = timezone.now() - timedelta(days=30)
        return (
            SpiralReflection.objects
            .filter(user=user, created_at__gte=one_month_ago)
            .select_related("spiral_day__spiral")
            .order_by("-created_at")
        )
