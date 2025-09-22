"""Схемы для работы с постами."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import Field

from auth_test_task.schemas._common import BaseSchema


class PostCreate(BaseSchema):
    """Схема для создания поста."""

    content: str = Field(min_length=1, max_length=1000)
    user_id: uuid.UUID


class PostResponse(PostCreate):
    """Схема для ответа с постом."""

    id: uuid.UUID
    created_at: datetime


class PostUpdate(BaseSchema):
    """Схема для обновления поста."""

    content: str | None = Field(default=None, min_length=1, max_length=1000)


class PostDelete(BaseSchema):
    """Схема для удаления поста."""

    id: uuid.UUID
