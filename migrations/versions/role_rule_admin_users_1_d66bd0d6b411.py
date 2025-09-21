"""Role rule admin users 1.

ID миграции: d66bd0d6b411
Изменяет: 8af847b54434
Дата создания: 21:12:58 21.09.2025 по МСК
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# Идентификаторы миграции, используются Alembic.
revision: str = "d66bd0d6b411"
down_revision: str | None = "8af847b54434"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Таблица правил для ролей
    role_rules = sa.table(
        "role_rules",
        sa.column("role", sa.String),
        sa.column("object_type", sa.String),
        sa.column("action", sa.String),
        sa.column("allowed", sa.Boolean),
    )

    # Добавление правил для роли 'admin' и объекта 'users'
    rules = [
        {"role": "admin", "object_type": "users", "action": "create", "allowed": True},
        {"role": "admin", "object_type": "users", "action": "read", "allowed": True},
        {"role": "admin", "object_type": "users", "action": "update", "allowed": True},
        {"role": "admin", "object_type": "users", "action": "delete", "allowed": True},
    ]

    op.bulk_insert(role_rules, rules)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        DELETE FROM role_rules
        WHERE role = 'admin' AND object_type = 'users'
        """
    )
