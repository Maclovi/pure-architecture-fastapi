from dataclasses import dataclass
from uuid import UUID

from typing_extensions import override


class ApplicationError(Exception):
    @property
    def message(self) -> str:
        return "Application error occurred"


@dataclass(eq=False)
class EntityNotFoundError(ApplicationError):
    oid: int | UUID

    @property
    @override
    def message(self) -> str:
        return f"Entity with id={self.oid} not found"
