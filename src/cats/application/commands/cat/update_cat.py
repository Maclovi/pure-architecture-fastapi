from dataclasses import dataclass
from typing import final

from cats.application.common.persistence.cat import CatGateway
from cats.application.common.persistence.transaction import Transaction
from cats.application.common.validators import validate_empty
from cats.entities.cat.models import CatID
from cats.entities.cat.value_objects import CatDescription


@dataclass(slots=True, frozen=True)
class UpdateCatDescriptionCommand:
    cat_id: int
    description: str


@final
class UpdateCatDescriptionCommandHandler:
    def __init__(
        self,
        cat_gateway: CatGateway,
        transaction: Transaction,
    ) -> None:
        self._cat_gateway = cat_gateway
        self._transaction = transaction

    async def run(self, data: UpdateCatDescriptionCommand) -> None:
        description = CatDescription(data.description)
        cat = await self._cat_gateway.with_id(CatID(data.cat_id))
        cat = validate_empty(cat, data.cat_id)
        cat.change_description(description)
        await self._transaction.commit()
