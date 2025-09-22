"""Схемы для работы с правилами ролей пользователя."""

from __future__ import annotations

from auth_test_task.schemas._common import BaseSchema
from auth_test_task.schemas._variables import ACTION_TYPES, OBJECT_TYPES, USER_ROLES


class RoleRuleBase(BaseSchema):
    """Базовая схема правила роли пользователя."""

    role: USER_ROLES
    object_type: OBJECT_TYPES
    action: ACTION_TYPES


class RoleRuleGet(RoleRuleBase):
    """Схема получения правила роли пользователя."""


class RoleRuleCreate(RoleRuleBase):
    """Схема создания правила роли пользователя."""

    allowed: bool


class RoleRuleResponse(RoleRuleCreate):
    """Схема ответа с информацией о правиле роли пользователя."""


class RoleRuleUpdate(BaseSchema):
    """Схема обновления правила роли пользователя."""

    role: USER_ROLES | None = None
    object_type: OBJECT_TYPES | None = None
    action: ACTION_TYPES | None = None
    allowed: bool | None = None


class RoleRuleDelete(RoleRuleGet):
    """Схема удаления правила роли пользователя."""
