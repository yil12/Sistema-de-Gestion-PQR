"""crear permisos y relacion rol permiso

Revision ID: d5f8611fec15
Revises: fb23dd797b45
Create Date: 2026-09-14

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d5f8611fec15"
down_revision: Union[str, Sequence[str], None] = "fb23dd797b45"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "permiso",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nombre"),
    )

    op.create_table(
        "rol_permiso",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("rol_id", sa.Integer(), nullable=False),
        sa.Column("permiso_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["permiso_id"], ["permiso.id"]),
        sa.ForeignKeyConstraint(["rol_id"], ["rol.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("rol_permiso")
    op.drop_table("permiso")