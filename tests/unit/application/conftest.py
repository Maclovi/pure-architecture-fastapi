from unittest.mock import AsyncMock, Mock

import pytest

from cats.application.common.persistence.breed import BreedGateway
from cats.application.common.persistence.cat import CatGateway, CatReader
from cats.application.common.persistence.view_models import CatView
from cats.application.common.transaction import Transaction
from cats.entities.breed.models import Breed
from cats.entities.breed.services import BreedService
from cats.entities.cat.models import Cat
from cats.entities.cat.services import CatService


@pytest.fixture
def fake_cat_service() -> CatService:
    fake = Mock()
    fake.create_cat = Mock(side_effect=CatService.create_cat)
    fake.change_description = Mock()
    fake.add_cat = Mock()
    fake.remove_cat = AsyncMock()
    return fake


@pytest.fixture
def fake_breed_service() -> BreedService:
    fake = Mock()
    fake.create_breed = Mock(side_effect=BreedService.create_breed)
    fake.add_breed = Mock()
    return fake


@pytest.fixture
def fake_transaction() -> Transaction:
    fake = Mock()
    fake.commit = AsyncMock()
    fake.flush = AsyncMock()
    return fake


@pytest.fixture
def fake_breed_gateway(new_breed: Breed) -> BreedGateway:
    breeds = [new_breed]
    fake = Mock()
    fake.with_id = AsyncMock(return_value=breeds[0])
    fake.with_name = AsyncMock(return_value=breeds[0])
    fake.all = AsyncMock(return_value=breeds)
    return fake


@pytest.fixture
def fake_cat_gateway(new_cat: Cat) -> CatGateway:
    fake = Mock()
    fake.with_id = AsyncMock(return_value=new_cat)
    return fake


@pytest.fixture
def fake_cat_reader() -> CatReader:
    cats = [CatView(1, None, 10, "pink", "some biba")]
    fake = Mock()
    fake.with_id = AsyncMock(return_value=cats[0])
    fake.with_breed_name = AsyncMock(return_value=cats)
    fake.all = AsyncMock(return_value=cats)
    return fake