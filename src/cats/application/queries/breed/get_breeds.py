from dataclasses import dataclass
from typing import Final

from cats.application.common.ports.breed import BreedGateway
from cats.application.common.ports.filters import Pagination
from cats.entities.breed.models import Breed


@dataclass(frozen=True, slots=True)
class GetBreedsQuery:
    pagination: Pagination


@dataclass(frozen=True, slots=True)
class BreedsOutput:
    total: int
    breeds: list[Breed]


class GetBreedsQueryHandler:
    def __init__(self, breed_gateway: BreedGateway) -> None:
        self._breed_gateway: Final = breed_gateway

    async def run(self, data: GetBreedsQuery) -> BreedsOutput:
        breeds = await self._breed_gateway.all(data.pagination)
        return BreedsOutput(len(breeds), breeds)
