from dataclasses import dataclass
from typing import Final

from cats.application.common.persistence.cat import CatGateway
from cats.application.common.transaction import Transaction
from cats.application.common.validators import validate_cat
from cats.entities.cat.models import CatID
from cats.entities.cat.services import CatService


@dataclass(frozen=True, slots=True)
class DeleteCatCommand:
    cat_id: int


class DeleteCatCommandHandler:
    def __init__(
        self,
        transaction: Transaction,
        cat_gateway: CatGateway,
        cat_service: CatService,
    ) -> None:
        self._transaction: Final = transaction
        self._cat_gateway: Final = cat_gateway
        self._cat_service: Final = cat_service

    async def run(self, data: DeleteCatCommand) -> None:
        cat = await self._cat_gateway.with_id(CatID(data.cat_id))
        assert validate_cat(cat, data.cat_id)
        await self._cat_service.remove_cat(cat)
        await self._transaction.commit()
