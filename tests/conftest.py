import asyncio
import logging
from contextlib import contextmanager
from typing import Generator

import pytest
from _pytest.logging import caplog as _caplog
from fastapi.testclient import TestClient
from loguru import logger
from sqlalchemy.orm import sessionmaker

# from icon_governance.db import engine

# from icon_governance.db import get_session
# @pytest.fixture(scope="session")
# def db() -> Generator:
#     yield get_session()
import pytest_asyncio

# @pytest.yield_fixture(scope='session')
# def event_loop(request):
#     """Create an instance of the default event loop for each test case."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture(scope="session")
def db():
    from icon_governance.db import engine
    SessionMade = sessionmaker(bind=engine)
    session = SessionMade()
    yield session
    session.close()


@pytest.fixture(scope="module")
def client() -> Generator:
    from icon_governance.main_api import app
    output = TestClient(app)
    return output
    # return TestClient(app)

    # with TestClient(app) as c:
    #     yield c


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

        try:
            old_value = getattr(settings, settings_name)
            setattr(settings, settings_name, value)
            yield
        finally:
            setattr(settings, settings_name, old_value)

    return f
