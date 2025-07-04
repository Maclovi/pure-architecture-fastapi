from dataclasses import dataclass
from typing import NewType, cast

from typing_extensions import Self

from cats.entities.breed.models import BreedID
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription
from cats.entities.common.base_entity import BaseEntity

CatID = NewType("CatID", int)


@dataclass
class Cat(BaseEntity[CatID]):
    breed_id: BreedID | None
    age: CatAge
    color: CatColor
    description: CatDescription

    def change_age(self, new_age: CatAge) -> None:
        self.age = new_age

    def change_color(self, new_color: CatColor) -> None:
        self.color = new_color

    def change_description(self, new: CatDescription) -> None:
        self.description = new

    @classmethod
    def create_cat(
        cls,
        breed_id: BreedID | None,
        age: CatAge,
        color: CatColor,
        description: CatDescription,
    ) -> Self:
        return cls(
            oid=cast("CatID", cast("object", None)),
            breed_id=breed_id,
            age=age,
            color=color,
            description=description,
        )
