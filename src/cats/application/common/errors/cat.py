from dataclasses import dataclass

from typing_extensions import override

from cats.application.common.errors.base import EntityNotFoundError


@dataclass(eq=False)
class CatNotFoundError(EntityNotFoundError):
    id: int

    @property
    @override
    def message(self) -> str:
        return f"Cat with id={self.id} not found"
