from dataclasses import dataclass
from typing import Final

from cats.application.common.persistence.cat import CatReader
from cats.application.common.persistence.view_models import CatView
from cats.application.common.validators import validate_cat
from cats.entities.cat.models import CatID


@dataclass(frozen=True, slots=True)
class GetCatWithIDQuery:
    id: int


@dataclass(frozen=True, slots=True)
class CatOutput:
    cat: CatView


class GetCatWithIDQueryHandler:
    def __init__(self, cat_reader: CatReader) -> None:
        self._cat_reader: Final = cat_reader

    async def run(self, data: GetCatWithIDQuery) -> CatOutput:
        cat = await self._cat_reader.with_id(CatID(data.id))
        assert validate_cat(cat, data.id)
        return CatOutput(cat)
