"""Зависимости для FastAPI приложения."""

# pyright: reportUnusedImport=false
# ruff: noqa: F401, RUF100

from __future__ import annotations

from auth_test_task.api.dependencies._common import cookies_dep, db_dep, rd_dep
from auth_test_task.api.dependencies.auth import (
    admin_dep,
    auth_dep,
    manager_dep,
    optional_auth_dep,
)
from auth_test_task.api.dependencies.comment import read_comment_dep, write_comment_dep
from auth_test_task.api.dependencies.post import read_post_dep, write_post_dep
from auth_test_task.api.dependencies.role_rule import read_role_rule_dep, write_role_rule_dep
from auth_test_task.api.dependencies.user import read_user_dep, write_user_dep
