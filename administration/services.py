# admin/services.py
from django.shortcuts import get_object_or_404
from account.models import UserAuth
from administration.models import AdminUser
from .serializers import AdminSerializer

class AdminService:
    @staticmethod
    def create_admin(validated_data, role="staff"):
        password = validated_data.pop("password")
        user = UserAuth.objects.create_user(
            email=validated_data["email"],
            full_name=validated_data["full_name"],
            username=validated_data["username"],
            password=password,
        )
        user.is_staff = True
        user.is_superuser = (role == "superadmin")
        user.save()

        admin = AdminUser.objects.create(user=user, role=role)
        return admin

    @staticmethod
    def update_admin(admin_id, validated_data):
        admin = get_object_or_404(AdminUser, pk=admin_id)
        serializer = AdminSerializer(instance=admin, data=validated_data, partial=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save()
