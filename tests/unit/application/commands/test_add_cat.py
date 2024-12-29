from unittest.mock import AsyncMock, Mock

import pytest

from cats.application.commands.cat.add_cat import (
    NewCatCommand,
    NewCatCommandHandler,
)
from cats.entities.breed.services import BreedService
from cats.entities.breed.value_objects import BreedName
from cats.entities.cat.services import CatService
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
    fake_breed_gateway: Mock,
    fake_cat_service: Mock,
    fake_breed_service: Mock,
) -> None:
    interactor = NewCatCommandHandler(
        fake_transaction,
        fake_breed_gateway,
        fake_cat_service,
        fake_breed_service,
    )
    await interactor.run(dto)
    cat = CatService.create_cat(
        None,
        CatAge(dto.age),
        CatColor(dto.color),
        CatDescription(dto.description),
    )
    if dto.breed_name:
        breed_name = BreedName(dto.breed_name)
        fake_breed_gateway.with_name.assert_called_once_with(breed_name)
        fake_cat_service.create_cat.assert_called_once_with(
            cat.breed_id,
            cat.age,
            cat.color,
            cat.description,
        )

    fake_cat_service.add_cat.assert_called_once_with(cat)
    fake_transaction.commit.assert_called_once()


async def test_add_breed_gateway_mocked(
    fake_transaction: Mock,
    fake_breed_gateway: Mock,
    fake_cat_service: Mock,
    fake_breed_service: Mock,
) -> None:
    breed_name_raw = "some breed"
    dto = NewCatCommand(3, "red", "some description", breed_name_raw)
    fake_breed_gateway.with_name = AsyncMock(return_value=None)
    interactor = NewCatCommandHandler(
        fake_transaction,
        fake_breed_gateway,
        fake_cat_service,
        fake_breed_service,
    )
    output = await interactor.run(dto)

    assert output is None
    breed = BreedService.create_breed(BreedName(breed_name_raw))
    cat = CatService.create_cat(
        breed.oid,
        CatAge(dto.age),
        CatColor(dto.color),
        CatDescription(dto.description),
    )
    fake_breed_service.create_breed.assert_called_once_with(breed.name)
    fake_cat_service.create_cat.assert_called_once_with(
        cat.breed_id,
        cat.age,
        cat.color,
        cat.description,
    )
    fake_breed_service.add_breed.assert_called_once_with(breed)
    fake_cat_service.add_cat.assert_called_once_with(cat)
    fake_transaction.flush.assert_called_once()
    fake_transaction.commit.assert_called_once()
