import re
from dataclasses import dataclass
from typing import Self

from users.domain.common.entity import BaseEntity
from users.domain.common.root import AggregateRoot
from users.domain.user.exceptions import (
    InvalidUsernameError,
    InvalidFirstNameError,
    InvalidLastNameError,
)

USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_.-]{3,30}$")
NAME_PATTERN = re.compile(r"^([A-ZА-ЯЁ][a-zа-яё]{1,49})(-[A-ZА-ЯЁ][a-zа-яё]{1,49})?$")


@dataclass(kw_only=True)
class User(BaseEntity, AggregateRoot):
    username: str
    first_name: str
    last_name: str
    middle_name: str | None = None

    @classmethod
    def create(
        cls,
        username: str,
        first_name: str,
        last_name: str,
        middle_name: str | None = None,
    ) -> Self:
        return cls(
            username=username,
            first_name=first_name.title(),
            last_name=last_name.title(),
            middle_name=middle_name.title() if middle_name else None,
        )

    def update_name(
        self,
        first_name: str | None = None,
        last_name: str | None = None,
        middle_name: str | None = None,
    ):
        if first_name is not None:
            first_name = first_name.title()
            self.__validate_first_name(first_name)
            self.first_name = first_name

        if last_name is not None:
            last_name = last_name.title()
            self.__validate_last_name(last_name)
            self.last_name = last_name

        if (
            self.middle_name is not None and middle_name is None
        ) or middle_name is not None:
            middle_name = middle_name.title() if middle_name else None
            self.__validate_middle_name(middle_name)
            self.middle_name = middle_name

    def _validate(self):
        self.__validate_username(self.username)
        self.__validate_first_name(self.first_name)
        self.__validate_last_name(self.last_name)
        self.__validate_middle_name(self.middle_name)

    def __validate_first_name(self, first_name):
        if not re.match(NAME_PATTERN, first_name):
            raise InvalidFirstNameError(
                msg="First name must contain only Latin or Cyrillic letters. "
                "One optional hyphen allowed. No digits, spaces, or special characters."
            )

    def __validate_last_name(self, last_name):
        if not re.match(NAME_PATTERN, last_name):
            raise InvalidLastNameError(
                msg="Last name must contain only Latin or Cyrillic letters. "
                "One optional hyphen allowed. No digits, spaces, or special characters."
            )

    def __validate_middle_name(self, middle_name):
        if middle_name is not None:
            if not re.match(NAME_PATTERN, middle_name):
                raise InvalidLastNameError(
                    msg="Middle name must contain only Latin or Cyrillic letters. "
                    "One optional hyphen allowed. No digits, spaces, or special characters."
                )

    def __validate_username(self, username):
        if not 7 <= len(username) <= 32:
            raise InvalidUsernameError(
                msg="Username must be between 7 and 32 characters long."
            )

        if not re.match(USERNAME_PATTERN, username):
            raise InvalidUsernameError(
                msg="Username may only contain Latin letters, digits, and the symbols ., -, and _. "
                "No spaces or other characters allowed."
            )
