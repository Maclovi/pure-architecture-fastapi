from dataclasses import dataclass
from typing import final

from cats.application.common.persistence.cat import CatGateway
from cats.application.common.persistence.transaction import (
    EntitySaver,
    Transaction,
)
from cats.application.common.validators import validate_empty
from cats.entities.cat.models import CatID


@dataclass(slots=True, frozen=True)
class DeleteCatCommand:
    cat_id: int


@final
class DeleteCatCommandHandler:
    def __init__(
        self,
        transaction: Transaction,
        entity_saver: EntitySaver,
        cat_gateway: CatGateway,
    ) -> None:
        self._transaction = transaction
        self._entity_saver = entity_saver
        self._cat_gateway = cat_gateway

    async def run(self, data: DeleteCatCommand) -> None:
        cat = await self._cat_gateway.with_id(CatID(data.cat_id))
        cat = validate_empty(cat, data.cat_id)

        await self._entity_saver.delete(cat)
        await self._transaction.commit()
