# admin/views.py
from rest_framework.views import APIView
from rest_framework import status, permissions
from administration.services import AdminService
from administration.serializers import AdminCreateSerializer, AdminSerializer
from administration.models import AdminUser
from account.utils import success_response, error_response


class AdminCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not request.user.is_superuser:
            return error_response(
                message="Only superusers can create admin/staff",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        serializer = AdminCreateSerializer(data=request.data)
        if serializer.is_valid():
            admin = AdminService.create_admin(
                serializer.validated_data, role=serializer.validated_data["role"]
            )
            return success_response(
                message="Admin/Staff created successfully",
                data=AdminSerializer(admin).data,
                status_code=status.HTTP_201_CREATED,
            )
        return error_response(
            message="Invalid data", errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST
        )


class AdminUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, admin_id):
        if not request.user.is_superuser:
            return error_response(
                message="Only superusers can update admins",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        try:
            admin = AdminService.update_admin(admin_id, request.data)
            return success_response(
                message="Admin updated successfully",
                data=AdminSerializer(admin).data,
                status_code=status.HTTP_200_OK,
            )
        except AdminUser.DoesNotExist:
            return error_response(
                message="Admin not found", status_code=status.HTTP_404_NOT_FOUND
            )


class AdminDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, admin_id):
        if not request.user.is_superuser:
            return error_response(
                message="Only superusers can delete admins",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        try:
            admin = AdminUser.objects.get(id=admin_id)
            admin.delete()
            return success_response(
                message="Admin deleted successfully",
                status_code=status.HTTP_200_OK,
            )
        except AdminUser.DoesNotExist:
            return error_response(
                message="Admin not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )




class AdminListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if not request.user.is_superuser:
            return error_response(
                message="Only superusers can view admins",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        admins = AdminUser.objects.select_related("user").all()
        serializer = AdminSerializer(admins, many=True)
        return success_response(
            message="Admin list retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

