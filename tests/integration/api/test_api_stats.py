from fastapi.testclient import TestClient

from icon_governance.config import settings


def test_api_stats_get_apy_over_time(client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/governance/stats/apy/time")
    assert response.status_code == 200


def test_api_stats_get_commission_over_time(client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/governance/stats/commission/time")
    assert response.status_code == 200


def test_api_stats_get_governance_stats(client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/governance/stats")
    assert response.status_code == 200
