from dataclasses import dataclass
from typing import NewType, cast

from typing_extensions import Self

from cats.entities.breed.value_objects import BreedName
from cats.entities.common.base_entity import BaseEntity

BreedID = NewType("BreedID", int)


@dataclass
class Breed(BaseEntity[BreedID]):
    name: BreedName

    @classmethod
    def create_breed(cls, breed_name: BreedName) -> Self:
        return cls(
            oid=cast("BreedID", cast("object", None)),
            name=breed_name,
        )
