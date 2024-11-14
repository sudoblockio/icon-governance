from typing import Optional

from sqlalchemy.orm import declared_attr
from sqlmodel import JSON, Column, Field, SQLModel


class Proposal(SQLModel, table=True):

    id: Optional[int] = Field(None, primary_key=True)
    proposer: Optional[str] = Field(None, index=False)
    proposer_name: Optional[str] = Field(None, index=False)
    status: Optional[str] = Field(None, index=False)

    start_block_height: Optional[int] = Field(None, index=False)
    end_block_height: Optional[int] = Field(None, index=False)

    contents_json: Optional[dict] = Field(
        None, sa_column=Column(JSON, index=False)
    )
    title: Optional[str] = Field(None, index=False)
    description: Optional[str] = Field(None, index=False)
    type: Optional[str] = Field(None, index=False)

    # value: Optional[Dict[Any, Any]] = Field(None, index=False, sa_column=Column(JSON))

    agree_count: Optional[str] = Field(None, index=False)
    agree_amount: Optional[str] = Field(None, index=False)
    disagree_count: Optional[str] = Field(None, index=False)
    disagree_amount: Optional[str] = Field(None, index=False)
    no_vote_count: Optional[str] = Field(None, index=False)
    no_vote_amount: Optional[str] = Field(None, index=False)

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "proposals"
