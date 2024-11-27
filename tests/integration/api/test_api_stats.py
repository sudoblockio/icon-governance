import httpx
import pytest
from fastapi.testclient import TestClient

from icon_governance.config import settings

# There is
# def test_api_stats_get_apy_over_time(client: TestClient):
#     response = client.get(f"{settings.REST_PREFIX}/governance/stats/apy/time")
#     assert response.status_code == 200
#
#
# def test_api_stats_get_commission_over_time(client: TestClient):
#     response = client.get(f"{settings.REST_PREFIX}/governance/stats/commission/time")
#     assert response.status_code == 200

@pytest.mark.asyncio
async def test_api_stats_get_governance_stats(client: httpx.AsyncClient):
    response = await client.get(f"{settings.REST_PREFIX}/governance/stats")
    assert response.status_code == 200
