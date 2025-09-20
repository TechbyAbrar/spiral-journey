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



class UserDiscoveryView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        """Create or update discovery source for the authenticated user."""
        serializer = UserDiscoverySerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            discovery = serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Discovery source saved successfully.",
                    "data": UserDiscoverySerializer(discovery).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"success": False, "message": "Invalid data.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get(self, request):
        """Retrieve current user’s discovery source."""
        try:
            discovery = request.user.discovery
            serializer = UserDiscoverySerializer(discovery)
            return Response(
                {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
            )
        except UserDiscovery.DoesNotExist:
            return Response(
                {"success": False, "message": "No discovery source set."},
                status=status.HTTP_404_NOT_FOUND,
            )


class QuestionListView(APIView):
    """List all questions for the survey"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        questions = Question.objects.all().order_by("id")
        serializer = QuestionSerializer(questions, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)


class SubmitAnswerView(APIView):
    """Submit or update an answer"""
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = UserAnswerSerializer(data=request.data)
        if serializer.is_valid():
            question_id = serializer.validated_data["question"].id
            answer = serializer.validated_data["answer"]

            user_answer, _ = UserAnswer.objects.update_or_create(
                user=request.user,
                question_id=question_id,
                defaults={"answer": answer},
            )

            return Response(
                {"success": True, "message": "Answer saved", "data": UserAnswerSerializer(user_answer).data},
                status=status.HTTP_201_CREATED,
            )

        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
