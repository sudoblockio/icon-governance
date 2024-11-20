from fastapi.testclient import TestClient

from icon_governance.config import settings


def test_api_delegations_address(client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/governance/delegations/cx43e2eec79eb76293c298f2b17aec06097be606e0")
    assert response.status_code == 200


def test_api_votes_address(client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/governance/votes/hxfc56203484921c3b7a4dee9579d8614d8c8daaf5")
    assert response.status_code == 200
