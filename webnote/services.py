from .models import Note
from django.shortcuts import get_object_or_404

class NoteService:
    @staticmethod
    def create_note(user, validated_data):
        """Create a new note for a user"""
        return Note.objects.create(user=user, **validated_data)

    @staticmethod
    def list_notes(user):
        """Return all notes for a user, ordered by newest first"""
        return Note.objects.filter(user=user).only('id', 'title', 'content', 'created_at', 'updated_at').order_by('-created_at')
