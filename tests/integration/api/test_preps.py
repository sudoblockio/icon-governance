import httpx
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from icon_governance.config import settings

@pytest.mark.asyncio
async def test_api_get_preps(db: Session, client: httpx.AsyncClient):
    response = await client.get(f"{settings.REST_PREFIX}/governance/preps")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_api_get_prep_error(db: Session, client: httpx.AsyncClient):
    response = await client.get(
        f"{settings.REST_PREFIX}/governance/preps/hx0b047c751658f7ce1b2595da34d57a0"
    )
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_api_get_preps_by_address(db: Session, client: httpx.AsyncClient):
    response = await client.get(
        f"{settings.REST_PREFIX}/governance/preps/hxfc56203484921c3b7a4dee9579d8614d8c8daaf5"
    )
    assert response.status_code == 200
