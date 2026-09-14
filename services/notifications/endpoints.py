# Эндпоинты уведомлений.

from config.stages import API_PREFIX


class NotificationEndpoints:
    notifications = f"{API_PREFIX}/notifications"
    unread_count  = f"{API_PREFIX}/notifications/unread-count"
    read_all      = f"{API_PREFIX}/notifications/read-all"

    @staticmethod
    def read(notification_id: str) -> str:
        return f"{API_PREFIX}/notifications/{notification_id}/read"
