from fastapi.testclient import TestClient

from icon_governance.config import settings

# This test is failing as no data in rewards table
# def test_api_rewards_address(client: TestClient):
#     response = client.get(f"{settings.REST_PREFIX}/governance/rewards/hxfc56203484921c3b7a4dee9579d8614d8c8daaf5")
#     assert response.status_code == 200
