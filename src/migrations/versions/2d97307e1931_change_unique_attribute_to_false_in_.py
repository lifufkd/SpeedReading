"""change unique attribute to false in 'email' field in 'users' table

Revision ID: 2d97307e1931
Revises: 8297126562e4
Create Date: 2025-06-24 23:38:57.944017

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d97307e1931'
down_revision: Union[str, Sequence[str], None] = '8297126562e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint("users_email_key", "users", type_="unique")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_unique_constraint("users_email_key", "users", ["email"])