"""Схемы для работы с пользователями."""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import EmailStr, Field

from auth_test_task.schemas._common import BaseSchema
from auth_test_task.schemas._variables import USER_ROLES


class UserCreate(BaseSchema):
    """Схема для создания пользователя."""

    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(alias="_password", min_length=8, max_length=64)


class UserResponse(UserCreate):
    """Схема для ответа с данными пользователя."""

    id: uuid.UUID

    is_active: bool = Field(exclude=True)
    role: USER_ROLES

    created_at: datetime


class UserUpdate(BaseSchema):
    """Схема для обновления данных пользователя."""

    name: str | None = Field(default=None, min_length=2, max_length=50)
    email: EmailStr | None = None
    password: str | None = Field(default=None, alias="_password", min_length=8, max_length=64)
