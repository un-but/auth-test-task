"""Общие переменные и типы для схем приложения."""

from __future__ import annotations

from typing import Literal

USER_ROLES = Literal["user", "admin", "manager"]
OBJECT_TYPES = Literal["role_rules", "users", "posts", "comments"]
ACTION_TYPES = Literal["create", "read", "update", "delete"]

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 64

USER_INCLUDE_TYPE = Literal["posts", "comments"]
