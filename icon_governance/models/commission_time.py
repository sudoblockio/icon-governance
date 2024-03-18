from typing import Optional

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class CommissionTime(SQLModel, table=True):
    timestamp: int = Field(primary_key=True)
    height: int = Field(nullable=False, index=True)

    commission_rate_average: float = Field(nullable=False)
    commission_rate_weighted_average: float = Field(nullable=False)
    commission_rate_median: float = Field(nullable=False)
    commission_rate_max: float = Field(nullable=False)
    commission_rate_min: float = Field(nullable=False)
    commission_rate_stdev: float = Field(nullable=False)
    commission_rate_weighted_stdev: float = Field(nullable=False)

    max_commission_change_rate_average: float = Field(nullable=False)
    max_commission_change_rate_weighted_average: float = Field(nullable=False)
    max_commission_change_rate_median: float = Field(nullable=False)
    max_commission_change_rate_max: float = Field(nullable=False)
    max_commission_change_rate_min: float = Field(nullable=False)
    max_commission_change_rate_stdev: float = Field(nullable=False)
    max_commission_change_rate_weighted_stdev: float = Field(nullable=False)

    max_commission_rate_average: float = Field(nullable=False)
    max_commission_rate_weighted_average: float = Field(nullable=False)
    max_commission_rate_median: float = Field(nullable=False)
    max_commission_rate_max: float = Field(nullable=False)
    max_commission_rate_min: float = Field(nullable=False)
    max_commission_rate_stdev: float = Field(nullable=False)
    max_commission_rate_weighted_stdev: float = Field(nullable=False)

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "commission_time"
