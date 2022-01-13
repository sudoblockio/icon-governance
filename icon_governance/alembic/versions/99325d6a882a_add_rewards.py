"""add rewards

Revision ID: 99325d6a882a
Revises: f63d08ae31ae
Create Date: 2022-01-12 18:49:19.715883

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "99325d6a882a"
down_revision = "f63d08ae31ae"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "rewards",
        sa.Column("tx_hash", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("address", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("block", sa.Integer(), nullable=True),
        sa.Column("timestamp", sa.Integer(), nullable=True),
        sa.Column("value", sa.Numeric(precision=10, scale=3), nullable=True),
        sa.Column("iscore", sa.Numeric(precision=13, scale=3), nullable=True),
        sa.PrimaryKeyConstraint("tx_hash"),
    )
    op.create_index(op.f("ix_rewards_address"), "rewards", ["address"], unique=False)
    op.create_index(op.f("ix_rewards_block"), "rewards", ["block"], unique=False)
    op.create_index(op.f("ix_rewards_iscore"), "rewards", ["iscore"], unique=False)
    op.create_index(op.f("ix_rewards_timestamp"), "rewards", ["timestamp"], unique=False)
    op.create_index(op.f("ix_rewards_tx_hash"), "rewards", ["tx_hash"], unique=False)
    op.create_index(op.f("ix_rewards_value"), "rewards", ["value"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_rewards_value"), table_name="rewards")
    op.drop_index(op.f("ix_rewards_tx_hash"), table_name="rewards")
    op.drop_index(op.f("ix_rewards_timestamp"), table_name="rewards")
    op.drop_index(op.f("ix_rewards_iscore"), table_name="rewards")
    op.drop_index(op.f("ix_rewards_block"), table_name="rewards")
    op.drop_index(op.f("ix_rewards_address"), table_name="rewards")
    op.drop_table("rewards")
    # ### end Alembic commands ###
