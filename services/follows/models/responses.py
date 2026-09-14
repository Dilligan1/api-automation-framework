# Модели ответов сервиса подписок.

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from services.common.models.responses import PaginatedResponse, UserBrief


class FollowResponse(BaseModel):
    """
    Результат подписки.

    status: accepted — публичный аккаунт, подписка сразу активна
            pending  — приватный аккаунт, ждёт решения владельца
    """

    id: UUID
    follower: UserBrief
    following: UserBrief
    status: str
    created_at: datetime


class FollowRequestResponse(BaseModel):
    """
    Входящий запрос на подписку (только для приватных аккаунтов).

    От FollowResponse отличается отсутствием following: владелец аккаунта
    и так знает, что запрос адресован ему.
    """

    id: UUID
    follower: UserBrief
    status: str
    created_at: datetime


FollowRequestListResponse = PaginatedResponse[FollowRequestResponse]
