# from django.db import transaction
# from rest_framework.views import APIView
# from rest_framework import status
# from rest_framework.response import Response
# from .serializers import SpiralSerializer, SpiralDaySerializer, SpiralReflectionSerializer
# from .pagination import SpiralPagination
# from .services import SpiralService, SpiralDayService, SpiralReflectionService
# from account.utils import success_response, error_response
# from django.shortcuts import get_object_or_404
# from .models import SpiralDay
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.exceptions import PermissionDenied


# # class SpiralListCreateView(APIView):
# #     """Create or List all Spirals"""

# #     def get(self, request):
# #         spirals = SpiralService.list_spirals(user=request.user)
# #         paginator = SpiralPagination()
# #         paginated_spirals = paginator.paginate_queryset(spirals, request)
# #         serializer = SpiralSerializer(paginated_spirals, many=True)

# #         # Build paginated response manually
# #         return Response({
# #             "count": paginator.page.paginator.count,
# #             "total_pages": paginator.page.paginator.num_pages,
# #             "current_page": paginator.page.number,
# #             "next": paginator.get_next_link(),
# #             "previous": paginator.get_previous_link(),
# #             "message": "Spirals retrieved successfully",
# #             "results": serializer.data,
# #         })

# #     @transaction.atomic
# #     def post(self, request):
# #         serializer = SpiralSerializer(data=request.data)
# #         if serializer.is_valid():
# #             spiral = SpiralService.create_spiral(request.user, serializer.validated_data)
# #             return success_response(
# #                 message="Spiral created successfully",
# #                 data=SpiralSerializer(spiral).data,
# #                 status_code=status.HTTP_201_CREATED,
# #             )
# #         return error_response(
# #             message="Validation error",
# #             errors=serializer.errors,
# #             status_code=status.HTTP_400_BAD_REQUEST,
# #         )



# class SpiralListCreateView(APIView):
#     """List spirals for all users, but allow creation only for staff/admin"""

#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         spirals = SpiralService.list_spirals()
#         paginator = SpiralPagination()
#         paginated_spirals = paginator.paginate_queryset(spirals, request)
#         serializer = SpiralSerializer(paginated_spirals, many=True)

#         return Response({
#             "count": paginator.page.paginator.count,
#             "total_pages": paginator.page.paginator.num_pages,
#             "current_page": paginator.page.number,
#             "next": paginator.get_next_link(),
#             "previous": paginator.get_previous_link(),
#             "message": "Spirals retrieved successfully",
#             "results": serializer.data,
#         }, status=status.HTTP_200_OK)

#     @transaction.atomic
#     def post(self, request):
#         # Restrict to staff/admin only
#         if not (request.user.is_staff or request.user.is_superuser):
#             raise PermissionDenied("Only staff or admin users can create spirals.")

#         serializer = SpiralSerializer(data=request.data)
#         if serializer.is_valid():
#             spiral = SpiralService.create_spiral(request.user, serializer.validated_data)
#             return success_response(
#                 message="Spiral created successfully",
#                 data=SpiralSerializer(spiral).data,
#                 status_code=status.HTTP_201_CREATED,
#             )
#         return error_response(
#             message="Validation error",
#             errors=serializer.errors,
#             status_code=status.HTTP_400_BAD_REQUEST,
#         )

# class SpiralDetailView(APIView):
#     """Retrieve, Update or Delete a Spiral"""

#     def get(self, request, pk):
#         spiral = SpiralService.get_spiral(pk, request.user)
#         return success_response(data=SpiralSerializer(spiral).data)

#     @transaction.atomic
#     def put(self, request, pk):
#         spiral = SpiralService.get_spiral(pk, request.user)
#         serializer = SpiralSerializer(spiral, data=request.data, partial=True)
#         if serializer.is_valid():
#             updated_spiral = SpiralService.update_spiral(spiral, serializer.validated_data)
#             return success_response(
#                 message="Spiral updated successfully",
#                 data=SpiralSerializer(updated_spiral).data,
#             )
#         return error_response(
#             message="Validation error",
#             errors=serializer.errors,
#             status_code=status.HTTP_400_BAD_REQUEST,
#         )

#     @transaction.atomic
#     def delete(self, request, pk):
#         spiral = SpiralService.get_spiral(pk, request.user)
#         SpiralService.delete_spiral(spiral)
#         return success_response(
#             message="Spiral deleted successfully",
#             status_code=status.HTTP_204_NO_CONTENT,
#         )


# class SpiralDayView(APIView):
#     """CRUD for Spiral Days"""

#     @transaction.atomic
#     def post(self, request, spiral_id):
#         spiral = SpiralService.get_spiral(spiral_id, request.user)
#         serializer = SpiralDaySerializer(data=request.data)
#         if serializer.is_valid():
#             day = SpiralDayService.create_day(spiral, serializer.validated_data)
#             return success_response(
#                 message="Spiral day created successfully",
#                 data=SpiralDaySerializer(day).data,
#                 status_code=status.HTTP_201_CREATED,
#             )
#         return error_response(
#             message="Validation error",
#             errors=serializer.errors,
#             status_code=status.HTTP_400_BAD_REQUEST,
#         )

#     @transaction.atomic
#     def put(self, request, spiral_id, day_id):
#         day = SpiralDayService.get_day(spiral_id, day_id, request.user)
#         serializer = SpiralDaySerializer(day, data=request.data, partial=True)
#         if serializer.is_valid():
#             updated_day = SpiralDayService.update_day(day, serializer.validated_data)
#             return success_response(
#                 message="Spiral day updated successfully",
#                 data=SpiralDaySerializer(updated_day).data,
#             )
#         return error_response(
#             message="Validation error",
#             errors=serializer.errors,
#             status_code=status.HTTP_400_BAD_REQUEST,
#         )

#     @transaction.atomic
#     def delete(self, request, spiral_id, day_id):
#         day = SpiralDayService.get_day(spiral_id, day_id, request.user)
#         SpiralDayService.delete_day(day)
#         return success_response(
#             message="Spiral day deleted successfully",
#             status_code=status.HTTP_204_NO_CONTENT,
#         )


# class SpiralReflectionView(APIView):
#     @transaction.atomic
#     def post(self, request):
#         serializer = SpiralReflectionSerializer(data=request.data)
#         if serializer.is_valid():
#             reflection = SpiralReflectionService.create_reflection(
#                 user=request.user,
#                 validated_data=serializer.validated_data
#             )
#             return success_response(
#                 message="Reflection created successfully",
#                 data=SpiralReflectionSerializer(reflection).data,
#                 status_code=status.HTTP_201_CREATED,
#             )
#         return error_response(
#             message="Validation error",
#             errors=serializer.errors,
#             status_code=status.HTTP_400_BAD_REQUEST,
#         )


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
from .services import SpiralService, SpiralDayService, SpiralReflectionService
from account.utils import success_response, error_response


class SpiralListCreateView(APIView):
    """List spirals (all users) / Create spirals (staff/admin only)."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        spirals = SpiralService.list_spirals()
        paginator = SpiralPagination()
        paginated_spirals = paginator.paginate_queryset(spirals, request)
        serializer = SpiralSerializer(paginated_spirals, many=True)

        return Response({
            "count": paginator.page.paginator.count,
            "total_pages": paginator.page.paginator.num_pages,
            "current_page": paginator.page.number,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "message": "Spirals retrieved successfully",
            "results": serializer.data,
        }, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        # Restrict to staff/admin only
        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied("Only staff or admin users can create spirals.")

        serializer = SpiralSerializer(data=request.data)
        if serializer.is_valid():
            spiral = SpiralService.create_spiral(request.user, serializer.validated_data)
            return success_response(
                message="Spiral created successfully",
                data=SpiralSerializer(spiral).data,
                status_code=status.HTTP_201_CREATED,
            )
        return error_response(
            message="Validation error",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class SpiralDetailView(APIView):
    """Retrieve (all users), Update/Delete (staff/admin only)."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        spiral = SpiralService.get_spiral(pk)
        return success_response(data=SpiralSerializer(spiral).data)

    @transaction.atomic
    def put(self, request, pk):
        spiral = SpiralService.get_spiral(pk)

        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied("Only staff or admin users can update spirals.")

        serializer = SpiralSerializer(spiral, data=request.data, partial=True)
        if serializer.is_valid():
            updated_spiral = SpiralService.update_spiral(spiral, serializer.validated_data)
            return success_response(
                message="Spiral updated successfully",
                data=SpiralSerializer(updated_spiral).data,
            )
        return error_response(
            message="Validation error",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    @transaction.atomic
    def delete(self, request, pk):
        spiral = SpiralService.get_spiral(pk)

        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied("Only staff or admin users can delete spirals.")

        SpiralService.delete_spiral(spiral)
        return success_response(
            message="Spiral deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT,
        )


class SpiralDayView(APIView):
    """CRUD for Spiral Days (staff/admin only)."""
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, spiral_id):
        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied("Only staff or admin users can create spiral days.")

        spiral = SpiralService.get_spiral(spiral_id)
        serializer = SpiralDaySerializer(data=request.data)
        if serializer.is_valid():
            day = SpiralDayService.create_day(spiral, serializer.validated_data)
            return success_response(
                message="Spiral day created successfully",
                data=SpiralDaySerializer(day).data,
                status_code=status.HTTP_201_CREATED,
            )
        return error_response(
            message="Validation error",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    @transaction.atomic
    def put(self, request, spiral_id, day_id):
        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied("Only staff or admin users can update spiral days.")

        day = SpiralDayService.get_day(spiral_id, day_id)
        serializer = SpiralDaySerializer(day, data=request.data, partial=True)
        if serializer.is_valid():
            updated_day = SpiralDayService.update_day(day, serializer.validated_data)
            return success_response(
                message="Spiral day updated successfully",
                data=SpiralDaySerializer(updated_day).data,
            )
        return error_response(
            message="Validation error",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    @transaction.atomic
    def delete(self, request, spiral_id, day_id):
        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied("Only staff or admin users can delete spiral days.")

        day = SpiralDayService.get_day(spiral_id, day_id)
        SpiralDayService.delete_day(day)
        return success_response(
            message="Spiral day deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT,
        )


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