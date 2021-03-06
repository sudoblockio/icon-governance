"""node state add

Revision ID: 11b01658b724
Revises: ad46aa4e5386
Create Date: 2021-11-15 21:08:52.990959

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "11b01658b724"
down_revision = "ad46aa4e5386"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "preps", sa.Column("node_state", sqlmodel.sql.sqltypes.AutoString(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "proposals", "id", existing_type=sa.INTEGER(), nullable=False, autoincrement=True
    )
    op.drop_column("preps", "node_state")
    # ### end Alembic commands ###
