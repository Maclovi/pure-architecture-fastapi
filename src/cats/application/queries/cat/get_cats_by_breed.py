from dataclasses import dataclass

from cats.application.common.persistence.cat import CatReader
from cats.application.common.persistence.filters import Pagination
from cats.application.queries.cat.output_shared import CatsOutput
from cats.entities.breed.value_objects import BreedName


@dataclass(frozen=True, slots=True)
class GetCatsWithBreedQuery:
    breed_name: str
    pagination: Pagination


class GetCatsWithBreedQueryHandler:
    def __init__(self, cat_reader: CatReader) -> None:
        self._cat_reader = cat_reader

    async def run(self, data: GetCatsWithBreedQuery) -> CatsOutput:
        cats = await self._cat_reader.with_breed_name(
            BreedName(data.breed_name),
            data.pagination,
        )
        return CatsOutput(len(cats), cats)
