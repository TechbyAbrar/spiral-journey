from django.urls import path
from .views import NoteCreateView, NoteListView

urlpatterns = [
    path("notes/create/", NoteCreateView.as_view(), name="note-create"),
    path("notes/", NoteListView.as_view(), name="note-list"),
]
