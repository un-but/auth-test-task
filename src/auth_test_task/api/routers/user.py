"""Эндпоинты, отвечающие за управление пользователем."""

import logging
from typing import Literal

from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError

from auth_test_task.api.dependencies import db_dep, user_dep
from auth_test_task.db.dal import UserDAL
from auth_test_task.schemas import UserCreate, UserResponse, UserUpdate

logger = logging.getLogger("auth_test_task")
router = APIRouter(
    prefix="/user",
    tags=["Управление пользователем"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Пользователь не найден"},
        status.HTTP_400_BAD_REQUEST: {"description": "Нарушение ограничений полей в базе данных"},
    },
)


@router.post(
    "/",
    summary="Создать пользователя",
    response_description="Информация о пользователе: пользователь успешно создан",
)
async def create_user(
    user_info: UserCreate,
    db: db_dep,
) -> UserResponse:
    try:
        user = await UserDAL.create(user_info, db)
    except IntegrityError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Нарушение ограничений данных")
    else:
        return UserResponse.model_validate(user)


@router.get(
    "/",
    summary="Получить пользователя",
    response_description="Информация о пользователе: пользователь успешно найден",
)
async def get_user(
    user: user_dep,
    db: db_dep,
) -> UserResponse:
    try:
        user = await UserDAL.get_by_id(
            user_id=user.id,
            session=db,
        )
    except LookupError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Пользователь не найден")
    else:
        return UserResponse.model_validate(user)


@router.patch(
    "/",
    summary="Обновить пользователя",
    response_description="Информация о пользователе: пользователь успешно обновлён",
)
async def update_user(
    user_info: UserUpdate,
    user: user_dep,
    db: db_dep,
) -> UserResponse:
    try:
        user = await UserDAL.update(
            user_id=user.id,
            user_info=user_info,
            session=db,
        )
    except IntegrityError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Нарушение ограничений данных")
    else:
        return UserResponse.model_validate(user)


@router.delete(
    "/",
    summary="Удалить пользователя",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Пустой ответ: пользователь успешно удалён",
)
async def delete_user(
    user: user_dep,
    db: db_dep,
) -> Response:
    try:
        await UserDAL.drop(user.id, db)
    except LookupError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Пользователь не найден")
    except IntegrityError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Нарушение целостности данных")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
