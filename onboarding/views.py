from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .models import UserDiscovery
from .serializers import UserDiscoverySerializer



from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Question, UserAnswer
from .serializers import QuestionSerializer, UserAnswerSerializer

from account.utils import success_response, error_response

class UserDiscoveryView(APIView):
    """Create, update, or retrieve discovery source for the authenticated user."""
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = UserDiscoverySerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            discovery = serializer.save()
            return success_response(
                "Discovery source saved successfully",
                UserDiscoverySerializer(discovery).data,
                status_code=status.HTTP_200_OK,
            )
        return error_response("Invalid data", serializer.errors)

    def get(self, request):
        try:
            discovery = request.user.discovery
            return success_response(
                "Discovery source retrieved",
                UserDiscoverySerializer(discovery).data,
            )
        except UserDiscovery.DoesNotExist:
            return error_response("No discovery source set.", status_code=status.HTTP_404_NOT_FOUND)


class QuestionListView(APIView):
    """List all questions OR create a new question (admin only)."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        questions = Question.objects.all().order_by("id")
        serializer = QuestionSerializer(questions, many=True)
        return success_response("Questions retrieved successfully", serializer.data)

    @transaction.atomic
    def post(self, request):
        if not request.user.is_staff:
            return error_response("Permission denied", status_code=status.HTTP_403_FORBIDDEN)

        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            return success_response(
                "Question created successfully",
                QuestionSerializer(question).data,
                status_code=status.HTTP_201_CREATED,
            )
        return error_response("Invalid data", serializer.errors)


class SubmitAnswerView(APIView):
    """Submit or update an answer for a question."""
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = UserAnswerSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.validated_data["question"]
            answer = serializer.validated_data["answer"]

            user_answer, _ = UserAnswer.objects.update_or_create(
                user=request.user,
                question=question,
                defaults={"answer": answer},
            )
            return success_response(
                "Answer saved successfully",
                UserAnswerSerializer(user_answer).data,
                status_code=status.HTTP_201_CREATED,
            )
        return error_response("Invalid data", serializer.errors)