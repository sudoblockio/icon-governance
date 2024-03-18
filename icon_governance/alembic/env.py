# from icon_governance.models.alembic_base import Base

# from sqlalchemy import engine_from_config, pool

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import SQLModel

from icon_governance.db import ASYNC_SQLALCHEMY_DATABASE_URL, SQLALCHEMY_DATABASE_URL
from icon_governance.models.apy_time import ApyTime
from icon_governance.models.delegations import Delegation
from icon_governance.models.preps import Prep
from icon_governance.models.proposals import Proposal
from icon_governance.models.rewards import Reward
from icon_governance.models.stats import Stats
from icon_governance.models.commission_time import CommissionTime

# Other versions imported each object
config = context.config

config.set_main_option("sqlalchemy.url", ASYNC_SQLALCHEMY_DATABASE_URL)

fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = SQLModel.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


IGNORE_TABLES = ["claims"]


def include_object(object, name, type_, reflected, compare_to):
    """
    Should you include this table or not?
    """

    if type_ == "table" and (name in IGNORE_TABLES or object.info.get("skip_autogenerate", False)):
        return False

    elif type_ == "column" and object.info.get("skip_autogenerate", False):
        return False

    return True


def run_migrations_offline():
    url = SQLALCHEMY_DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


# def run_migrations_online():
#     configuration = config.get_section(config.config_ini_section)
#     configuration["sqlalchemy.url"] = SQLALCHEMY_DATABASE_URL
#     connectable = engine_from_config(
#         configuration,
#         prefix="sqlalchemy.",
#         poolclass=pool.NullPool,
#     )
#
#     with connectable.connect() as connection:
#         context.configure(
#             connection=connection, target_metadata=target_metadata, compare_type=True
#         )
#
#         with context.begin_transaction():
#             context.run_migrations()

# if context.is_offline_mode():
#
#     run_migrations_offline()
# else:
#     asyncio.run(run_migrations_online())
#     # run_migrations_online()
asyncio.run(run_migrations_online())
