import pytest

from cats.entities.breed.models import Breed
from cats.entities.breed.services import BreedService
from cats.entities.breed.value_objects import BreedName
from cats.entities.cat.models import Cat
from cats.entities.cat.services import CatService
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription


@pytest.fixture
def new_cat() -> Cat:
    return CatService.create_cat(
        None,
        CatAge(15),
        CatColor("pink"),
        CatDescription("biba with pink hair"),
    )


@pytest.fixture
def new_breed() -> Breed:
    return BreedService.create_breed(BreedName("boba with cute face"))
