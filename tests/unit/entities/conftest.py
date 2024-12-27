import pytest

from cats.entities.breed.models import Breed, BreedID
from cats.entities.breed.value_objects import BreedName
from cats.entities.cat.models import Cat, CatID
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription


@pytest.fixture
def new_cat() -> Cat:
    return Cat(
        CatID(1),
        BreedID(1),
        CatAge(3),
        CatColor("red"),
        CatDescription("biba"),
    )


@pytest.fixture
def new_breed() -> Breed:
    return Breed(BreedID(1), BreedName("boba"))
