"""Модуль для работы с правилами ролей пользователей в базе данных."""

from __future__ import annotations

import uuid
from collections.abc import Sequence
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from auth_test_task.db.models import RoleRuleModel

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.sql.base import ExecutableOption


class RoleRuleDAL:
    """Класс для работы с правилами ролей пользователей в базе данных."""
