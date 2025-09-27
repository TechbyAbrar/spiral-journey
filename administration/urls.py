from django.urls import path
from administration.views import AdminCreateView, AdminUpdateView, AdminListView, AdminDeleteView

urlpatterns = [
    path("create-admin/", AdminCreateView.as_view(), name="create-admin"),
    path("admin-update/<int:admin_id>/", AdminUpdateView.as_view(), name="update-admin"),
    path("delete/<int:admin_id>/", AdminDeleteView.as_view(), name="admin-delete"),
    path("staff/list/", AdminListView.as_view(), name="list-admins"),
]
