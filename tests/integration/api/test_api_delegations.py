import httpx
import pytest
from fastapi.testclient import TestClient

from icon_governance.config import settings


# TODO: Not properly hydrated - skip
@pytest.mark.asyncio
async def test_api_delegations_address(client: httpx.AsyncClient):
    response = await client.get(f"{settings.REST_PREFIX}/governance/delegations/hxf55eccb07a95a263a81d79561adb372bc39b3ca8")
    assert response.status_code == 200


# THis test failed as delegation table was empty. Added data to delegation table, and it worked
# Need to run test_delegation test before running this test
@pytest.mark.asyncio
async def test_api_votes_address(client: httpx.AsyncClient):
    response = await client.get(f"{settings.REST_PREFIX}/governance/votes/hx0b047c751658f7ce1b2595da34d57a0e7dad357d")
    assert response.status_code == 200
