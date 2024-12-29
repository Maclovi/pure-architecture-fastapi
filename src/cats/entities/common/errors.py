from dataclasses import dataclass


@dataclass(eq=False)
class DomainError(Exception):
    @property
    def message(self) -> str:
        raise NotImplementedError


class FieldError(DomainError):
    pass


class InsertProcessingError(DomainError):
    pass
