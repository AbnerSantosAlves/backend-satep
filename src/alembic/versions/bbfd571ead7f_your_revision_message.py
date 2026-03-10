"""Your revision message

Revision ID: bbfd571ead7f
Revises: 726bcd3747df
Create Date: 2025-10-11 17:34:44.100299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bbfd571ead7f'
down_revision: Union[str, Sequence[str], None] = '726bcd3747df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
