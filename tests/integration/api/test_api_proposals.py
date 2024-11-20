from fastapi.testclient import TestClient

from icon_governance.config import settings


def test_api_proposals(client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/governance/proposals")
    assert response.status_code == 200
