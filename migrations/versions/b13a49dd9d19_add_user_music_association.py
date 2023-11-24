"""Add user-music association

Revision ID: b13a49dd9d19
Revises: becab35d073f
Create Date: 2023-11-16 10:14:08.913030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b13a49dd9d19'
down_revision = 'becab35d073f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_music',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('music_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['music_id'], ['music.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'music_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_music')
    # ### end Alembic commands ###