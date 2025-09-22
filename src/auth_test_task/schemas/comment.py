"""Схемы для работы с комментариями."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import Field

from auth_test_task.schemas._common import BaseSchema


class CommentCreate(BaseSchema):
    """Схема для создания комментария."""

    content: str = Field(min_length=1, max_length=500)

    post_id: uuid.UUID
    user_id: uuid.UUID


class CommentResponse(CommentCreate):
    """Схема для ответа с комментарием."""

    id: uuid.UUID
    created_at: datetime


class CommentUpdate(BaseSchema):
    """Схема для обновления комментария."""

    content: str | None = Field(default=None, min_length=1, max_length=500)


class CommentDelete(BaseSchema):
    """Схема для удаления комментария."""

    id: uuid.UUID
