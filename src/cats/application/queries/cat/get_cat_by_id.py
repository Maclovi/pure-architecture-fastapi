from typing import Final, NamedTuple

from cats.application.common.ports.cat import CatReader
from cats.application.common.ports.view_models import CatView
from cats.application.common.validators import validate_cat
from cats.entities.cat.models import CatID


class GetCatWithIDQuery(NamedTuple):
    id: int


class CatOutput(NamedTuple):
    cat: CatView


class GetCatWithIDQueryHandler:
    def __init__(self, cat_reader: CatReader) -> None:
        self._cat_reader: Final = cat_reader

    async def run(self, data: GetCatWithIDQuery) -> CatOutput:
        cat = await self._cat_reader.with_id(CatID(data.id))
        cat = validate_cat(cat, data.id)
        return CatOutput(cat)
