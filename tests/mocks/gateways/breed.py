from cats.application.common.persistence.breed import BreedGateway
from cats.application.common.persistence.filters import Pagination
from cats.entities.breed.models import Breed, BreedID
from cats.entities.breed.value_objects import BreedName


class FakeBreedGateway(BreedGateway):
    def __init__(self) -> None:
        self.breeds = {
            BreedID(1): Breed(BreedID(1), BreedName("Bibo")),
            BreedID(2): Breed(BreedID(2), BreedName("Boba")),
            BreedID(3): Breed(BreedID(3), BreedName("Smell")),
        }

    async def with_id(self, breed_id: BreedID) -> Breed | None:
        return self.breeds.get(breed_id)

    async def with_name(self, name: BreedName) -> Breed | None:
        for breed in self.breeds.values():
            if breed.name.value == name.value:
                return breed
        return None

    async def all(self, pagination: Pagination) -> list[Breed]:
        results = [*self.breeds.values()]
        if pagination.offset:
            results = results[pagination.offset :]
        if pagination.limit:
            results = results[: pagination.limit]
        return results
