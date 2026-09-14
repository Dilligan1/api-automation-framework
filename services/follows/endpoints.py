# Эндпоинты подписок. Для приватных аккаунтов подписка уходит в pending
# и требует accept/reject владельцем — это ключевой статусный переход сервиса.

from config.stages import API_PREFIX


class FollowEndpoints:
    requests = f"{API_PREFIX}/follows/requests"

    @staticmethod
    def follow(username: str) -> str:
        return f"{API_PREFIX}/users/{username}/follow"

    @staticmethod
    def accept(follow_id: str) -> str:
        return f"{API_PREFIX}/follows/requests/{follow_id}/accept"

    @staticmethod
    def reject(follow_id: str) -> str:
        return f"{API_PREFIX}/follows/requests/{follow_id}/reject"
