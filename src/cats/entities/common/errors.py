from abc import abstractmethod


class DomainError(Exception):
    pass


class FieldError(DomainError):
    @property
    @abstractmethod
    def message(self) -> str:
        raise NotImplementedError


class InsertProcessingError(DomainError):
    pass
