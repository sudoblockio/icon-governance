from typing import Optional, Any, List
from sqlmodel import Field, Session, SQLModel, create_engine


class PrepBase(SQLModel):
    address: str


class PrepCreate(PrepBase):
    pass


class Prep(PrepBase, table=True):
    address: str = Field(primary_key=True)

    name: Optional[str]
    country: Optional[str]
    city: Optional[str]
    email: Optional[str]
    website: Optional[str]
    details: Optional[str]
    p2p_endpoint: Optional[str]
    node_address: Optional[str]

    status: Optional[str] = "active"

    last_updated_block: Optional[int]
    last_updated_timestamp: Optional[int]
    created_block: Optional[int]
    created_timestamp: Optional[int]

    # Logos
    logo_256: Optional[str] = None
    logo_1024: Optional[str] = None
    logo_svg: Optional[str] = None

    # Social Media
    steemit: Optional[str] = None
    twitter: Optional[str] = None
    youtube: Optional[str] = None
    facebook: Optional[str] = None
    github: Optional[str] = None
    reddit: Optional[str] = None
    keybase: Optional[str] = None
    telegram: Optional[str] = None
    wechat: Optional[str] = None

    # Server
    api_endpoint: Optional[str] = None
    server_country: Optional[str] = None
    server_city: Optional[str] = None
    server_type: Optional[str] = None
