"""
Intial

Revision ID: 2c15792750b5
Revises: 
Create Date: 2023-10-18 16:31:30.260279+00:00
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# Revision identifiers, used by Alembic
revision: str = "2c15792750b5"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "reservation",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column("href", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(length=255), nullable=True),
        sa.Column("reservation_state", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_reservation_id"), "reservation", ["id"], unique=False)
    op.create_table(
        "resource_pool_management",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column("href", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_resource_pool_management_id"),
        "resource_pool_management",
        ["id"],
        unique=False,
    )
    op.create_table(
        "capacity",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("capacity_amount", sa.Integer(), nullable=False),
        sa.Column("capacity_amount_from", sa.String(length=255), nullable=False),
        sa.Column("capacity_amount_to", sa.String(length=255), nullable=False),
        sa.Column("resource_pool_id", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["resource_pool_id"],
            ["resource_pool_management.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_capacity_id"), "capacity", ["id"], unique=False)
    op.create_table(
        "reservation_item",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("sub_reservation_state", sa.String(length=255), nullable=False),
        sa.Column("reservation_id", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["reservation_id"],
            ["reservation.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_reservation_item_id"), "reservation_item", ["id"], unique=False
    )
    op.create_table(
        "reservation_related_party",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=255), nullable=True),
        sa.Column("reservation_id", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["reservation_id"],
            ["reservation.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_reservation_related_party_id"),
        "reservation_related_party",
        ["id"],
        unique=False,
    )
    op.create_table(
        "valid_for",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reservation_id", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["reservation_id"],
            ["reservation.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_valid_for_id"), "valid_for", ["id"], unique=False)
    op.create_table(
        "applied_capacity_amount",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column("applied_capacity_amount", sa.String(length=255), nullable=False),
        sa.Column("reservation_item_id", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["reservation_item_id"],
            ["reservation_item.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_applied_capacity_amount_id"),
        "applied_capacity_amount",
        ["id"],
        unique=False,
    )
    op.create_table(
        "reservation_resource_capacity",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(length=255), nullable=False),
        sa.Column("capacity_demand_amount", sa.String(length=255), nullable=False),
        sa.Column("reservation_item_id", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["reservation_item_id"],
            ["reservation_item.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_reservation_resource_capacity_id"),
        "reservation_resource_capacity",
        ["id"],
        unique=False,
    )
    op.create_table(
        "resource_place",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(length=255), nullable=False),
        sa.Column("capacity_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["capacity_id"],
            ["capacity.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_resource_place_id"), "resource_place", ["id"], unique=False
    )
    op.create_table(
        "resource_related_party",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=255), nullable=False),
        sa.Column("capacity_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["capacity_id"],
            ["capacity.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_resource_related_party_id"),
        "resource_related_party",
        ["id"],
        unique=False,
    )
    op.create_table(
        "reservation_applicable_time_period",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column("is_from", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "reservation_resource_capacity_id", sa.String(length=255), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["reservation_resource_capacity_id"],
            ["reservation_resource_capacity.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_reservation_applicable_time_period_id"),
        "reservation_applicable_time_period",
        ["id"],
        unique=False,
    )
    op.create_table(
        "reservation_place",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(length=255), nullable=False),
        sa.Column(
            "reservation_resource_capacity_id", sa.String(length=255), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["reservation_resource_capacity_id"],
            ["reservation_resource_capacity.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_reservation_place_id"), "reservation_place", ["id"], unique=False
    )
    op.create_table(
        "reservation_resource",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column("referred_type", sa.String(length=255), nullable=False),
        sa.Column("href", sa.String(length=255), nullable=False),
        sa.Column("resource_id", sa.String(length=255), nullable=False),
        sa.Column("applied_capacity_amount_id", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["applied_capacity_amount_id"],
            ["applied_capacity_amount.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_reservation_resource_id"), "reservation_resource", ["id"], unique=False
    )
    op.create_table(
        "reservation_resource_pool",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column("pool_id", sa.String(length=255), nullable=False),
        sa.Column("href", sa.String(length=255), nullable=False),
        sa.Column(
            "reservation_resource_capacity_id", sa.String(length=255), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["reservation_resource_capacity_id"],
            ["reservation_resource_capacity.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_reservation_resource_pool_id"),
        "reservation_resource_pool",
        ["id"],
        unique=False,
    )
    op.create_table(
        "characteristic",
        sa.Column("id", sa.String(length=255), nullable=False),
        sa.Column("ipv4_subnet", sa.String(length=255), nullable=False),
        sa.Column("resource_id", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["resource_id"],
            ["reservation_resource.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_characteristic_id"), "characteristic", ["id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_characteristic_id"), table_name="characteristic")
    op.drop_table("characteristic")
    op.drop_index(
        op.f("ix_reservation_resource_pool_id"), table_name="reservation_resource_pool"
    )
    op.drop_table("reservation_resource_pool")
    op.drop_index(op.f("ix_reservation_resource_id"), table_name="reservation_resource")
    op.drop_table("reservation_resource")
    op.drop_index(op.f("ix_reservation_place_id"), table_name="reservation_place")
    op.drop_table("reservation_place")
    op.drop_index(
        op.f("ix_reservation_applicable_time_period_id"),
        table_name="reservation_applicable_time_period",
    )
    op.drop_table("reservation_applicable_time_period")
    op.drop_index(
        op.f("ix_resource_related_party_id"), table_name="resource_related_party"
    )
    op.drop_table("resource_related_party")
    op.drop_index(op.f("ix_resource_place_id"), table_name="resource_place")
    op.drop_table("resource_place")
    op.drop_index(
        op.f("ix_reservation_resource_capacity_id"),
        table_name="reservation_resource_capacity",
    )
    op.drop_table("reservation_resource_capacity")
    op.drop_index(
        op.f("ix_applied_capacity_amount_id"), table_name="applied_capacity_amount"
    )
    op.drop_table("applied_capacity_amount")
    op.drop_index(op.f("ix_valid_for_id"), table_name="valid_for")
    op.drop_table("valid_for")
    op.drop_index(
        op.f("ix_reservation_related_party_id"), table_name="reservation_related_party"
    )
    op.drop_table("reservation_related_party")
    op.drop_index(op.f("ix_reservation_item_id"), table_name="reservation_item")
    op.drop_table("reservation_item")
    op.drop_index(op.f("ix_capacity_id"), table_name="capacity")
    op.drop_table("capacity")
    op.drop_index(
        op.f("ix_resource_pool_management_id"), table_name="resource_pool_management"
    )
    op.drop_table("resource_pool_management")
    op.drop_index(op.f("ix_reservation_id"), table_name="reservation")
    op.drop_table("reservation")
    # ### end Alembic commands ###
