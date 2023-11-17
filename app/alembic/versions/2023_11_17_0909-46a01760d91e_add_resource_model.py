"""
add resource model

Revision ID: 46a01760d91e
Revises: 17b4755d875f
Create Date: 2023-11-17 09:09:27.650526+00:00
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# Revision identifiers, used by Alembic
revision: str = "46a01760d91e"
down_revision: str | None = "17b4755d875f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "resource_pool_resource",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column("resource_id", sa.String(length=255), nullable=False),
        sa.Column("href", sa.String(length=255), nullable=False),
        sa.Column("resource_pool_capacity_id", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["resource_pool_capacity_id"],
            ["resource_pool_capacity.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_resource_pool_resource_id"),
        "resource_pool_resource",
        ["id"],
        unique=False,
    )
    op.alter_column(
        "external_party_characteristics",
        "ipam_description",
        existing_type=sa.VARCHAR(length=255),
        nullable=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "external_party_characteristics",
        "ipam_description",
        existing_type=sa.VARCHAR(length=255),
        nullable=False,
    )
    op.drop_index(
        op.f("ix_resource_pool_resource_id"), table_name="resource_pool_resource"
    )
    op.drop_table("resource_pool_resource")
    # ### end Alembic commands ###