
import datetime

import pytest
from auth.models.user import User


@pytest.mark.asyncio
async def test_create_user():
    user = User(
        username="mockuser",
        email="mockuser@example.com",
        password="mockpassword",
        first_name="Mock",
        last_name="User",
        birth_date=datetime.date.today().isoformat(),
        gender="Male",
        city="Mock City",
        interests=["Coding", "AI"]
    )

    await user.insert()
    assert user.id is not None, 'User ID should not be None'