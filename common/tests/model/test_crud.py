from typing import Any
from uuid import UUID, uuid4

from pydantic import Field
import pytest

from common.model import BasePgModel

class TestModel(BasePgModel):
    __database__ = 'social_network'
    __table__ = 'test_table'
    
    id: UUID = Field(default_factory=uuid4)
    field: str


@pytest.mark.asyncio
async def test_insert():
    test_model = TestModel(
        field="test_field",
    )
    assert test_model.id is not None, 'TestModel ID must be set'

    test_model = await test_model.insert()

    assert test_model.id is not None, 'TestModel ID must be set'

@pytest.mark.asyncio
async def test_load():
    test_model = TestModel(
        field="test_field",
    )
    test_model = await test_model.insert()

    test_model_loaded = await TestModel.load(test_model.id)
    assert test_model_loaded.id == test_model.id