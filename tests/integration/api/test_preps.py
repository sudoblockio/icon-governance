from fastapi.testclient import TestClient
from icon_governance.config import settings

from sqlalchemy.orm import Session


def test_api_get_preps(db: Session, client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/preps")
    print()
