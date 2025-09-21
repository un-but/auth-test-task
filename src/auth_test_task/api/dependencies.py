"""Зависимости для FastAPI приложения."""

from __future__ import annotations

import logging
from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from auth_test_task.api.utils import get_user_by_token
from auth_test_task.db.connection import get_db, get_redis
from auth_test_task.db.models import UserModel
from auth_test_task.schemas import Cookies

logger = logging.getLogger("auth_test_task")

cookies_dep = Annotated[Cookies, Cookie()]
db_dep = Annotated[AsyncSession, Depends(get_db)]
rd_dep = Annotated[Redis, Depends(get_redis)]


async def authorize_user(
    cookies: cookies_dep,
    db: db_dep,
    rd: rd_dep,
) -> UserModel:
    if cookies.access_token:
        return await get_user_by_token(cookies.access_token, "access", db, rd)

    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Необходима авторизация")


async def optional_authorize_user(
    cookies: cookies_dep,
    db: db_dep,
    rd: rd_dep,
) -> UserModel | None:
    if cookies.access_token:
        return await authorize_user(cookies, db, rd)
    return None


user_dep = Annotated[UserModel, Depends(authorize_user)]
optional_user_dep = Annotated[UserModel | None, Depends(optional_authorize_user)]
