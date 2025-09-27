from django.urls import path
from dashboard.views import DashboardUserListView

urlpatterns = [
    path("user-management/", DashboardUserListView.as_view(), name="dashboard-user-list"),
]
