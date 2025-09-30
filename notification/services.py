# notifications/services.py
from typing import Iterable, List
from .models import Notification
from django.db import transaction


class NotificationService:
    @staticmethod
    def create_admin_notification(type_: str, title: str, message: str) -> Notification:
        return Notification.objects.create(
            type=type_,
            title=title,
            message=message,
            for_admin=True
        )

    @staticmethod
    def mark_as_read(notification_id: int) -> bool:
        updated = Notification.objects.filter(id=notification_id, for_admin=True).update(is_read=True)
        return bool(updated)

    @staticmethod
    def bulk_mark_as_read(notification_ids: Iterable[int]) -> int:
        with transaction.atomic():
            updated = Notification.objects.filter(id__in=notification_ids, for_admin=True).update(is_read=True)
        return updated

    @staticmethod
    def archive(notification_id: int) -> bool:
        updated = Notification.objects.filter(id=notification_id, for_admin=True).update(archived=True)
        return bool(updated)

    @staticmethod
    def bulk_archive(notification_ids: Iterable[int]) -> int:
        with transaction.atomic():
            updated = Notification.objects.filter(id__in=notification_ids, for_admin=True).update(archived=True)
        return updated
