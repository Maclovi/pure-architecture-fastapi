from dataclasses import dataclass
from typing import final

from cats.application.common.persistence.cat import CatReader
from cats.application.common.persistence.view_models import CatView
from cats.application.common.validators import validate_cat
from cats.entities.cat.models import CatID


@dataclass(slots=True, frozen=True)
class GetCatWithIDQuery:
    id: int


@dataclass(slots=True, frozen=True)
class CatOutput:
    cat: CatView


@final
class GetCatWithIDQueryHandler:
    def __init__(self, cat_reader: CatReader) -> None:
        self._cat_reader = cat_reader

    async def run(self, data: GetCatWithIDQuery) -> CatOutput:
        cat = await self._cat_reader.with_id(CatID(data.id))
        cat = validate_cat(cat, data.id)
        return CatOutput(cat)
