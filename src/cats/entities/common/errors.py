from abc import abstractmethod
from dataclasses import dataclass


@dataclass(eq=False)
class DomainError(Exception):
    @property
    @abstractmethod
    def message(self) -> str:
        raise NotImplementedError


@dataclass(eq=False)
class FieldError(DomainError):
    pass


@dataclass(eq=False)
class InsertProcessingError(DomainError):
    pass
