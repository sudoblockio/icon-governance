from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class Stats(SQLModel, table=True):
    timestamp: int = Field(primary_key=True, nullable=False)

    stakers: int = Field(nullable=False)
    bonders: int = Field(nullable=False)

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "stats"
