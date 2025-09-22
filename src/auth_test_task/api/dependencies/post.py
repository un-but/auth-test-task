"""Зависимости объектов постов."""

from __future__ import annotations

import logging
import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, status

from auth_test_task.api.dependencies._common import db_dep
from auth_test_task.api.dependencies.auth import auth_dep
from auth_test_task.db.dal import PostDAL
from auth_test_task.db.models import PostModel

logger = logging.getLogger("auth_test_task")


async def write_access_post(
    post_id: uuid.UUID,
    user: auth_dep,
    db: db_dep,
) -> PostModel:
    """Проверяет, что пост принадлежит пользователю."""
    try:
        post = await PostDAL.get_by_id(post_id, db)
    except LookupError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Пост не найден")
    else:
        if post.user_id == user.id or user.role in {"admin", "manager"}:
            return post

        raise HTTPException(status.HTTP_403_FORBIDDEN, "Доступ запрещён")


write_post_dep = Annotated[PostModel, Depends(write_access_post)]


async def read_access_post(
    post_id: uuid.UUID,
    db: db_dep,
) -> PostModel:
    """Проверяет доступ к посту для чтения."""
    try:
        post = await PostDAL.get_by_id(post_id, db)
    except LookupError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Пост не найден")
    else:
        return post


read_post_dep = Annotated[PostModel, Depends(read_access_post)]
