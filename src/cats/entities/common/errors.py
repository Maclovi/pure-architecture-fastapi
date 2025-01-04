class DomainError(Exception):
    @property
    def message(self) -> str:
        return "Domain error occurred"


class FieldError(DomainError):
    pass
