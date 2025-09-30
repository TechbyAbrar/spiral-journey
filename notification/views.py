# notifications/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.db.models import Q

from .models import Notification
from .serializers import NotificationSerializer
from .services import NotificationService

from account.utils import success_response, error_response



class AdminNotificationListView(APIView):
    """
    GET /api/admin/notifications/?status=all|unread&since=ISO_DATETIME&archived=false
    Returns notifications for admin. Supports incremental fetching via `since` param.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        status_filter = request.query_params.get("status", "all")
        since = request.query_params.get("since")
        archived = request.query_params.get("archived", "false").lower() in ("true", "1", "yes")

        qs = Notification.objects.filter(for_admin=True)

        if status_filter == "unread":
            qs = qs.filter(is_read=False)

        qs = qs.filter(archived=archived)

        if since:
            dt = parse_datetime(since)
            if dt is None:
                return error_response("Invalid 'since' datetime format. Use ISO 8601.", status_code=400)
            qs = qs.filter(updated_at__gt=dt)

        serializer = NotificationSerializer(qs, many=True)
        return success_response(data=serializer.data, message="Admin notifications fetched successfully")


class AdminNotificationCountView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        unread_count = Notification.objects.filter(for_admin=True, is_read=False, archived=False).count()
        return success_response(data={"unread_count": unread_count}, message="Unread notifications count fetched successfully")


class AdminNotificationMarkReadView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        ok = NotificationService.mark_as_read(pk)
        if ok:
            return success_response(message="Notification marked as read")
        return error_response("Notification not found", status_code=404)


class AdminNotificationBulkMarkReadView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        ids = request.data.get("ids")
        if not isinstance(ids, list):
            return error_response("Field 'ids' must be a list of integers", status_code=400)
        updated = NotificationService.bulk_mark_as_read(ids)
        return success_response(data={"updated_count": updated}, message="Notifications marked as read successfully")


class AdminNotificationArchiveView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        ok = NotificationService.archive(pk)
        if ok:
            return success_response(message="Notification archived successfully")
        return error_response("Notification not found", status_code=404)


class AdminNotificationBulkArchiveView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        ids = request.data.get("ids")
        if not isinstance(ids, list):
            return error_response("Field 'ids' must be a list of integers", status_code=400)
        updated = NotificationService.bulk_archive(ids)
        return success_response(data={"updated_count": updated}, message="Notifications archived successfully")