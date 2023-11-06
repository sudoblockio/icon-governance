import datetime

from sqlalchemy import Column
from sqlalchemy.orm import declared_attr
from sqlalchemy.types import DateTime
from sqlmodel import Field, SQLModel


class ApyTime(SQLModel, table=True):
    # date: datetime.datetime = Field(
    #     sa_column=Column(DateTime(timezone=True)),
    #     primary_key=True,
    # )
    timestamp: int = Field(primary_key=True)
    height: int = Field(nullable=False)

    i_global: float = Field(nullable=False)
    i_voter: float = Field(nullable=False)
    i_prep: float = Field(nullable=False)
    i_cps: float = Field(nullable=False)
    i_relay: float = Field(nullable=False)

    staking_apy: float = Field(nullable=False)
    prep_apy: float = Field(nullable=False)
    cps_apy: float = Field(nullable=False)
    relay_apy: float = Field(nullable=False)

    total_delegated: float = Field(nullable=False)
    total_stake: float = Field(nullable=False)

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "apy_time"
