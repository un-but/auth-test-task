"""Зависимости объектов пользователей."""

from __future__ import annotations

import logging
import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, status

from auth_test_task.api.dependencies._common import db_dep
from auth_test_task.api.dependencies.auth import auth_dep
from auth_test_task.db.dal import UserDAL
from auth_test_task.db.models import UserModel

logger = logging.getLogger("auth_test_task")


async def write_access_user(
    user_id: uuid.UUID,
    user: auth_dep,
    db: db_dep,
) -> UserModel:
    """Проверяет, что пользователь может менять данные другого пользователя."""
    try:
        target_user = await UserDAL.get_by_id(user_id, db)
    except LookupError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Пользователь не найден")
    else:
        if target_user.id == user.id or user.role in {"admin", "manager"}:
            return target_user

        raise HTTPException(status.HTTP_403_FORBIDDEN, "Доступ запрещён")


write_user_dep = Annotated[UserModel, Depends(write_access_user)]


async def read_access_user(
    user_id: uuid.UUID,
    db: db_dep,
) -> UserModel:
    """Проверяет доступ к данным пользователя для чтения."""
    try:
        target_user = await UserDAL.get_by_id(user_id, db)
    except LookupError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Пользователь не найден")
    else:
        return target_user


read_user_dep = Annotated[UserModel, Depends(read_access_user)]
