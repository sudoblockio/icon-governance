from typing import Optional

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class ApyTime(SQLModel, table=True):
    timestamp: int = Field(primary_key=True)
    height: int = Field(nullable=False)

    i_global: float = Field(nullable=False)
    i_prep: float = Field(nullable=False)
    i_cps: float = Field(nullable=False)
    i_relay: float = Field(nullable=False)

    # Pre / post iiss 4.0
    i_voter: Optional[float] = Field(nullable=True)
    i_wage: Optional[float] = Field(nullable=True)

    staking_apy: float = Field(nullable=False)
    prep_apy: float = Field(nullable=False)
    cps_apy: float = Field(nullable=False)
    relay_apy: float = Field(nullable=False)

    total_delegated: float = Field(nullable=False)
    total_stake: float = Field(nullable=False)
    total_bonded: float = Field(nullable=False)
    total_power: float = Field(nullable=False)

    total_wage: float = Field(nullable=False)
    active_preps: int = Field(nullable=False)


    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "apy_time"
