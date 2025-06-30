from dataclasses import dataclass

from users.domain.common.exception import DomainError


@dataclass(kw_only=True)
class InvalidUsernameError(DomainError): ...


@dataclass(kw_only=True)
class InvalidFirstNameError(DomainError): ...


@dataclass(kw_only=True)
class InvalidLastNameError(DomainError): ...
