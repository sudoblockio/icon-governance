import httpx
import pytest
from fastapi.testclient import TestClient

from icon_governance.config import settings


@pytest.mark.asyncio
async def test_api_proposals(client: httpx.AsyncClient):
    response = await client.get(f"{settings.REST_PREFIX}/governance/proposals")
    assert response.status_code == 200
