from typing import Optional

from pydantic import condecimal
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class Reward(SQLModel, table=True):
    tx_hash: Optional[str] = Field(primary_key=True)
    address: Optional[str] = Field(..., index=True)
    block: Optional[int] = Field(None)
    timestamp: Optional[int] = Field(None)

    # Come from Tx logs
    value: condecimal(max_digits=10, decimal_places=3) = Field(None)
    iscore: condecimal(max_digits=13, decimal_places=3) = Field(None)

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "rewards"
