class DomainError(Exception):
    pass


class FieldError(DomainError):
    message: str


class InsertProcessingError(DomainError):
    pass
