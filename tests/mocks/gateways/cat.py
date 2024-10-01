from cats.application.common.persistence.cat import CatFilters, CatGateway
from cats.application.common.persistence.filters import Pagination
from cats.entities.breed.models import BreedID
from cats.entities.breed.value_objects import BreedName
from cats.entities.cat.models import Cat, CatID
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription


class FakeCatGateway(CatGateway):
    def __init__(self) -> None:
        self.cats = {
            CatID(1): Cat(
                CatID(1),
                BreedID(1),
                CatAge(2),
                CatColor("blue"),
                CatDescription("cat Biba"),
            ),
            CatID(2): Cat(
                CatID(2),
                BreedID(2),
                CatAge(50),
                CatColor("red"),
                CatDescription("cat Boba"),
            ),
            CatID(3): Cat(
                CatID(3),
                BreedID(1),
                CatAge(70),
                CatColor("yellow"),
                CatDescription("cat Biba and Boba"),
            ),
        }

    async def with_id(self, cat_id: CatID) -> Cat | None:
        return self.cats.get(cat_id)

    async def with_breed_name(
        self,
        breed_name: BreedName,
        pagination: Pagination,
    ) -> list[Cat]:
        if breed_name and pagination:
            pass
        return [*self.cats.values()]

    async def all(
        self, filters: CatFilters, pagination: Pagination
    ) -> list[Cat]:
        if filters and pagination:
            pass
        return []
