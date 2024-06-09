"""add help field to taks model

Revision ID: aba17ee79d05
Revises: c4f916028966
Create Date: 2024-06-07 02:31:13.974001

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aba17ee79d05'
down_revision: Union[str, None] = 'c4f916028966'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activity_task', sa.Column('is_running', sa.Boolean(), server_default='False', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('activity_task', 'is_running')
    # ### end Alembic commands ###
