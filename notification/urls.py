# notifications/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("admin-notify/", views.AdminNotificationListView.as_view(), name="admin-notifications"),
    path("count/", views.AdminNotificationCountView.as_view(), name="admin-notifications-count"),
    path("admin/notifications/<int:pk>/read/", views.AdminNotificationMarkReadView.as_view(), name="admin-notification-read"),
    path("admin/notifications/bulk/read/", views.AdminNotificationBulkMarkReadView.as_view(), name="admin-notifications-bulk-read"),
    path("admin/notifications/<int:pk>/archive/", views.AdminNotificationArchiveView.as_view(), name="admin-notification-archive"),
    path("admin/notifications/bulk/archive/", views.AdminNotificationBulkArchiveView.as_view(), name="admin-notifications-bulk-archive"),
]
