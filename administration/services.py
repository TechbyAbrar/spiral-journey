# admin/services.py
from django.shortcuts import get_object_or_404
from account.models import UserAuth
from administration.models import AdminUser

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

        if "is_active" in validated_data:
            admin.is_active = validated_data["is_active"]
            admin.user.is_active = validated_data["is_active"]
            admin.user.save()

        if "role" in validated_data:
            admin.role = validated_data["role"]
            # Sync superuser flag
            admin.user.is_superuser = (admin.role == "superadmin")
            admin.user.save()

        admin.save()
        return admin
