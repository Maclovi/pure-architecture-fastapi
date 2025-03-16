from typing import cast

from cats.entities.breed.models import BreedID
from cats.entities.cat.models import Cat, CatID
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription


class CatService:
    @staticmethod
    def create_cat(
        breed_id: BreedID | None,
        age: CatAge,
        color: CatColor,
        description: CatDescription,
    ) -> Cat:
        return Cat(
            oid=cast("CatID", cast("object", None)),
            breed_id=breed_id,
            age=age,
            color=color,
            description=description,
        )
