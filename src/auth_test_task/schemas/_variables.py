"""Общие переменные и типы для схем приложения."""

from __future__ import annotations

from typing import Literal

USER_ROLES = Literal["user", "admin", "manager"]
OBJECT_TYPES = Literal["users", "posts", "comments"]
ACTION_TYPES = Literal["create", "read", "update", "delete"]
