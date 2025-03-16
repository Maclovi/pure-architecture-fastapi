from typing import cast

from cats.entities.breed.models import Breed, BreedID
from cats.entities.breed.value_objects import BreedName


class BreedService:
    @staticmethod
    def create_breed(breed_name: BreedName) -> Breed:
        return Breed(
            oid=cast("BreedID", cast("object", None)),
            name=breed_name,
        )
