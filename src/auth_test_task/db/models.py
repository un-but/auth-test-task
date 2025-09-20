"""Модели SQLAlchemy ORM."""

from __future__ import annotations

import pkgutil
import re
import uuid
from datetime import datetime
from typing import Literal

from sqlalchemy import BigInteger, ForeignKey, String, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
    validates,
)

rename_pattern = re.compile(r"(?<!^)(?=[A-Z])")
source_statuses = Literal["success", "fail", "in_progress", "in_queue", "partial_success"]


class Base(DeclarativeBase):
    """Базовый класс для моделей SQLAlchemy.

    Автоматически генерирует имя таблицы в snake_case во множественном числе.
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Генерирует имя таблицы из имени класса."""
        class_name = re.sub(
            rename_pattern,
            "_",
            cls.__name__.replace("Model", ""),
        ).lower()
        return class_name + "s" if class_name[-1] != "y" else class_name[:-1] + "ies"
