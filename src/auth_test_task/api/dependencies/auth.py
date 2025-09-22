"""Зависимости авторизации."""

from __future__ import annotations

import logging
from typing import Annotated

from fastapi import Depends, HTTPException, status

from auth_test_task.api.dependencies._common import cookies_dep, db_dep, rd_dep
from auth_test_task.api.utils import get_user_by_token
from auth_test_task.db.models import UserModel

logger = logging.getLogger("auth_test_task")


async def authorize_user(
    cookies: cookies_dep,
    db: db_dep,
    rd: rd_dep,
) -> UserModel:
    """Авторизует пользователя по токену из куки."""
    if cookies.access_token:
        return await get_user_by_token(cookies.access_token, "access", db, rd)

    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Необходима авторизация")


auth_dep = Annotated[UserModel, Depends(authorize_user)]


async def optional_authorize_user(
    cookies: cookies_dep,
    db: db_dep,
    rd: rd_dep,
) -> UserModel | None:
    """Может авторизовать пользователя, если передан токен."""
    if cookies.access_token:
        return await authorize_user(cookies, db, rd)
    return None


optional_auth_dep = Annotated[UserModel | None, Depends(optional_authorize_user)]


async def authorize_admin(user: auth_dep) -> UserModel:
    """Проверяет, что пользователь администратор."""
    if user.is_active and user.role == "admin":
        return user
    raise HTTPException(status.HTTP_403_FORBIDDEN, "Доступ запрещён")


admin_dep = Annotated[UserModel, Depends(authorize_admin)]


async def authorize_manager(user: auth_dep) -> UserModel:
    """Проверяет, что пользователь менеджер или администратор."""
    if user.is_active and user.role in {"admin", "manager"}:
        return user
    raise HTTPException(status.HTTP_403_FORBIDDEN, "Доступ запрещён")


manager_dep = Annotated[UserModel, Depends(authorize_manager)]
