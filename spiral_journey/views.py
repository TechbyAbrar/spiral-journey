from django.db import transaction
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import SpiralSerializer, SpiralDaySerializer
from .pagination import SpiralPagination
from .services import SpiralService, SpiralDayService
from account.utils import success_response, error_response


class SpiralListCreateView(APIView):
    """Create or List all Spirals"""

    def get(self, request):
        spirals = SpiralService.list_spirals(user=request.user)
        paginator = SpiralPagination()
        paginated_spirals = paginator.paginate_queryset(spirals, request)
        serializer = SpiralSerializer(paginated_spirals, many=True)

        # Build paginated response manually
        return Response({
            "count": paginator.page.paginator.count,
            "total_pages": paginator.page.paginator.num_pages,
            "current_page": paginator.page.number,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "message": "Spirals retrieved successfully",
            "results": serializer.data,
        })

    @transaction.atomic
    def post(self, request):
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
    """Retrieve, Update or Delete a Spiral"""

    def get(self, request, pk):
        spiral = SpiralService.get_spiral(pk, request.user)
        return success_response(data=SpiralSerializer(spiral).data)

    @transaction.atomic
    def put(self, request, pk):
        spiral = SpiralService.get_spiral(pk, request.user)
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
        spiral = SpiralService.get_spiral(pk, request.user)
        SpiralService.delete_spiral(spiral)
        return success_response(
            message="Spiral deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT,
        )


class SpiralDayView(APIView):
    """CRUD for Spiral Days"""

    @transaction.atomic
    def post(self, request, spiral_id):
        spiral = SpiralService.get_spiral(spiral_id, request.user)
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
        day = SpiralDayService.get_day(spiral_id, day_id, request.user)
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
        day = SpiralDayService.get_day(spiral_id, day_id, request.user)
        SpiralDayService.delete_day(day)
        return success_response(
            message="Spiral day deleted successfully",
            status_code=status.HTTP_204_NO_CONTENT,
        )
