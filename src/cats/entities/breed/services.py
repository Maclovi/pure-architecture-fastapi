from typing import cast

from cats.entities.breed.models import Breed, BreedID
from cats.entities.breed.value_objects import BreedName
from cats.entities.common.tracker import Tracker


class BreedService:
    def __init__(self, tracker: Tracker) -> None:
        self._tracker = tracker

    def create_breed(self, breed_name: BreedName) -> Breed:
        return Breed(oid=cast(BreedID, None), name=breed_name)

    def add_breed(self, breed: Breed) -> None:
        self._tracker.add_one(breed)

    async def remove_breed(self, breed: Breed) -> None:
        await self._tracker.delete(breed)
