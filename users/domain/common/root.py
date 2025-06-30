from abc import ABC, abstractclassmethod, abstractmethod
from dataclasses import dataclass
from typing import Self


@dataclass(kw_only=True)
class AggregateRoot(ABC):

    def __post_init__(self):
        self._validate()

    @abstractmethod
    def _validate(self): ...

    @classmethod
    @abstractmethod
    async def create(cls, *args) -> Self: ...
