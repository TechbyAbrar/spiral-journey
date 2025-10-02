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
    email = serializers.EmailField(source="user.email")
    full_name = serializers.CharField(source="user.full_name")
    username = serializers.CharField(source="user.username")

    class Meta:
        model = AdminUser
        fields = ["id", "email", "full_name", "username", "role", "is_active", "created_at"]

    def update(self, instance, validated_data):
        # Update related user fields
        user_data = validated_data.pop("user", {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        # Update AdminUser fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
