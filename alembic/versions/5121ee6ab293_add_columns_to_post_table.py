"""add columns to post table

Revision ID: 5121ee6ab293
Revises: 180cd3ad2f35
Create Date: 2025-04-22 13:15:39.219488

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5121ee6ab293'
down_revision: Union[str, None] = '180cd3ad2f35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))
    op.add_column("posts", sa.Column("published", sa.Boolean, server_default='TRUE', nullable=False))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
