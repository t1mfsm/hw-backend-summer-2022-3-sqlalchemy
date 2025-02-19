"""Added column for quesion and answer models 2.0

Revision ID: e653da630fd3
Revises: 8e224229122c
Create Date: 2024-04-23 03:18:06.300291

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e653da630fd3'
down_revision: Union[str, None] = '8e224229122c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answers', sa.Column('title', sa.String(), nullable=False))
    op.drop_constraint('answers_answer_key', 'answers', type_='unique')
    op.create_unique_constraint(None, 'answers', ['title'])
    op.drop_column('answers', 'answer')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answers', sa.Column('answer', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'answers', type_='unique')
    op.create_unique_constraint('answers_answer_key', 'answers', ['answer'])
    op.drop_column('answers', 'title')
    # ### end Alembic commands ###
