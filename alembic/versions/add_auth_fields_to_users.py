"""add authentication fields to users

Revision ID: a1b2c3d4e5f6
Revises: fcfcf24cfcd6
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'a1b2c3d4e5f6'
down_revision = 'fcfcf24cfcd6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Agregar columna hashed_password (nullable para compatibilidad con datos existentes)
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hashed_password', sa.String(length=255), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('hashed_password')
