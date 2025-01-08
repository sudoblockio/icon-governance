"""v0.10.0-add-preps-indexes

Revision ID: cb7b9f733741
Revises: 939ec864a967
Create Date: 2024-11-20 19:38:50.609673

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'cb7b9f733741'
down_revision = '939ec864a967'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_preps_bond_percent'), 'preps', ['bond_percent'], unique=False)
    op.create_index(op.f('ix_preps_commission_rate'), 'preps', ['commission_rate'], unique=False)
    op.create_index(op.f('ix_preps_failure_count'), 'preps', ['failure_count'], unique=False)
    op.create_index(op.f('ix_preps_grade'), 'preps', ['grade'], unique=False)
    op.create_index(op.f('ix_preps_has_public_key'), 'preps', ['has_public_key'], unique=False)
    op.create_index(op.f('ix_preps_jail_flags'), 'preps', ['jail_flags'], unique=False)
    op.create_index(op.f('ix_preps_name'), 'preps', ['name'], unique=False)
    op.create_index(op.f('ix_preps_penalty'), 'preps', ['penalty'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_preps_penalty'), table_name='preps')
    op.drop_index(op.f('ix_preps_name'), table_name='preps')
    op.drop_index(op.f('ix_preps_jail_flags'), table_name='preps')
    op.drop_index(op.f('ix_preps_has_public_key'), table_name='preps')
    op.drop_index(op.f('ix_preps_grade'), table_name='preps')
    op.drop_index(op.f('ix_preps_failure_count'), table_name='preps')
    op.drop_index(op.f('ix_preps_commission_rate'), table_name='preps')
    op.drop_index(op.f('ix_preps_bond_percent'), table_name='preps')
    # ### end Alembic commands ###
