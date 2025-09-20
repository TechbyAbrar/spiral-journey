from django.urls import path
from .views import UserDiscoveryView, QuestionListView, SubmitAnswerView

urlpatterns = [
    path("app/discovery/info/", UserDiscoveryView.as_view(), name="user-discovery"),
    path("questions/", QuestionListView.as_view(), name="question-list"),
    path("submit-answers/", SubmitAnswerView.as_view(), name="submit-answer"),
]


