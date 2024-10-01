from dataclasses import dataclass

from cats.application.common.interactor import Interactor
from cats.application.common.persistence.breed import BreedGateway
from cats.application.common.persistence.filters import Pagination
from cats.entities.breed.models import Breed


@dataclass(frozen=True, slots=True)
class GetBreedsQuery:
    pagination: Pagination


@dataclass(frozen=True, slots=True)
class BreedsOutput:
    total: int
    breeds: list[Breed]


class GetBreedsQueryHandler(Interactor[GetBreedsQuery, BreedsOutput]):
    def __init__(self, breed_gateway: BreedGateway) -> None:
        self._breed_gateway = breed_gateway

    async def run(self, data: GetBreedsQuery) -> BreedsOutput:
        breeds = await self._breed_gateway.all(data.pagination)
        return BreedsOutput(len(breeds), breeds)
