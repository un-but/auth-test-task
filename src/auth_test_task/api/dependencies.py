"""Зависимости для FastAPI приложения."""

from __future__ import annotations

import logging
import uuid
from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, Query, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from auth_test_task.api.utils import get_user_by_token
from auth_test_task.db.connection import get_db, get_redis
from auth_test_task.db.dal import CommentDAL, PostDAL, RoleRuleDAL
from auth_test_task.db.models import CommentModel, PostModel, RoleRuleModel, UserModel
from auth_test_task.schemas import Cookies, RoleRuleGet

logger = logging.getLogger("auth_test_task")

cookies_dep = Annotated[Cookies, Cookie()]
db_dep = Annotated[AsyncSession, Depends(get_db)]
rd_dep = Annotated[Redis, Depends(get_redis)]


async def authorize_user(
    cookies: cookies_dep,
    db: db_dep,
    rd: rd_dep,
) -> UserModel:
    """Авторизует пользователя по токену из куки."""
    if cookies.access_token:
        return await get_user_by_token(cookies.access_token, "access", db, rd)

    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Необходима авторизация")


async def optional_authorize_user(
    cookies: cookies_dep,
    db: db_dep,
    rd: rd_dep,
) -> UserModel | None:
    """Может авторизовать пользователя, если передан токен."""
    if cookies.access_token:
        return await authorize_user(cookies, db, rd)
    return None


auth_dep = Annotated[UserModel, Depends(authorize_user)]
optional_auth_dep = Annotated[UserModel | None, Depends(optional_authorize_user)]


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
        if post.user_id == user.id:
            return post

        raise HTTPException(status.HTTP_403_FORBIDDEN, "Доступ запрещён")


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
        if comment.user_id == user.id:
            return comment

        raise HTTPException(status.HTTP_403_FORBIDDEN, "Доступ запрещён")


async def write_role_rule(
    db: db_dep,
    role_rule_info: RoleRuleGet = Query(...),
) -> RoleRuleModel:
    """Проверяет, что пользователь может менять правило роли."""
    try:
        role_rule = await RoleRuleDAL.get(role_rule_info, db)
    except LookupError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Правило роли не найдено")
    else:
        return role_rule


write_post_dep = Annotated[PostModel, Depends(write_access_post)]
read_post_dep = Annotated[PostModel, Depends(read_access_post)]

write_comment_dep = Annotated[CommentModel, Depends(write_access_comment)]
write_role_rule_dep = Annotated[RoleRuleModel, Depends(write_role_rule)]
