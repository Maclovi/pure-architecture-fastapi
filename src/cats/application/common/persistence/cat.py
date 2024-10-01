from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Protocol

from cats.application.common.persistence.filters import Pagination
from cats.application.common.persistence.view_models import CatView
from cats.entities.breed.value_objects import BreedName
from cats.entities.cat.models import Cat, CatID


@dataclass(frozen=True)
class CatFilters:
    breed: str | None = field(default=None)
    color: str | None = field(default=None)


class CatGateway(Protocol):
    @abstractmethod
    async def with_id(self, cat_id: CatID) -> Cat | None: ...


class CatReader(Protocol):
    @abstractmethod
    async def with_breed_name(
        self, breed_name: BreedName, pagination: Pagination
    ) -> list[CatView]: ...

    @abstractmethod
    async def all(
        self, filters: CatFilters, pagination: Pagination
    ) -> list[CatView]: ...
