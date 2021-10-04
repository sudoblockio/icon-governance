from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from icon_governance.config import settings


def test_api_get_preps(db: Session, client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/preps")
    assert response.status_code == 200
