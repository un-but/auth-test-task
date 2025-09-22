"""Схемы для работы с правилами ролей пользователя."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import field_validator

from auth_test_task.schemas._common import BaseSchema
from auth_test_task.schemas._variables import ACTION_TYPES, OBJECT_TYPES, USER_ROLES

if TYPE_CHECKING:  # Требуется для корректной работы отложенного импорта
    ...


class RoleRuleBase(BaseSchema):
    """Базовая схема правила роли пользователя."""

    role: ACTION_TYPES
    object_type: OBJECT_TYPES
    action: USER_ROLES


class RoleRuleGet(RoleRuleBase):
    """Схема получения правила роли пользователя."""


class RoleRuleCreate(RoleRuleBase):
    """Схема создания правила роли пользователя."""

    allowed: bool


class RoleRuleResponse(RoleRuleCreate):
    """Схема ответа с информацией о правиле роли пользователя."""


class RoleRuleUpdate(BaseSchema):
    """Схема обновления правила роли пользователя."""

    role: ACTION_TYPES | None = None
    object_type: OBJECT_TYPES | None = None
    action: USER_ROLES | None = None
    allowed: bool | None = None


class RoleRuleDelete(RoleRuleGet):
    """Схема удаления правила роли пользователя."""
