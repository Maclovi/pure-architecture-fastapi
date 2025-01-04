from typing import Final, cast

from cats.entities.breed.models import Breed, BreedID
from cats.entities.breed.value_objects import BreedName
from cats.entities.common.tracker import Tracker


class BreedService:
    def __init__(self, tracker: Tracker) -> None:
        self._tracker: Final = tracker

    @staticmethod
    def create_breed(breed_name: BreedName) -> Breed:
        return Breed(
            oid=cast(BreedID, cast(object, None)),
            name=breed_name,
        )

    def add_breed(self, breed: Breed) -> None:
        self._tracker.add_one(breed)
