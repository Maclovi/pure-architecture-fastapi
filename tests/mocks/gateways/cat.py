from cats.application.common.persistence.cat import (
    CatFilters,
    CatGateway,
    CatReader,
)
from cats.application.common.persistence.filters import Pagination
from cats.application.common.persistence.view_models import CatView
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
                None,
                CatAge(50),
                CatColor("red"),
                CatDescription("cat Boba"),
            ),
            CatID(3): Cat(
                CatID(3),
                BreedID(2),
                CatAge(70),
                CatColor("yellow"),
                CatDescription("cat Biba and Boba"),
            ),
        }

    async def with_id(self, cat_id: CatID) -> Cat | None:
        return self.cats.get(cat_id)


class FakeCatReader(CatReader):
    def __init__(self) -> None:
        self.cats = {
            CatID(1): CatView(
                CatID(1),
                "some breed",
                2,
                "blue",
                "cat Biba",
            ),
            CatID(2): CatView(
                CatID(2),
                "some breed",
                50,
                "red",
                "cat Boba",
            ),
            CatID(3): CatView(
                CatID(3),
                "sobaka",
                70,
                "yellow",
                "cat Biba and Boba",
            ),
        }

    async def with_id(self, cat_id: CatID) -> CatView | None:
        return self.cats.get(cat_id)

    async def with_breed_name(
        self,
        breed_name: BreedName,
        pagination: Pagination,
    ) -> list[CatView]:
        if breed_name and pagination:
            pass
        return [*self.cats.values()]

    async def all(
        self,
        filters: CatFilters,
        pagination: Pagination,
    ) -> list[CatView]:
        if filters and pagination:
            pass
        return []
