from typing import Generator

import pytest
from fastapi.testclient import TestClient

from core.db import DBSetup
from main import app


@pytest.fixture(scope="session")
def db() -> Generator:
    db_setup = DBSetup()
    yield db_setup.get_session()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
