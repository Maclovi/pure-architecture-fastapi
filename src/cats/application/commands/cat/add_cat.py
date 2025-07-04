from dataclasses import dataclass
from typing import final

from cats.application.common.persistence.breed import BreedGateway
from cats.application.common.persistence.transaction import (
    EntitySaver,
    Transaction,
)
from cats.entities.breed.models import Breed, BreedID
from cats.entities.breed.value_objects import BreedName
from cats.entities.cat.models import Cat, CatID
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription


@dataclass(frozen=True, slots=True)
class NewCatCommand:
    age: int
    color: str
    description: str
    breed_name: str | None


@final
class NewCatCommandHandler:
    def __init__(
        self,
        transaction: Transaction,
        entity_saver: EntitySaver,
        breed_gateway: BreedGateway,
    ) -> None:
        self._transaction = transaction
        self._entity_saver = entity_saver
        self._breed_gateway = breed_gateway

    async def run(self, data: NewCatCommand) -> CatID:
        if data.breed_name:
            breed_id = await self._get_breed_id(BreedName(data.breed_name))
        else:
            breed_id = None
        new_cat = Cat.create_cat(
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
            breed = Breed.create_breed(breed_name)
            self._entity_saver.add_one(breed)
            await self._transaction.flush()
        return breed.oid
