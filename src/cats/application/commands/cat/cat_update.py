from dataclasses import dataclass
from typing import final

from cats.application.common.persistence.cat import CatGateway
from cats.application.common.persistence.transaction import Transaction
from cats.application.common.validators import validate_empty
from cats.entities.cat.models import CatID
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription


@dataclass(slots=True, frozen=True)
class CatUpdate:
    cat_id: int
    age: int | None = None
    color: str | None = None
    description: str | None = None


@final
class CatUpdateHandler:
    def __init__(
        self,
        cat_gateway: CatGateway,
        transaction: Transaction,
    ) -> None:
        self._cat_gateway = cat_gateway
        self._transaction = transaction

    async def run(self, data: CatUpdate) -> None:
        cat = await self._cat_gateway.with_id(CatID(data.cat_id))
        cat = validate_empty(cat, data.cat_id)

        if data.age:
            cat.change_age(CatAge(data.age))
        if data.color:
            cat.change_color(CatColor(data.color))
        if data.description:
            cat.change_description(CatDescription(data.description))

        await self._transaction.commit()
