import pytest

from users.domain.user.entity import User
from users.domain.user.exceptions import (
    InvalidFirstNameError,
    InvalidLastNameError,
    InvalidUsernameError,
)


def test_create_user(faker):
    username = faker.user_name()
    first_name = faker.first_name()
    last_name = faker.last_name()
    middle_name = faker.first_name()

    user = User.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
    )

    assert user.id is not None
    assert user.username == username
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.middle_name == middle_name


def test_invalid_username(faker):
    invalid_usernames = [
        "username with spaces",
        "*?,special=+symbols>/",
        "too_long" * 500,
        "too_short"[0:3],
    ]

    for username in invalid_usernames:
        with pytest.raises(InvalidUsernameError):
            User.create(
                username=username,
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                middle_name=faker.first_name(),
            )


def test_invalid_first_name(faker):
    invalid_first_names = [
        "name_with/special*symbols",
        "name with spaces",
        "nam3withdigits",
        "",
    ]

    for name in invalid_first_names:
        with pytest.raises(InvalidFirstNameError):
            User.create(
                username="valid_name",
                first_name=name,
                last_name=faker.last_name(),
                middle_name=faker.first_name(),
            )


def test_invalid_last_name(faker):
    invalid_last_names = [
        "name_with/special*symbols",
        "name with spaces",
        "nam3withdigits",
        "",
    ]

    for name in invalid_last_names:
        with pytest.raises(InvalidLastNameError):
            User.create(
                username="valid_name",
                first_name=faker.first_name(),
                last_name=name,
                middle_name=faker.first_name(),
            )


def test_set_name(valid_user):
    valid_user.update_name(
        first_name="NewFirstName", last_name="NewLastName", middle_name="NewMiddleName"
    )

    assert valid_user.first_name == "Newfirstname"
    assert valid_user.last_name == "Newlastname"
    assert valid_user.middle_name == "Newmiddlename"


def test_update_name_with_invalid_data(valid_user):
    old_first_name = valid_user.first_name
    old_last_name = valid_user.last_name
    old_middle_name = valid_user.middle_name

    with pytest.raises(InvalidFirstNameError):
        valid_user.update_name(first_name="Invalid First Name")
    assert valid_user.first_name == old_first_name

    with pytest.raises(InvalidLastNameError):
        valid_user.update_name(last_name="Invalid Last Name")
    assert valid_user.last_name == old_last_name

    # TODO test for middle_name
