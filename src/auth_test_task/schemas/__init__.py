"""Модуль включающий в себя все схемы. Для доступа следует импортировать все из этого модуля."""

# pyright: reportUnusedImport=false
# ruff: noqa: F401, RUF100

from __future__ import annotations

from auth_test_task.schemas._common import BaseSchema, NoContentSchema
from auth_test_task.schemas._configuration import config
from auth_test_task.schemas._variables import (
    ACTION_TYPES,
    MAX_PASSWORD_LENGTH,
    MIN_PASSWORD_LENGTH,
    OBJECT_TYPES,
    USER_ROLES,
)
from auth_test_task.schemas.auth import AuthResponse, AuthWithEmail, Cookies
from auth_test_task.schemas.user import UserCreate, UserResponse, UserUpdate
