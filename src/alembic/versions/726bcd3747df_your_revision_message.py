"""Your revision message

Revision ID: 726bcd3747df
Revises: f493da3054bb
Create Date: 2025-10-11 17:34:33.759994

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '726bcd3747df'
down_revision: Union[str, Sequence[str], None] = 'f493da3054bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
