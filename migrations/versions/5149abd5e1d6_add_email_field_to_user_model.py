"""Add email field to User model

Revision ID: 5149abd5e1d6
Revises: 8a3176fe5023
Create Date: 2023-11-22 10:32:27.263938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5149abd5e1d6'
down_revision = '8a3176fe5023'
branch_labels = None
depends_on = None


def upgrade():
    # Add the 'email' column to the 'user' table
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=120), nullable=False))
    
    # Create a unique constraint on the 'email' column
    op.create_unique_constraint('user_email_key', 'user', ['email'])

    # Drop the 'new_username' and 'new_password_hash' columns
    op.drop_column('user', 'new_username')
    op.drop_column('user', 'new_password_hash')


def downgrade():
    # Add the 'new_password_hash' and 'new_username' columns back
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('new_password_hash', sa.VARCHAR(length=128), nullable=True))
        batch_op.add_column(sa.Column('new_username', sa.VARCHAR(length=80), nullable=True))
    
    # Drop the unique constraint on the 'email' column
    op.drop_constraint('user_email_key', 'user', type_='unique')
    
    # Drop the 'email' column
    op.drop_column('user', 'email')
