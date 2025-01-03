"""init tables

Revision ID: 645a3bcf967c
Revises:
Create Date: 2024-12-20 22:46:40.181750

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "645a3bcf967c"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "breeds",
        sa.Column(
            "breed_id",
            sa.BigInteger(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("breed_name", sa.String(length=50), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("breed_id", name=op.f("pk_breeds")),
        sa.UniqueConstraint("breed_name", name=op.f("uq_breeds_breed_name")),
    )
    op.create_table(
        "cats",
        sa.Column(
            "cat_id",
            sa.BigInteger(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("cat_age", sa.Integer(), nullable=False),
        sa.Column("cat_color", sa.String(length=50), nullable=False),
        sa.Column("cat_description", sa.String(length=1000), nullable=False),
        sa.Column("breed_id", sa.BigInteger(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["breed_id"],
            ["breeds.breed_id"],
            name=op.f("fk_cats_breed_id_breeds"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("cat_id", name=op.f("pk_cats")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("cats")
    op.drop_table("breeds")
    # ### end Alembic commands ###
