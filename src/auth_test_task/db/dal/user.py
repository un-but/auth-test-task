"""Модуль для работы с пользователями в базе данных."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select

from auth_test_task.db.models import UserModel

if TYPE_CHECKING:
    import uuid
    from collections.abc import Sequence

    from sqlalchemy.ext.asyncio import AsyncSession

    from auth_test_task.schemas import UserCreate


class UserDAL:
    """Класс для работы с пользователями в базе данных."""

    @staticmethod
    async def create(user_info: UserCreate, session: AsyncSession) -> UserModel:
        user = UserModel(
            name=user_info.name,
            email=user_info.email,
            _password=user_info.password,
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user

    @staticmethod
    async def get_by_id(
        user_id: uuid.UUID,
        session: AsyncSession,
    ) -> UserModel:
        if user := await session.scalar(select(UserModel).where(UserModel.id == user_id)):
            return user

        msg = "Указанный пользователь не найден"
        raise LookupError(msg)

    @staticmethod
    async def get_with_email(
        email: str,
        session: AsyncSession,
    ) -> UserModel:
        if user := await session.scalar(select(UserModel).where(UserModel.email == email)):
            return user

        msg = "Указанный пользователь не найден"
        raise LookupError(msg)

    @staticmethod
    async def get_all(
        session: AsyncSession,
    ) -> Sequence[UserModel]:
        users = await session.scalars(select(UserModel))
        return users.all()

    @staticmethod
    async def drop(user_id: uuid.UUID, session: AsyncSession) -> None:
        user = await UserDAL.get_by_id(user_id, session)

        await session.delete(user)
        await session.commit()
