"""add unique constraint to user

Revision ID: 6403e3a6f43a
Revises: 41da74acae98
Create Date: 2025-02-27 00:51:43.759399

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6403e3a6f43a"
down_revision: Union[str, None] = "41da74acae98"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
