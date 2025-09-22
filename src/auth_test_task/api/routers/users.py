"""Эндпоинты, отвечающие за управление всеми пользователями."""

import logging
import uuid

from fastapi import APIRouter, HTTPException, Query, Response, status
from sqlalchemy.exc import IntegrityError

from auth_test_task.api.dependencies import db_dep, manager_dep, read_user_dep, write_user_dep
from auth_test_task.db.dal import UserDAL
from auth_test_task.schemas import (
    USER_INCLUDE_TYPE,
    UserResponse,
    UserWithRoleCreate,
    UserWithRoleUpdate,
)

logger = logging.getLogger("auth_test_task")
router = APIRouter(
    prefix="/users",
    tags=["Управление всеми пользователями"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Пользователь не найден"},
    },
)


@router.post(
    "/",
    summary="Создать пользователя (с ролью)",
    response_description="Информация о пользователе: пользователь успешно создан",
)
async def create_with_role(
    user_info: UserWithRoleCreate,
    admin: manager_dep,
    db: db_dep,
) -> UserResponse:
    try:
        user = await UserDAL.create(user_info, db)
    except IntegrityError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Нарушение ограничений данных")
    else:
        return UserResponse.model_validate(user)


@router.get(
    "/{user_id}",
    summary="Получить любого пользователя",
    response_description="Информация о пользователе: пользователь успешно найден",
)
async def get_any_user(
    user: read_user_dep,
    db: db_dep,
    include: tuple[USER_INCLUDE_TYPE, ...] = Query(default=()),
) -> UserResponse:
    user = await UserDAL.get_by_id(
        user_id=user.id,
        include=include,
        session=db,
    )

    return UserResponse.model_validate(user)


@router.patch(
    "/{user_id}",
    summary="Обновить любого пользователя (с ролью)",
    response_description="Информация о пользователе: пользователь успешно обновлён",
)
async def update_any_user_with_role(
    user: write_user_dep,
    update_info: UserWithRoleUpdate,
    db: db_dep,
) -> UserResponse:
    try:
        user = await UserDAL.update(
            user_id=user.id,
            update_info=update_info,
            session=db,
        )
    except IntegrityError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Нарушение ограничений данных")
    else:
        return UserResponse.model_validate(user)


@router.delete(
    "/{user_id}",
    summary="Удалить пользователя (деактивировать)",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Пустой ответ: пользователь успешно удалён",
)
async def delete_any_user(
    user: write_user_dep,
    db: db_dep,
) -> Response:
    try:
        await UserDAL.change_active_status(user.id, False, db)
    except IntegrityError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Нарушение ограничений данных")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/{user_id}/hard",
    summary="Удалить пользователя вместе с данными",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Пустой ответ: пользователь успешно удалён",
)
async def hard_delete_any_user(
    user: write_user_dep,
    db: db_dep,
) -> Response:
    try:
        await UserDAL.drop(user.id, db)
    except IntegrityError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Нарушение ограничений данных")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
