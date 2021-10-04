import logging
from typing import Generator

import pytest
from _pytest.logging import caplog as _caplog
from fastapi.testclient import TestClient
from loguru import logger

# from icon_governance.db import get_session
# @pytest.fixture(scope="session")
# def db() -> Generator:
#     yield get_session()

# from icon_governance.db import session
# @pytest.fixture(scope="session")
# def db():
#     yield session


@pytest.fixture(scope="module")
def client() -> Generator:
    from icon_governance.main_api import app

    with TestClient(app) as c:
        yield c


@pytest.fixture
def caplog(_caplog):
    class PropogateHandler(logging.Handler):
        def emit(self, record):
            logging.getLogger(record.name).handle(record)

    handler_id = logger.add(PropogateHandler(), format="{message} {extra}")
    yield _caplog
    logger.remove(handler_id)
