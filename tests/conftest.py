import asyncio
import logging
from contextlib import contextmanager
from typing import Generator

import pytest
import httpx
from _pytest.logging import caplog as _caplog
from fastapi.testclient import TestClient
from httpx import AsyncClient
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from icon_governance.main_api import app

from icon_governance.db import engine

# from icon_governance.db import get_session
# @pytest.fixture(scope="session")
# def db() -> Generator:
#     yield get_session()
import pytest_asyncio
# from starlette.testclient import TestClient


@pytest.fixture(scope="session")
def event_loop():
    """Create a new event loop for the entire test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

# @pytest.fixture(scope="function")
# async def db():
#     from icon_governance.db import get_session
#     async for session in get_session():
#         yield session

@pytest.fixture(scope="session")
def db():
    SessionMade = sessionmaker(bind=engine)
    session = SessionMade()

    yield session


# @pytest_asyncio.fixture(scope="module")
# def client() -> TestClient:
#     return TestClient(app)

@pytest_asyncio.fixture(scope="module")
async def client() -> httpx.AsyncClient:
    async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

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
