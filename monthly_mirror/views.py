from django.shortcuts import render
from onboarding.models import UserAnswer
from onboarding.serializers import UserAnswerSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from account.utils import success_response, error_response
from account.permissions import IsOwnerOrSuperuser

class InnerChildView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        answers = UserAnswer.objects.filter(user=user)
        serializer = UserAnswerSerializer(answers, many=True)
        return success_response(data=serializer.data)
    
    

from rest_framework.permissions import IsAuthenticated

from .services import VoiceHistoryService
from .serializers import VoiceHistorySerializer


class MonthlyVoiceHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reflections = VoiceHistoryService.get_monthly_voice_history(request.user)
        serializer = VoiceHistorySerializer(reflections, many=True)
        return Response(serializer.data)
