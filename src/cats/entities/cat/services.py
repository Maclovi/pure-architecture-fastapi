from typing import cast

from cats.entities.breed.models import BreedID
from cats.entities.cat.models import Cat, CatID
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription
from cats.entities.common.tracker import Tracker


class CatService:
    def __init__(self, tracker: Tracker) -> None:
        self._tracker = tracker

    def new_cat(
        self,
        breed_id: BreedID | None,
        age: int,
        color: str,
        description: str,
    ) -> Cat:
        return Cat(
            oid=cast(CatID, None),
            breed_id=breed_id,
            age=CatAge(age),
            color=CatColor(color),
            description=CatDescription(description),
        )

    def change_description(self, cat: Cat, new: CatDescription) -> None:
        cat.description = new

    def add_cat(self, new_cat: Cat) -> None:
        self._tracker.add_one(new_cat)

    async def remove_cat(self, cat: Cat) -> None:
        await self._tracker.delete(cat)
