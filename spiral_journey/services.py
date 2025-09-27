from django.shortcuts import get_object_or_404
from .models import Spiral, SpiralDay, SpiralReflection
from rest_framework import serializers


class SpiralService:
    @staticmethod
    def list_spirals():
        """
        Get all spirals for all users.
        (Visible to any authenticated user)
        """
        return (
            Spiral.objects
            .select_related("user")
            .prefetch_related("days")
            .order_by("-created_at")
        )

    @staticmethod
    def get_spiral(pk):
        """
        Retrieve a single spiral.
        (Permission handled in views: 
        staff/admin can edit/delete, all users can view)
        """
        return get_object_or_404(
            Spiral.objects.select_related("user").prefetch_related("days"),
            pk=pk,
        )

    @staticmethod
    def create_spiral(user, validated_data):
        """Create a spiral for the given user (staff/admin only)."""
        return Spiral.objects.create(user=user, **validated_data)

    @staticmethod
    def update_spiral(spiral, validated_data):
        """Update spiral fields safely (staff/admin only)."""
        for attr, value in validated_data.items():
            setattr(spiral, attr, value)
        spiral.save()
        return spiral

    @staticmethod
    def delete_spiral(spiral):
        """Delete a spiral (staff/admin only)."""
        spiral.delete()


class SpiralDayService:
    @staticmethod
    def get_day(spiral_id, day_id):
        """
        Retrieve a spiral day.
        (Visible to all authenticated users,
        staff/admin can edit/delete)
        """
        return get_object_or_404(
            SpiralDay.objects.select_related("spiral"),
            id=day_id, spiral__id=spiral_id,
        )

    @staticmethod
    def create_day(spiral, validated_data):
        """Create a day inside a spiral (staff/admin only)."""
        return SpiralDay.objects.create(spiral=spiral, **validated_data)

    @staticmethod
    def update_day(day, validated_data):
        """Update a spiral day (staff/admin only)."""
        for attr, value in validated_data.items():
            setattr(day, attr, value)
        day.save()
        return day

    @staticmethod
    def delete_day(day):
        """Delete a spiral day (staff/admin only)."""
        day.delete()


class SpiralReflectionService:
    @staticmethod
    def create_reflection(user, validated_data):
        """
        Allow an authenticated user to create a reflection.
        Enforces uniqueness: one reflection per day per user.
        """
        spiral_day = validated_data["spiral_day"]

        if SpiralReflection.objects.filter(user=user, spiral_day=spiral_day).exists():
            raise serializers.ValidationError(
                "You have already submitted a reflection for this day."
            )
        
        return SpiralReflection.objects.create(
            user=user,
            spiral=validated_data["spiral"],
            spiral_day=spiral_day,
            text_response=validated_data["text_response"]
        )
