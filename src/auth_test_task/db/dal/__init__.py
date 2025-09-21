"""Модуль для работы с моделями ORM. Рекомендую импортировать напрямую из этого модуля модели."""

# pyright: reportUnusedImport=false
# ruff: noqa: F401, RUF100

from __future__ import annotations

from auth_test_task.db.dal.comment import CommentDAL
from auth_test_task.db.dal.post import PostDAL
from auth_test_task.db.dal.role_rule import RoleRuleDAL
from auth_test_task.db.dal.user import UserDAL
