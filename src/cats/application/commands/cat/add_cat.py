from dataclasses import dataclass

from cats.application.common.persistence.breed import BreedGateway
from cats.application.common.transaction import Transaction
from cats.entities.breed.models import Breed, BreedID
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
        breed_gateway: BreedGateway,
        cat_service: CatService,
        breed_service: BreedService,
    ) -> None:
        self._transaction = transaction
        self._breed_gateway = breed_gateway
        self._cat_service = cat_service
        self._breed_service = breed_service

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
        self._cat_service.add_cat(new_cat)
        await self._transaction.commit()
        return new_cat.oid

    async def _get_breed_id(self, breed_name: BreedName) -> BreedID:
        breed = await self._breed_gateway.with_name(breed_name)
        if breed is None:
            breed = await self._create_breed(breed_name)
        return breed.oid

    async def _create_breed(self, breed_name: BreedName) -> Breed:
        new_breed = self._breed_service.create_breed(breed_name)
        self._breed_service.add_breed(new_breed)
        await self._transaction.flush()
        return new_breed
