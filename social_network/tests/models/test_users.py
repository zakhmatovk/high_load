import datetime
from uuid import uuid4

import pytest
from social_network.models.user import User


async def test_create_user():
    password = str(uuid4())
    user = User(
        username="mockuser",
        email="mockuser@example.com",
        password=password,
        first_name="Mock",
        last_name="User",
        birth_date=datetime.date.today(),
        gender="Male",
        city="Mock City",
        interests=["Coding", "AI"],
    )

    user = await user.insert()
    assert user.id is not None, "User ID should not be None"
    assert user.password.get_secret_value() != password, "Password should be encrypted"
