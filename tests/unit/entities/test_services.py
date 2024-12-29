from unittest.mock import AsyncMock, Mock

import pytest

from cats.entities.breed.models import Breed
from cats.entities.breed.services import BreedService
from cats.entities.breed.value_objects import BreedName
from cats.entities.cat.models import Cat
from cats.entities.cat.services import CatService
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription
from cats.entities.common.tracker import Tracker


@pytest.fixture
def fake_tracker() -> Tracker:
    fake = Mock()
    fake.add_one = Mock()
    fake.add_many = Mock()
    fake.delete = AsyncMock()
    return fake


async def test_cat_service(fake_tracker: Mock) -> None:
    service = CatService(fake_tracker)
    new_cat = service.create_cat(
        None,
        CatAge(3),
        CatColor("blue"),
        CatDescription("biba and boba"),
    )
    service.add_cat(new_cat)
    service.change_description(new_cat, CatDescription("new descr"))
    await service.remove_cat(new_cat)

    fake_tracker.add_one.assert_called_once_with(new_cat)
    fake_tracker.delete.assert_called_once_with(new_cat)
    assert new_cat.description.value == "new descr"
    assert isinstance(new_cat, Cat)


async def test_breed_service(fake_tracker: Mock) -> None:
    service = BreedService(fake_tracker)
    new_breed = service.create_breed(BreedName("boba"))
    service.add_breed(new_breed)

    fake_tracker.add_one.assert_called_once_with(new_breed)
    assert new_breed.name.value == "boba"
    assert isinstance(new_breed, Breed)
