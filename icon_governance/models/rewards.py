from typing import Optional

from pydantic import condecimal
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class Reward(SQLModel, table=True):
    tx_hash: Optional[str] = Field(primary_key=True)
    address: Optional[str] = Field(..., index=True)
    block: Optional[int]
    timestamp: Optional[int]

    # Come from Tx logs
    value: condecimal(max_digits=10, decimal_places=3) = None
    iscore: condecimal(max_digits=13, decimal_places=3) = None

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "rewards"
