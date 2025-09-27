from django.db import transaction
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .permissions import IsSuperUserOrReadOnly
from .serializers import (
    SignupSerializer,
    VerifyEmailOTPSerializer,
    ResendOTPSerializer,
    LoginSerializer,
    ForgetPasswordSerializer,
    ResetPasswordSerializer,
    UserSerializer,
    VerifyForgetPasswordOTPSerializer,
    GoogleAuthSerializer,
    FacebookAuthSerializer,
    AppleAuthSerializer
)
from .utils import generate_tokens_for_user, success_response, error_response

User = get_user_model()
from rest_framework import permissions

class SignupView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return success_response(
                "User registered successfully. Please verify your email.We have sent an OTP to your email.",
                {
                    "user_id": user.user_id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "username": user.username,
                },
                status_code=status.HTTP_201_CREATED,
            )
        return error_response("Signup failed", serializer.errors)



class VerifyEmailOTPView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = VerifyEmailOTPSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.context["user"]
            user.is_verified = True
            user.save(update_fields=["is_verified"])  # minimal write

            tokens = generate_tokens_for_user(user)
            return success_response(
                "Email verified successfully",
                {"user_id": user.user_id, "email": user.email, "tokens": tokens},
            )

        return error_response("OTP verification failed", serializer.errors)
    
class ResendOTPView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return success_response(f"OTP resent to {user.email}")
        return error_response("Resend OTP failed", serializer.errors)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = generate_tokens_for_user(user)

            # Serialize user data
            user_data = UserSerializer(user).data
            user_data['tokens'] = tokens  # append JWT tokens

            return success_response(
                "Login successful",
                user_data
            )

        return error_response("Login failed", serializer.errors)


class ForgetPasswordView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return success_response(f"OTP sent to {user.email} for password reset.")
        return error_response("Forget password failed", serializer.errors)


class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]  # access token required

    @transaction.atomic
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return success_response("Password reset successfully.")
        return error_response("Reset password failed", serializer.errors)



class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return success_response("Profile fetched successfully", serializer.data)

    @transaction.atomic
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response("Profile updated successfully", serializer.data)
        return error_response("Profile update failed", serializer.errors)


class SpecificUserView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        try:
            user = User.objects.only(
                'user_id', 'email', 'full_name', 'username', 'profile_pic',
                'profile_pic_url', 'contanct_no', 'country', 'is_verified', 'is_active'
            ).get(user_id=user_id)
        except User.DoesNotExist:
            return error_response("User not found", status_code=404)

        serializer = UserSerializer(user)
        return success_response("User fetched successfully", serializer.data)


class VerifyForgetPasswordOTPView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = VerifyForgetPasswordOTPSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.context['user']

            # Use the existing utility function to generate tokens
            tokens = generate_tokens_for_user(user)

            return success_response(
                f"OTP verified successfully for {user.email}",
                {"access_token": tokens["access"]}  # Only provide access token for reset
            )

        return error_response("OTP verification failed", serializer.errors)



# User deletion



class DeleteUserView(APIView):
    """
    Admin-only endpoint to delete a user by user_id.
    """
    permission_classes = [IsSuperUserOrReadOnly]

    @transaction.atomic
    def delete(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return error_response("User not found", status_code=status.HTTP_404_NOT_FOUND)

        # Prevent admin from deleting themselves
        if user == request.user:
            return error_response("You cannot delete your own account", status_code=status.HTTP_400_BAD_REQUEST)

        user.delete()
        return success_response(f"User {user.email} deleted successfully.", status_code=status.HTTP_200_OK)
    
    
# social auth


# ---------------------------
# Google Login View
# ---------------------------
class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.create(serializer.validated_data)
            return success_response(
                data.get("message", "Login successful"),
                data
            )
        return error_response("Google login failed", serializer.errors)


# ---------------------------
# Facebook Login View
# ---------------------------
class FacebookLoginView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = FacebookAuthSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validate(serializer.validated_data)
            return success_response(
                data.get("message", "Login successful"),
                data
            )
        return error_response("Facebook login failed", serializer.errors)


# ---------------------------
# Apple Login View
# ---------------------------
class AppleLoginView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = AppleAuthSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validate(serializer.validated_data)
            return success_response(
                data.get("message", "Login successful"),
                data
            )
        return error_response("Apple login failed", serializer.errors)