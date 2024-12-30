class DomainError(Exception):
    pass


class FieldError(DomainError):
    @property
    def message(self) -> str:
        raise NotImplementedError


class InsertProcessingError(DomainError):
    pass
