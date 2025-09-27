from django.urls import path
from .views import InnerChildView, MonthlyVoiceHistoryView
from webnote.views import NoteListView
urlpatterns = [
    path('inner-child/details/', InnerChildView.as_view(), name='inner-child'),
    path("notes/", NoteListView.as_view(), name="note-list"),
    path("voice-history/monthly/", MonthlyVoiceHistoryView.as_view(), name="monthly-voice-history"),
]
