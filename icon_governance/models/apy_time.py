from typing import Optional

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class ApyTime(SQLModel, table=True):
    timestamp: int = Field(primary_key=True)
    height: int = Field(nullable=True)

    i_global: float = Field(nullable=True)
    i_prep: float = Field(nullable=True)
    i_cps: float = Field(nullable=True)
    i_relay: float = Field(nullable=True)

    # Pre / post iiss 4.0
    i_voter: Optional[float] = Field(nullable=True)
    i_wage: Optional[float] = Field(nullable=True)

    staking_apy: float = Field(nullable=True)
    prep_apy: float = Field(nullable=True)

    total_delegated: float = Field(nullable=True)
    total_stake: float = Field(nullable=True)
    total_bonded: float = Field(nullable=True)
    total_power: float = Field(nullable=True)

    total_wage: float = Field(nullable=True)
    active_preps: int = Field(nullable=True)


    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "apy_time"
