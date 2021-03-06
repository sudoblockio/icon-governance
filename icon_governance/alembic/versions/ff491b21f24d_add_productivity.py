"""add productivity

Revision ID: ff491b21f24d
Revises: 92b906e51bf3
Create Date: 2021-10-08 16:40:49.829048

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "ff491b21f24d"
down_revision = "92b906e51bf3"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "preps",
        sa.Column("address", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("country", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("city", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("website", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("details", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("p2p_endpoint", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("node_address", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("status", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("penalty", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("grade", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("last_updated_block", sa.Integer(), nullable=True),
        sa.Column("last_updated_timestamp", sa.Integer(), nullable=True),
        sa.Column("created_block", sa.Integer(), nullable=True),
        sa.Column("created_timestamp", sa.Integer(), nullable=True),
        sa.Column("logo_256", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("logo_1024", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("logo_svg", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("steemit", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("twitter", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("youtube", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("facebook", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("github", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("reddit", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("keybase", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("telegram", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("wechat", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("api_endpoint", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("server_country", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("server_city", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("server_type", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("voted", sa.Float(), nullable=True),
        sa.Column("voting_power", sa.Float(), nullable=True),
        sa.Column("delegated", sa.Float(), nullable=True),
        sa.Column("stake", sa.Float(), nullable=True),
        sa.Column("irep", sa.Float(), nullable=True),
        sa.Column("irep_updated_block_height", sa.Float(), nullable=True),
        sa.Column("total_blocks", sa.Float(), nullable=True),
        sa.Column("validated_blocks", sa.Float(), nullable=True),
        sa.Column("unvalidated_sequence_blocks", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("address"),
    )
    op.create_index(op.f("ix_preps_address"), "preps", ["address"], unique=False)
    op.drop_index("ix_prep_address", table_name="prep")
    op.drop_table("prep")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "prep",
        sa.Column("address", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("country", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("city", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("website", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("details", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("p2p_endpoint", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("node_address", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("status", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("penalty", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("grade", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("last_updated_block", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("last_updated_timestamp", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("created_block", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("created_timestamp", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("logo_256", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("logo_1024", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("logo_svg", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("steemit", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("twitter", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("youtube", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("facebook", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("github", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("reddit", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("keybase", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("telegram", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("wechat", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("api_endpoint", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("server_country", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("server_city", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("server_type", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "voted", postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True
        ),
        sa.Column(
            "voting_power",
            postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "delegated",
            postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "stake", postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True
        ),
        sa.Column(
            "irep", postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True
        ),
        sa.PrimaryKeyConstraint("address", name="prep_pkey"),
    )
    op.create_index("ix_prep_address", "prep", ["address"], unique=False)
    op.drop_index(op.f("ix_preps_address"), table_name="preps")
    op.drop_table("preps")
    # ### end Alembic commands ###
