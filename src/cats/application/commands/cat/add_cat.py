from dataclasses import dataclass
from typing import Final

from cats.application.common.ports.breed import BreedGateway
from cats.application.common.ports.transaction import EntitySaver, Transaction
from cats.entities.breed.models import BreedID
from cats.entities.breed.services import BreedService
from cats.entities.breed.value_objects import BreedName
from cats.entities.cat.models import CatID
from cats.entities.cat.services import CatService
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription


@dataclass(frozen=True, slots=True)
class NewCatCommand:
    age: int
    color: str
    description: str
    breed_name: str | None


class NewCatCommandHandler:
    def __init__(
        self,
        transaction: Transaction,
        entity_saver: EntitySaver,
        breed_gateway: BreedGateway,
        cat_service: CatService,
        breed_service: BreedService,
    ) -> None:
        self._transaction: Final = transaction
        self._entity_saver: Final = entity_saver
        self._breed_gateway: Final = breed_gateway
        self._cat_service: Final = cat_service
        self._breed_service: Final = breed_service

    async def run(self, data: NewCatCommand) -> CatID:
        if data.breed_name:
            breed_id = await self._get_breed_id(BreedName(data.breed_name))
        else:
            breed_id = None
        new_cat = self._cat_service.create_cat(
            breed_id,
            CatAge(data.age),
            CatColor(data.color),
            CatDescription(data.description),
        )
        self._entity_saver.add_one(new_cat)
        await self._transaction.commit()
        return new_cat.oid

    async def _get_breed_id(self, breed_name: BreedName) -> BreedID:
        breed = await self._breed_gateway.with_name(breed_name)
        if breed is None:
            breed = self._breed_service.create_breed(breed_name)
            self._entity_saver.add_one(breed)
            await self._transaction.flush()
        return breed.oid
