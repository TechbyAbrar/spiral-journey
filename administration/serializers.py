# admin/serializers.py
from rest_framework import serializers
from administration.models import AdminUser
from account.models import UserAuth

class AdminCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True, min_length=6)
    role = serializers.ChoiceField(choices=[("staff", "Staff"), ("superadmin", "Super Admin")])

class AdminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    full_name = serializers.CharField(source="user.full_name", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = AdminUser
        fields = ["id", "email", "full_name", "username", "role", "is_active", "created_at"]
