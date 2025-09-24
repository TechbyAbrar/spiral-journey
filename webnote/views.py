from django.db import transaction
from rest_framework.views import APIView
from .serializers import NoteSerializer
from .services import NoteService
from account.utils import success_response, error_response

class NoteCreateView(APIView):
    @transaction.atomic
    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            note = NoteService.create_note(user=request.user, validated_data=serializer.validated_data)
            return success_response(
                message="Note created successfully",
                data=NoteSerializer(note).data,
                status_code=201
            )
        return error_response(
            message="Validation error",
            errors=serializer.errors,
            status_code=400
        )


class NoteListView(APIView):
    def get(self, request):
        notes = NoteService.list_notes(user=request.user)
        serializer = NoteSerializer(notes, many=True)
        return success_response(
            message="Notes fetched successfully",
            data=serializer.data,
            status_code=200
        )
