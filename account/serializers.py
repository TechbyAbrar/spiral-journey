from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from .utils import (
    generate_username,
    send_otp_email,
)

User = get_user_model()
from django.db import transaction
from django.utils import timezone

from rest_framework import serializers
from django.utils.crypto import get_random_string
from .models import UserAuth
from .utils import generate_tokens_for_user, validate_google_token, validate_facebook_token
import jwt

from subscription.models import UserSubscription

class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'user_id', 'email', 'full_name', 'username', 'profile_pic',
            'profile_pic_url', 'contanct_no', 'country', 'is_verified',
            'is_active', 'is_staff', 'is_superuser', 'is_subscribed',
            'created_at', 'updated_at',
        ]
        read_only_fields = [
            'user_id', 'email', 'is_verified', 'is_superuser', 'is_staff','otp', 'otp_expired',
            'is_active',
            'is_subscribed', 'created_at', 'updated_at',
        ]
        
    def get_is_subscribed(self, obj):
    # Only one user (request.user) -> single query
        return UserSubscription.objects.filter(user=obj, is_active=True).exists()


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'full_name', 'email', 'password']

    # def validate_password(self, value):
    #     validate_password(value)
    #     return value

    @transaction.atomic
    def create(self, validated_data):
        email = validated_data['email']
        full_name = validated_data['full_name']
        password = validated_data['password']
        username = generate_username(email)

        # Create user instance without using objects.create
        user = User(email=email, full_name=full_name, username=username)
        user.set_password(password)
        user.set_otp()  # Generate OTP
        user.save()     # Save OTP in DB

        print(f"[DEBUG] OTP for {user.email}: {user.otp}")  # Debug: ensure OTP is set

        # Send OTP email
        send_otp_email(user.email, user.otp)
        print(f"[DEBUG] OTP email sent to {user.email} -- {user.otp}")

        return user



class VerifyEmailOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6, write_only=True)

    def validate_otp(self, value):
        """
        Only OTP is required. We fetch the first active, unverified user with this OTP.
        """
        now = timezone.now()

        try:
            # Fetch minimal fields, unverified users only
            user = User.objects.only(
                "user_id", "otp", "otp_expired", "is_verified", "email"
            ).filter(is_verified=False, otp=value, otp_expired__gte=now).first()

            if not user:
                raise serializers.ValidationError("Invalid or expired OTP.")

        except Exception:
            raise serializers.ValidationError("OTP validation failed.")

        self.context["user"] = user
        return value

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.only('email').get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        self.context['user'] = user
        return value

    def save(self):
        user = self.context['user']
        user.set_otp()
        user.save(update_fields=['otp', 'otp_expired'])
        send_otp_email(user.email, user.otp)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_active:
            raise serializers.ValidationError("User account is inactive.")

        attrs['user'] = user
        return attrs


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.only('email', 'otp', 'otp_expired').get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        self.context['user'] = user
        return value

    def save(self):
        user = self.context['user']
        user.set_otp()
        user.save(update_fields=['otp', 'otp_expired'])
        send_otp_email(user.email, user.otp)
        return user


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        if new_password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        # Get the user from the request context (access token)
        user = self.context.get("user")
        if not user or not user.is_authenticated:
            raise serializers.ValidationError("User authentication required.")

        attrs["user"] = user
        return attrs

    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        return user




class VerifyForgetPasswordOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6, write_only=True)

    def validate_otp(self, value):
        try:
            # Only consider verified users
            user = User.objects.only('user_id', 'email', 'otp', 'otp_expired', 'is_verified') \
                            .get(otp=value, is_verified=True)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired OTP.")

        # Double check expiry
        if user.otp_expired is None or user.otp_expired < timezone.now():
            raise serializers.ValidationError("OTP has expired.")

        self.context['user'] = user
        return value



# social auth
class GoogleAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    full_name = serializers.CharField(required=False)
    google_id = serializers.CharField(required=False)
    picture = serializers.URLField(required=False)

    def validate(self, attrs):
        if attrs.get("id_token"):
            google_data = validate_google_token(attrs["id_token"])
            if not google_data or not google_data.get("email"):
                raise serializers.ValidationError("Invalid or expired Google token.")
        else:
            if not attrs.get("email"):
                raise serializers.ValidationError("Email is required if no id_token provided.")
            google_data = {
                "email": attrs.get("email"),
                "name": attrs.get("full_name", ""),
                "sub": attrs.get("google_id"),
                "profile_pic": attrs.get("picture", ""),
            }

        attrs["google_data"] = google_data
        return attrs

    def create(self, validated_data):
        google_data = validated_data["google_data"]
        email_prefix = google_data["email"].split("@")[0][:8]
        username = f"{email_prefix}{get_random_string(4)}"
        while UserAuth.objects.filter(username=username).exists():
            username = f"{email_prefix}{get_random_string(4)}"

        user, created = UserAuth.objects.get_or_create(
            email=google_data["email"],
            defaults={
                "full_name": google_data.get("name", ""),
                "username": username
            }
        )

        if created:
            user.set_unusable_password()
            user.is_verified = True

        if google_data.get("profile_pic") and user.profile_pic_url != google_data["profile_pic"]:
            user.profile_pic_url = google_data["profile_pic"]

        if not user.full_name and google_data.get("name"):
            user.full_name = google_data["name"]

        user.save()
        tokens = generate_tokens_for_user(user)

        return {
            "success": True,
            "message": "User authenticated successfully",
            "access": tokens["access"],
            "refresh": tokens["refresh"],
            "data": {
                "user_profile": UserSerializer(user).data
            },
        }


class FacebookAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField()

    def validate(self, attrs):
        access_token = attrs.get("access_token")
        facebook_data = validate_facebook_token(access_token)

        if not facebook_data or not facebook_data.get("email"):
            raise serializers.ValidationError("Invalid Facebook token or missing email.")

        user, created = UserAuth.objects.get_or_create(
            email=facebook_data["email"],
            defaults={"full_name": facebook_data.get("name", "")},
        )

        if created:
            user.set_unusable_password()
            user.is_verified = True
            user.save()

        tokens = generate_tokens_for_user(user)
        return {
            "success": True,
            "message": "User authenticated successfully",
            "access": tokens["access"],
            "refresh": tokens["refresh"],
            "data": {
                "user_profile": UserSerializer(user).data
            },
        }


class AppleAuthSerializer(serializers.Serializer):
    identity_token = serializers.CharField()

    def validate(self, attrs):
        identity_token = attrs.get("identity_token")
        try:
            apple_data = jwt.decode(identity_token, options={"verify_signature": False})
        except jwt.PyJWTError:
            raise serializers.ValidationError("Invalid Apple identity token.")

        email = apple_data.get("email")
        full_name = apple_data.get("name", "")

        if not email:
            raise serializers.ValidationError("Apple token missing email.")

        user, created = UserAuth.objects.get_or_create(
            email=email,
            defaults={"full_name": full_name},
        )

        if created:
            user.set_unusable_password()
            user.is_verified = True
            user.save()

        tokens = generate_tokens_for_user(user)
        return {
            "success": True,
            "message": "User authenticated successfully",
            "access": tokens["access"],
            "refresh": tokens["refresh"],
            "data": {
                "user_profile": {
                    "user_id": user.user_id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "profile_pic_url": user.profile_pic_url
                }
            },
        }
