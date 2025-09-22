"""Эндпоинты, отвечающие за управление комментариями."""

import logging

from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError

from auth_test_task.api.dependencies import auth_dep, db_dep, read_post_dep, write_comment_dep
from auth_test_task.db.dal import CommentDAL
from auth_test_task.schemas import CommentCreate, CommentResponse, CommentUpdate

logger = logging.getLogger("auth_test_task")
router = APIRouter(
    prefix="/comments",
    tags=["Управление комментариями"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Комментарий не найден"},
    },
)


@router.post(
    "/",
    summary="Создать комментарий",
    response_description="Информация о комментарие: комментарий успешно создан",
)
async def create_comment(
    comment_info: CommentCreate,
    post: read_post_dep,
    user: auth_dep,
    db: db_dep,
) -> CommentResponse:
    try:
        comment = await CommentDAL.create(user.id, post.id, comment_info, db)
    except IntegrityError:
        logger.exception("Нарушение ограничений данных при создании комментария")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Нарушение ограничений данных")
    else:
        return CommentResponse.model_validate(comment)


@router.get(
    "/",
    summary="Получить комментарий",
    response_description="Информация о комментарие: комментарий успешно найден",
)
async def get_comment(
    comment: write_comment_dep,
) -> CommentResponse:
    return CommentResponse.model_validate(comment)


@router.patch(
    "/",
    summary="Обновить комментарий",
    response_description="Информация о комментарие: комментарий успешно обновлён",
)
async def update_comment(
    update_info: CommentUpdate,
    comment: write_comment_dep,
    db: db_dep,
) -> CommentResponse:
    try:
        comment = await CommentDAL.update(
            comment_id=comment.id,
            update_info=update_info,
            session=db,
        )
    except IntegrityError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Нарушение ограничений данных")
    else:
        return CommentResponse.model_validate(comment)


@router.delete(
    "/",
    summary="Удалить комментарий",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Пустой ответ: комментарий успешно удалён",
)
async def delete_comment(
    comment: write_comment_dep,
    db: db_dep,
) -> Response:
    try:
        await CommentDAL.drop(comment.id, db)
    except IntegrityError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Нарушение ограничений данных")
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
