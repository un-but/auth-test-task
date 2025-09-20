"""Зависимости для FastAPI приложения."""

from __future__ import annotations

import logging
import uuid
from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, Path, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from auth_test_task.api.utils import check_admin_token, get_user_by_token
from auth_test_task.db.connection import get_db, get_redis
from auth_test_task.db.dal import AssistantDAL, SourceDAL, ThreadDAL
from auth_test_task.db.models import AssistantModel, SourceModel, ThreadModel, UserModel
from auth_test_task.schemas import Cookies, config

logger = logging.getLogger("auth_test_task")

# Пример
# cookies_dep = Annotated[Cookies, Cookie()]
