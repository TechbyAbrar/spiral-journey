from django.shortcuts import get_object_or_404
from .models import Spiral, SpiralDay


class SpiralService:
    @staticmethod
    def list_spirals(user=None):
        """
        Get all spirals, optionally filtered by user.
        """
        qs = Spiral.objects.select_related("user").prefetch_related("days")
        if user:
            qs = qs.filter(user=user)
        return qs.order_by("-created_at")  # ✅ ordered to avoid warnings

    @staticmethod
    def get_spiral(pk, user):
        """
        Retrieve a single spiral owned by the user.
        """
        return get_object_or_404(
            Spiral.objects.select_related("user").prefetch_related("days"),
            pk=pk, user=user,
        )

    @staticmethod
    def create_spiral(user, validated_data):
        """Create a spiral for the given user."""
        return Spiral.objects.create(user=user, **validated_data)

    @staticmethod
    def update_spiral(spiral, validated_data):
        """Update spiral fields safely."""
        for attr, value in validated_data.items():
            setattr(spiral, attr, value)
        spiral.save()
        return spiral

    @staticmethod
    def delete_spiral(spiral):
        spiral.delete()


class SpiralDayService:
    @staticmethod
    def get_day(spiral_id, day_id, user):
        """Retrieve a spiral day owned by the user."""
        return get_object_or_404(
            SpiralDay.objects.select_related("spiral"),
            id=day_id, spiral__id=spiral_id, spiral__user=user,
        )

    @staticmethod
    def create_day(spiral, validated_data):
        return SpiralDay.objects.create(spiral=spiral, **validated_data)

    @staticmethod
    def update_day(day, validated_data):
        for attr, value in validated_data.items():
            setattr(day, attr, value)
        day.save()
        return day

    @staticmethod
    def delete_day(day):
        day.delete()
