from typing import Final, cast

from cats.entities.breed.models import BreedID
from cats.entities.cat.models import Cat, CatID
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription
from cats.entities.common.tracker import Tracker


class CatService:
    def __init__(self, tracker: Tracker) -> None:
        self._tracker: Final = tracker

    @staticmethod
    def create_cat(
        breed_id: BreedID | None,
        age: CatAge,
        color: CatColor,
        description: CatDescription,
    ) -> Cat:
        return Cat(
            oid=cast(CatID, cast(object, None)),
            breed_id=breed_id,
            age=age,
            color=color,
            description=description,
        )

    def change_description(self, cat: Cat, new: CatDescription) -> None:
        cat.description = new

    def add_cat(self, new_cat: Cat) -> None:
        self._tracker.add_one(new_cat)

    async def remove_cat(self, cat: Cat) -> None:
        await self._tracker.delete(cat)
