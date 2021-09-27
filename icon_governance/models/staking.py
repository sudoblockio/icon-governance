from typing import Optional, Any, List
from sqlmodel import Field, Session, SQLModel, create_engine
from pydantic import condecimal


class DelegationsBase(SQLModel):
    address: str
    prep_address: str
    amount: float


class Delegations(DelegationsBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    prep_address: str
    value: condecimal(max_digits=13, decimal_places=10) = Field(nullable=False, index=False)


class DelegationTransactionsBase(SQLModel):
    address: str
    prep_address: str
    amount: str
