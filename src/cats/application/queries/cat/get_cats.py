from dataclasses import dataclass

from cats.application.common.interactor import Interactor
from cats.application.common.persistence.cat import (
    CatFilters,
    CatReader,
)
from cats.application.common.persistence.filters import Pagination
from cats.application.queries.cat.output_shared import CatsOutput


@dataclass(frozen=True, slots=True)
class GetCatsQuery:
    filters: CatFilters
    pagination: Pagination


class GetCatsQueryHandler(Interactor[GetCatsQuery, CatsOutput]):
    def __init__(self, cat_reader: CatReader) -> None:
        self._cat_reader = cat_reader

    async def run(self, data: GetCatsQuery) -> CatsOutput:
        cats = await self._cat_reader.all(data.filters, data.pagination)
        return CatsOutput(len(cats), cats)