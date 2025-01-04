class ApplicationError(Exception):
    @property
    def message(self) -> str:
        return "Application error occurred"


class EntityNotFoundError(ApplicationError):
    pass
