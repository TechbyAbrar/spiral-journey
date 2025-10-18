from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .serializers import (
    SpiralSerializer,
    SpiralDaySerializer,
    SpiralReflectionSerializer
)
from .pagination import SpiralPagination
from .services import SpiralService, SpiralReflectionService
from account.utils import success_response, error_response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class SpiralListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @transaction.atomic
    def get(self, request):
        spirals = SpiralService.list_spirals()
        serializer = SpiralSerializer(spirals, many=True)
        return success_response("Spirals retrieved", serializer.data)

    @transaction.atomic
    def post(self, request):
        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied("Only staff or admin users can create spirals.")

        serializer = SpiralSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            spiral = SpiralService.create_spiral(request.user, serializer.validated_data)
            return success_response("Spiral created successfully", SpiralSerializer(spiral).data, status.HTTP_201_CREATED)

        return error_response("Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)

class SpiralDetailView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @transaction.atomic
    def get(self, request, pk):
        spiral = SpiralService.get_spiral(pk)
        serializer = SpiralSerializer(spiral)
        return success_response(data=serializer.data)

    @transaction.atomic
    def patch(self, request, pk):
        """Partial update — update spiral info or selected day(s)."""
        spiral = SpiralService.get_spiral(pk)

        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied("Only staff or admin users can update spirals.")

        serializer = SpiralSerializer(
            spiral, data=request.data, partial=True, context={"request": request}
        )

        if serializer.is_valid():
            updated = SpiralService.update_spiral(
                spiral, serializer.validated_data, partial=True
            )
            return success_response("Spiral updated successfully", SpiralSerializer(updated).data)
        return error_response("Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def delete(self, request, pk):
        spiral = SpiralService.get_spiral(pk)

        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied("Only staff or admin users can delete spirals.")

        SpiralService.delete_spiral(spiral)
        return success_response("Spiral deleted", status_code=status.HTTP_204_NO_CONTENT)




# spiral day create api
class AdminSpiralDayCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @transaction.atomic
    def post(self, request, spiral_id):
        """Admin can create a new Spiral Day."""
        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied("Only admin users can create spiral days.")

        serializer = AdminSpiralDaySerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)

        try:
            # Inject spiral_id into validated data
            validated_data = serializer.validated_data
            validated_data["spiral_id"] = spiral_id

            spiral_day = SpiralService.admin_create_spiral_day(
                spiral_id=spiral_id,
                validated_data=validated_data
            )
            return success_response(
                message="Spiral day created successfully.",
                data=AdminSpiralDaySerializer(spiral_day).data,
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return error_response("Failed to create spiral day", str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)





from .serializers import AdminSpiralDaySerializer
class AdminSpiralDayDetailView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @transaction.atomic
    def get(self, request, spiral_id, day_number):
        """Admin can fetch a specific spiral day with all details."""
        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied("Only admin users can access this endpoint.")

        spiral_day = SpiralService.get_spiral_day(spiral_id, day_number)
        serializer = AdminSpiralDaySerializer(spiral_day)
        return success_response(data=serializer.data)

    @transaction.atomic
    def patch(self, request, spiral_id, day_number):
        """Admin can update full spiral day (title, prompt, voice, etc)."""
        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied("Only admin users can update spiral days.")

        spiral_day = SpiralService.get_spiral_day(spiral_id, day_number)
        serializer = AdminSpiralDaySerializer(spiral_day, data=request.data, partial=True)

        if serializer.is_valid():
            updated_day = SpiralService.admin_update_spiral_day(spiral_day, serializer.validated_data)
            return success_response(
                "Spiral day updated successfully by admin",
                AdminSpiralDaySerializer(updated_day).data,
            )
        return error_response("Validation error", serializer.errors, status.HTTP_400_BAD_REQUEST)




# parted

class SpiralReflectionView(APIView):
    """Authenticated users can create reflections."""
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = SpiralReflectionSerializer(data=request.data)
        if serializer.is_valid():
            reflection = SpiralReflectionService.create_reflection(
                user=request.user,
                validated_data=serializer.validated_data
            )
            return success_response(
                message="Reflection created successfully",
                data=SpiralReflectionSerializer(reflection).data,
                status_code=status.HTTP_201_CREATED,
            )
        return error_response(
            message="Validation error",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )



from .models import Soundscape
from .serializers import SoundscapeSerializer
from django.db.models import Count
import random
from rest_framework import permissions
from rest_framework import parsers

class AdminSoundscapeCreateView(APIView):
    """
    Admin Dashboard API to create a new Soundscape
    """
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]  # for file uploads

    def post(self, request):
        serializer = SoundscapeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(
                message="Soundscape created successfully",
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )
        return error_response(
            message="Invalid data",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

class SoundscapeView(APIView):
    permission_classes = [IsAuthenticated]
    """
    API to get a random soundscape based on mood
    """

    def get(self, request):
        mood = request.query_params.get("mood")
        if not mood:
            return error_response(message="Mood parameter is required", status_code=status.HTTP_400_BAD_REQUEST)
        
        soundscapes = Soundscape.objects.filter(mood=mood)
        count = soundscapes.aggregate(count=Count('id'))['count']
        if count == 0:
            return error_response(message="No soundscapes available for this mood", status_code=status.HTTP_404_NOT_FOUND)
        
        random_index = random.randint(0, count - 1)
        soundscape = soundscapes[random_index]
        serializer = SoundscapeSerializer(soundscape)
        return success_response(data=serializer.data) 