import pytest
from faker import Faker

from users.domain.user.entity import User


@pytest.fixture
def faker():
    return Faker()


@pytest.fixture
def valid_user():
    return User.create(username="valid_username", first_name="valid", last_name="valid")
