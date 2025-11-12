from typing import List, Dict, Any, Optional
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from .models import Spiral, SpiralDay, SpiralReflection
from rest_framework import serializers

from typing import Any, Dict, List, Optional
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import Spiral, SpiralDay


class SpiralService:
    @staticmethod
    def list_spirals():
        return Spiral.objects.prefetch_related("days").order_by("-created_at")

    @staticmethod
    def get_spiral(pk: int) -> Spiral:
        return get_object_or_404(Spiral.objects.prefetch_related("days"), pk=pk)

    @staticmethod
    @transaction.atomic
    def create_spiral(user, validated_data: Dict[str, Any]) -> Spiral:
        days_data: List[Dict[str, Any]] = validated_data.pop("days", [])
        spiral = Spiral.objects.create(user=user, **validated_data)
        SpiralService._bulk_create_or_update_days(spiral, days_data)
        return Spiral.objects.prefetch_related("days").get(pk=spiral.pk)
    

    @staticmethod
    @transaction.atomic
    def update_spiral(spiral: Spiral, validated_data: Dict[str, Any], partial: bool = False) -> Spiral:
        days_data: Optional[List[Dict[str, Any]]] = validated_data.pop("days", None)

        # Update spiral core fields
        for attr, val in validated_data.items():
            setattr(spiral, attr, val)
        spiral.save()

        # Handle day updates
        if days_data is not None:
            SpiralService._bulk_create_or_update_days(spiral, days_data)

        return Spiral.objects.prefetch_related("days").get(pk=spiral.pk)

    @staticmethod
    def delete_spiral(spiral: Spiral):
        for d in spiral.days.all():
            if d.voice_drop:
                d.voice_drop.delete(save=False)
        spiral.delete()

    @staticmethod
    def _bulk_create_or_update_days(spiral: Spiral, days_data: List[Dict[str, Any]]):
        """Safely update or create SpiralDay entries without breaking unique constraint."""
        existing_days = {d.day_number: d for d in spiral.days.all()}

        seen_day_numbers = set()
        for day_dict in days_data:
            day_number = int(day_dict.get("day_number"))
            if day_number in seen_day_numbers:
                raise ValidationError(f"Duplicate day_number: {day_number}")
            seen_day_numbers.add(day_number)

            journal_prompt = day_dict.get("journal_prompt")
            voice_title = day_dict.get("voice_title")
            voice_drop = day_dict.get("voice_drop")

            # Update if exists, else create
            if day_number in existing_days:
                day = existing_days[day_number]
                day.journal_prompt = journal_prompt or day.journal_prompt
                day.voice_title = voice_title or day.voice_title
                if voice_drop:
                    day.voice_drop = voice_drop
                day.save()
            else:
                SpiralDay.objects.create(
                    spiral=spiral,
                    day_number=day_number,
                    journal_prompt=journal_prompt,
                    voice_title=voice_title,
                    voice_drop=voice_drop,
                )
                
                
    @staticmethod
    def get_spiral_day(spiral_id: int, day_number: int) -> SpiralDay:
        return get_object_or_404(SpiralDay, spiral_id=spiral_id, day_number=day_number)

    @staticmethod
    @transaction.atomic
    def update_spiral_day(spiral_day: SpiralDay, validated_data: Dict[str, Any]) -> SpiralDay:
        for attr, val in validated_data.items():
            setattr(spiral_day, attr, val)
        spiral_day.save()
        return spiral_day

    @staticmethod
    @transaction.atomic
    def admin_update_spiral_day(spiral_day: SpiralDay, validated_data: Dict[str, Any]) -> SpiralDay:
        # prevent breaking unique constraints
        if "day_number" in validated_data:
            new_day_number = validated_data["day_number"]
            if SpiralDay.objects.filter(
                spiral=spiral_day.spiral,
                day_number=new_day_number
            ).exclude(id=spiral_day.id).exists():
                raise ValidationError(f"Day number {new_day_number} already exists for this spiral.")
        
        for attr, val in validated_data.items():
            setattr(spiral_day, attr, val)
        spiral_day.save()
        return spiral_day
    
    @staticmethod
    @transaction.atomic
    def admin_create_spiral_day(spiral_id: int, validated_data: Dict[str, Any]) -> SpiralDay:
        """
        Admin can create a new SpiralDay for a given Spiral.
        Auto-calculates next available day_number if not provided.
        """
        spiral = get_object_or_404(Spiral, pk=spiral_id)

        # If day_number not provided, assign next sequential number
        if not validated_data.get("day_number"):
            validated_data["day_number"] = (
                SpiralDay.objects.filter(spiral=spiral).count() + 1
            )

        day_number = validated_data["day_number"]

        # Prevent duplicate day_number for the same spiral
        if SpiralDay.objects.filter(spiral=spiral, day_number=day_number).exists():
            raise ValidationError(f"Day number {day_number} already exists for this spiral.")

        spiral_day = SpiralDay.objects.create(spiral=spiral, **validated_data)
        return spiral_day





# Service for handling SpiralReflection logic
class SpiralReflectionService:
   
    # def create_reflection(user, validated_data):
    #     """
    #     Allow an authenticated user to create a reflection.
    #     Enforces uniqueness: one reflection per day per user.
    #     """
    #     spiral_day = validated_data["spiral_day"]

    #     if SpiralReflection.objects.filter(user=user, spiral_day=spiral_day).exists():
    #         raise serializers.ValidationError(
    #             "You have already submitted a reflection for this day."
    #         )
        
    #     return SpiralReflection.objects.create(
    #         user=user,
    #         spiral=validated_data["spiral"],
    #         spiral_day=spiral_day,
    #         text_response=validated_data["text_response"]
    #     )
    @staticmethod
    def create_reflection(user, validated_data):
        """
        Allow an authenticated user to create a reflection.
        Enforces uniqueness: one reflection per day per user.
        Marks the corresponding SpiralDay as completed.
        """
        spiral_day = validated_data["spiral_day"]

        # Ensure only one reflection per user per day
        if SpiralReflection.objects.filter(user=user, spiral_day=spiral_day).exists():
            raise serializers.ValidationError(
                "You have already submitted a reflection for this day."
            )
        
        # Create the reflection
        reflection = SpiralReflection.objects.create(
            user=user,
            spiral=validated_data["spiral"],
            spiral_day=spiral_day,
            text_response=validated_data["text_response"]
        )

        # Mark the day as completed
        if not spiral_day.is_completed:
            spiral_day.is_completed = True
            spiral_day.save(update_fields=["is_completed"])

        return reflection
