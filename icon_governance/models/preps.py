from typing import Optional

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class Prep(SQLModel, table=True):
    address: str = Field(primary_key=True)

    name: Optional[str] = Field(None)
    country: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    website: Optional[str] = Field(None)
    details: Optional[str] = Field(None)
    node_address: Optional[str] = Field(None)
    public_key: Optional[str] = Field(None)

    node_state: Optional[str] = Field(None)

    status: Optional[str] = Field(None)
    penalty: Optional[str] = Field(None)
    grade: Optional[str] = Field(None)

    last_updated_block: Optional[int] = Field(None)
    last_updated_timestamp: Optional[int] = Field(None)
    created_block: Optional[int] = Field(None)
    created_timestamp: Optional[int] = Field(None)

    # Logos
    logo_256: Optional[str] = Field(None)
    logo_1024: Optional[str] = Field(None)
    logo_svg: Optional[str] = Field(None)

    # Social Media
    steemit: Optional[str] = Field(None)
    twitter: Optional[str] = Field(None)
    youtube: Optional[str] = Field(None)
    facebook: Optional[str] = Field(None)
    github: Optional[str] = Field(None)
    reddit: Optional[str] = Field(None)
    keybase: Optional[str] = Field(None)
    telegram: Optional[str] = Field(None)
    wechat: Optional[str] = Field(None)

    # Endpoints
    api_endpoint: Optional[str] = Field(None)
    metrics_endpoint: Optional[str] = Field(None)
    p2p_endpoint: Optional[str] = Field(None)

    # Server
    server_country: Optional[str] = Field(None)
    server_city: Optional[str] = Field(None)
    server_type: Optional[str] = Field(None)

    # Delegation
    voted: Optional[float] = Field(None)
    voting_power: Optional[float] = Field(None)
    delegated: Optional[float] = Field(None)
    stake: Optional[float] = Field(None)
    irep: Optional[float] = Field(None)
    irep_updated_block_height: Optional[float] = Field(None)

    # Productivity
    total_blocks: Optional[float] = Field(None)
    validated_blocks: Optional[float] = Field(None)
    unvalidated_sequence_blocks: Optional[float] = Field(None)

    bonded: Optional[float] = Field(None)
    power: Optional[float] = Field(None)

    # CPS
    sponsored_cps_grants: Optional[int] = Field(None)
    cps_governance: bool = Field(False)

    # Blocks
    failure_count: int = Field(None)
    penalties: int = Field(None)

    # Rewards
    reward_monthly: float = Field(None)
    reward_monthly_usd: float = Field(None)
    reward_daily: float = Field(None)
    reward_daily_usd: float = Field(None)

    class Config:
        extra = "ignore"

    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return "preps"
