import logging
from contextlib import contextmanager
from typing import Generator

import pytest
from _pytest.logging import caplog as _caplog
from fastapi.testclient import TestClient
from loguru import logger
from sqlalchemy.orm import sessionmaker

from icon_governance.db import engine

# from icon_governance.db import get_session
# @pytest.fixture(scope="session")
# def db() -> Generator:
#     yield get_session()


@pytest.fixture(scope="session")
def db():
    SessionMade = sessionmaker(bind=engine)
    session = SessionMade()

    yield session


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


@pytest.fixture
def tmp_set_settings():
    @contextmanager
    def f(settings_name: str, value):
        from icon_governance.config import settings

        old_value = getattr(settings, settings_name)
        setattr(settings, settings_name, value)
        yield
        setattr(settings, settings_name, old_value)

    return f
