from dataclasses import dataclass
from typing import Final

from cats.application.common.persistence.cat import CatGateway
from cats.application.common.transaction import Transaction
from cats.application.common.validators import validate_cat
from cats.entities.cat.models import CatID
from cats.entities.cat.services import CatService
from cats.entities.cat.value_objects import CatDescription


@dataclass(frozen=True, slots=True)
class UpdateCatDescriptionCommand:
    cat_id: int
    description: str


class UpdateCatDescriptionCommandHandler:
    def __init__(
        self,
        cat_gateway: CatGateway,
        cat_service: CatService,
        transaction: Transaction,
    ) -> None:
        self._cat_gateway: Final = cat_gateway
        self._cat_service: Final = cat_service
        self._transaction: Final = transaction

    async def run(self, data: UpdateCatDescriptionCommand) -> None:
        description = CatDescription(data.description)
        cat = await self._cat_gateway.with_id(CatID(data.cat_id))
        assert validate_cat(cat, data.cat_id)
        self._cat_service.change_description(cat, description)
        await self._transaction.commit()
