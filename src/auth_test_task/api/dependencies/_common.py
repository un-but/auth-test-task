"""Общие зависимости для FastAPI зависимостей или эндпоинтов."""

from typing import Annotated

from fastapi import Cookie, Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from auth_test_task.db.connection import get_db, get_redis
from auth_test_task.schemas import Cookies

cookies_dep = Annotated[Cookies, Cookie()]
db_dep = Annotated[AsyncSession, Depends(get_db)]
rd_dep = Annotated[Redis, Depends(get_redis)]
