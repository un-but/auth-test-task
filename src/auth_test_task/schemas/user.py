"""Схемы для работы с пользователями."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import field_validator

from auth_test_task.schemas._common import BaseSchema

if TYPE_CHECKING:  # Требуется для корректной работы отложенного импорта
    ...
