from httpx import AsyncClient
import pytest

from web import app


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

@pytest.fixture
async def dataset():
    from social_network.tests.dataset import Dataset

    yield Dataset
