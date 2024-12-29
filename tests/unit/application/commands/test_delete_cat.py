from unittest.mock import Mock

import pytest

from cats.application.commands.cat.delete_cat_by_id import (
    DeleteCatCommand,
    DeleteCatCommandHandler,
)
from cats.application.common.errors.cat import CatNotFoundError
from cats.entities.cat.models import Cat, CatID


async def test_delete_cat_with_id(
    fake_transaction: Mock,
    fake_cat_gateway: Mock,
    fake_cat_service: Mock,
    new_cat: Cat,
) -> None:
    dto = DeleteCatCommand(1)
    interactor = DeleteCatCommandHandler(
        fake_transaction,
        fake_cat_gateway,
        fake_cat_service,
    )
    await interactor.run(dto)
    fake_cat_gateway.with_id.assert_called_once_with(CatID(1))
    fake_cat_service.remove_cat.assert_called_once_with(new_cat)
    fake_transaction.commit.assert_called_once()


async def test_delete_cat_with_id_noncat(
    fake_transaction: Mock,
    fake_cat_gateway: Mock,
    fake_cat_service: Mock,
) -> None:
    fake_cat_gateway.with_id.return_value = None
    dto = DeleteCatCommand(2)
    interactor = DeleteCatCommandHandler(
        fake_transaction,
        fake_cat_gateway,
        fake_cat_service,
    )
    with pytest.raises(CatNotFoundError) as excinfo:
        await interactor.run(dto)

    assert excinfo.value.message == f"Cat with id={dto.cat_id} not found"
    fake_cat_service.remove_cat.assert_not_called()
    fake_transaction.commit.assert_not_called()
