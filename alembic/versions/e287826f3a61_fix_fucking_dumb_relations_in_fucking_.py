"""fix fucking dumb relations in fucking db schema

Revision ID: e287826f3a61
Revises: aba17ee79d05
Create Date: 2024-06-07 02:54:38.767428

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e287826f3a61'
down_revision: Union[str, None] = 'aba17ee79d05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activity_task', sa.Column('activity_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'activity_task', 'activity', ['activity_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'activity_task', type_='foreignkey')
    op.drop_column('activity_task', 'activity_id')
    # ### end Alembic commands ###
