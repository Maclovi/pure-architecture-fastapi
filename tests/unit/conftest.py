import pytest

from cats.entities.breed.models import Breed
from cats.entities.breed.value_objects import BreedName
from cats.entities.cat.models import Cat
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription


@pytest.fixture
def new_cat() -> Cat:
    return Cat.create_cat(
        None,
        CatAge(15),
        CatColor("pink"),
        CatDescription("biba with pink hair"),
    )


@pytest.fixture
def new_breed() -> Breed:
    return Breed.create_breed(BreedName("boba with cute face"))
