"""Зависимости объектов правил ролей."""

from __future__ import annotations

import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Query, status

from auth_test_task.api.dependencies._common import db_dep
from auth_test_task.api.dependencies.auth import auth_dep
from auth_test_task.db.dal import RoleRuleDAL
from auth_test_task.db.models import RoleRuleModel
from auth_test_task.schemas import ACTION_TYPE, OBJECT_TYPE, USER_ROLE, RoleRuleGet

logger = logging.getLogger("auth_test_task")


async def write_role_rule(
    user: auth_dep,
    db: db_dep,
    role_rule_info: RoleRuleGet = Query(...),
) -> RoleRuleModel:
    """Проверяет, что пользователь может менять правило роли."""
    try:
        role_rule = await RoleRuleDAL.get(role_rule_info, db)
    except LookupError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Правило роли не найдено")
    else:
        if user.role == "admin":
            return role_rule

        raise HTTPException(status.HTTP_403_FORBIDDEN, "Доступ запрещён")


write_role_rule_dep = Annotated[RoleRuleModel, Depends(write_role_rule)]


async def read_access_role_rule(
    role: USER_ROLE,
    object_type: OBJECT_TYPE,
    action: ACTION_TYPE,
    db: db_dep,
) -> RoleRuleModel:
    """Проверяет доступ к правилу роли для чтения."""
    role_rule_info = RoleRuleGet(role=role, object_type=object_type, action=action)

    try:
        role_rule = await RoleRuleDAL.get(role_rule_info, db)
    except LookupError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Правило роли не найдено")
    else:
        return role_rule


read_role_rule_dep = Annotated[RoleRuleModel, Depends(read_access_role_rule)]
