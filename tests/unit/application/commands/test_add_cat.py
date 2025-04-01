from unittest.mock import Mock

import pytest

from cats.application.commands.cat.add_cat import (
    NewCatCommand,
    NewCatCommandHandler,
)
from cats.entities.breed.models import Breed
from cats.entities.breed.value_objects import BreedName
from cats.entities.cat.models import Cat
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription


@pytest.mark.parametrize(
    ("dto"),
    [
        NewCatCommand(1, "yellow", "some description 1", "random breed 1"),
        NewCatCommand(2, "black", "some description 2", None),
    ],
)
async def test_add_cat(
    dto: NewCatCommand,
    fake_transaction: Mock,
    fake_entity_saver: Mock,
    fake_breed_gateway: Mock,
) -> None:
    interactor = NewCatCommandHandler(
        fake_transaction,
        fake_entity_saver,
        fake_breed_gateway,
    )
    cat_id = await interactor.run(dto)
    cat = Cat.create_cat(
        None,
        CatAge(dto.age),
        CatColor(dto.color),
        CatDescription(dto.description),
    )
    if dto.breed_name:
        breed_name = BreedName(dto.breed_name)
        fake_breed_gateway.with_name.assert_called_once_with(breed_name)
        assert isinstance(cat, Cat)

    fake_entity_saver.add_one.assert_called_once_with(cat)
    fake_transaction.commit.assert_called_once()
    assert cat_id is None


async def test_add_breed_gateway_mocked(
    fake_transaction: Mock,
    fake_entity_saver: Mock,
    fake_breed_gateway: Mock,
) -> None:
    breed_name_raw = "some breed"
    dto = NewCatCommand(3, "red", "some description", breed_name_raw)
    fake_breed_gateway.with_name.return_value = None
    interactor = NewCatCommandHandler(
        fake_transaction,
        fake_entity_saver,
        fake_breed_gateway,
    )
    output = await interactor.run(dto)

    breed = Breed.create_breed(BreedName(breed_name_raw))
    cat = Cat.create_cat(
        breed.oid,
        CatAge(dto.age),
        CatColor(dto.color),
        CatDescription(dto.description),
    )
    assert isinstance(breed, Breed)
    assert isinstance(cat, Cat)
    fake_entity_saver.add_one.assert_called()
    fake_transaction.flush.assert_called_once()
    fake_transaction.commit.assert_called_once()
    assert output is None
