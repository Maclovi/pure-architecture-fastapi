from typing import Final, NamedTuple

from cats.application.common.ports.cat import CatGateway
from cats.application.common.ports.transaction import EntitySaver, Transaction
from cats.application.common.validators import validate_cat
from cats.entities.cat.models import CatID


class DeleteCatCommand(NamedTuple):
    cat_id: int


class DeleteCatCommandHandler:
    def __init__(
        self,
        transaction: Transaction,
        entity_saver: EntitySaver,
        cat_gateway: CatGateway,
    ) -> None:
        self._transaction: Final = transaction
        self._entity_saver: Final = entity_saver
        self._cat_gateway: Final = cat_gateway

    async def run(self, data: DeleteCatCommand) -> None:
        cat = await self._cat_gateway.with_id(CatID(data.cat_id))
        cat = validate_cat(cat, data.cat_id)
        await self._entity_saver.delete(cat)
        await self._transaction.commit()
