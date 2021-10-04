from typing import Any, List, Optional

from sqlmodel import Field, Session, SQLModel, create_engine


class Prep(SQLModel, table=True):
    address: str = Field(primary_key=True)

    name: Optional[str] = Field(None, index=False)
    country: Optional[str] = Field(None, index=False)
    city: Optional[str] = Field(None, index=False)
    email: Optional[str] = Field(None, index=False)
    website: Optional[str] = Field(None, index=False)
    details: Optional[str] = Field(None, index=False)
    p2p_endpoint: Optional[str] = Field(None, index=False)
    node_address: Optional[str] = Field(None, index=False)

    status: Optional[str] = Field(None, index=False)
    penalty: Optional[str] = Field(None, index=False)
    grade: Optional[str] = Field(None, index=False)

    last_updated_block: Optional[int] = Field(None, index=False)
    last_updated_timestamp: Optional[int] = Field(None, index=False)
    created_block: Optional[int] = Field(None, index=False)
    created_timestamp: Optional[int] = Field(None, index=False)

    # Logos
    logo_256: Optional[str] = Field(None, index=False)
    logo_1024: Optional[str] = Field(None, index=False)
    logo_svg: Optional[str] = Field(None, index=False)

    # Social Media
    steemit: Optional[str] = Field(None, index=False)
    twitter: Optional[str] = Field(None, index=False)
    youtube: Optional[str] = Field(None, index=False)
    facebook: Optional[str] = Field(None, index=False)
    github: Optional[str] = Field(None, index=False)
    reddit: Optional[str] = Field(None, index=False)
    keybase: Optional[str] = Field(None, index=False)
    telegram: Optional[str] = Field(None, index=False)
    wechat: Optional[str] = Field(None, index=False)

    # Server
    api_endpoint: Optional[str] = Field(None, index=False)
    server_country: Optional[str] = Field(None, index=False)
    server_city: Optional[str] = Field(None, index=False)
    server_type: Optional[str] = Field(None, index=False)
