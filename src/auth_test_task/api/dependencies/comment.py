"""Зависимости объектов комментариев."""

from __future__ import annotations

import logging
import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, status

from auth_test_task.api.dependencies._common import db_dep
from auth_test_task.api.dependencies.auth import auth_dep
from auth_test_task.db.dal import CommentDAL
from auth_test_task.db.models import CommentModel

logger = logging.getLogger("auth_test_task")


async def write_access_comment(
    comment_id: uuid.UUID,
    user: auth_dep,
    db: db_dep,
) -> CommentModel:
    """Проверяет, что комментарий принадлежит пользователю."""
    try:
        comment = await CommentDAL.get_by_id(comment_id, db)
    except LookupError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Комментарий не найден")
    else:
        if comment.user_id == user.id or user.role in {"admin", "manager"}:
            return comment

        raise HTTPException(status.HTTP_403_FORBIDDEN, "Доступ запрещён")


write_comment_dep = Annotated[CommentModel, Depends(write_access_comment)]


async def read_access_comment(
    comment_id: uuid.UUID,
    db: db_dep,
) -> CommentModel:
    """Проверяет доступ к комментарию для чтения."""
    try:
        comment = await CommentDAL.get_by_id(comment_id, db)
    except LookupError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Комментарий не найден")
    else:
        return comment


read_comment_dep = Annotated[CommentModel, Depends(read_access_comment)]
