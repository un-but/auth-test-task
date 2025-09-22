"""Зависимости объектов пользователей."""

from __future__ import annotations

import logging
import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, status

from auth_test_task.api.dependencies._common import db_dep
from auth_test_task.api.dependencies.auth import manager_dep
from auth_test_task.db.dal import UserDAL
from auth_test_task.db.models import UserModel

logger = logging.getLogger("auth_test_task")


async def write_access_user(
    user_id: uuid.UUID,
    admin: manager_dep,
    db: db_dep,
) -> UserModel:
    """Проверяет, что пользователь может менять данные другого пользователя."""
    try:
        user = await UserDAL.get_by_id(user_id, db)
    except LookupError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Пользователь не найден")
    else:
        if user.role in {"admin", "manager"}:
            return user

        raise HTTPException(status.HTTP_403_FORBIDDEN, "Доступ запрещён")


write_user_dep = Annotated[UserModel, Depends(write_access_user)]


async def read_access_user(
    user_id: uuid.UUID,
    admin: manager_dep,
    db: db_dep,
) -> UserModel:
    """Проверяет доступ к данным пользователя для чтения."""
    try:
        user = await UserDAL.get_by_id(user_id, db)
    except LookupError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Пользователь не найден")
    else:
        return user


read_user_dep = Annotated[UserModel, Depends(read_access_user)]
