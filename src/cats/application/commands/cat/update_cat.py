from typing import Final, NamedTuple

from cats.application.common.ports.cat import CatGateway
from cats.application.common.ports.transaction import Transaction
from cats.application.common.validators import validate_cat
from cats.entities.cat.models import CatID
from cats.entities.cat.value_objects import CatDescription


class UpdateCatDescriptionCommand(NamedTuple):
    cat_id: int
    description: str


class UpdateCatDescriptionCommandHandler:
    def __init__(
        self,
        cat_gateway: CatGateway,
        transaction: Transaction,
    ) -> None:
        self._cat_gateway: Final = cat_gateway
        self._transaction: Final = transaction

    async def run(self, data: UpdateCatDescriptionCommand) -> None:
        description = CatDescription(data.description)
        cat = await self._cat_gateway.with_id(CatID(data.cat_id))
        cat = validate_cat(cat, data.cat_id)
        cat.change_description(description)
        await self._transaction.commit()
