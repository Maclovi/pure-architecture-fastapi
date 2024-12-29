from unittest.mock import AsyncMock, Mock

import pytest

from cats.application.commands.cat.update_cat import (
    UpdateCatDescriptionCommand,
    UpdateCatDescriptionCommandHandler,
)
from cats.application.common.errors.cat import CatNotFoundError
from cats.entities.cat.models import Cat, CatID
from cats.entities.cat.value_objects import CatDescription


async def test_update_cat_description(
    fake_cat_gateway: Mock,
    fake_cat_service: Mock,
    fake_transaction: Mock,
    new_cat: Cat,
) -> None:
    dto = UpdateCatDescriptionCommand(cat_id=1, description="new desc")
    interactor = UpdateCatDescriptionCommandHandler(
        fake_cat_gateway,
        fake_cat_service,
        fake_transaction,
    )
    await interactor.run(dto)
    fake_cat_gateway.with_id.assert_called_once_with(CatID(dto.cat_id))
    fake_cat_service.change_description.assert_called_once_with(
        new_cat,
        CatDescription(dto.description),
    )


async def test_update_cat_descruption_noncat(
    fake_cat_gateway: Mock,
    fake_cat_service: Mock,
    fake_transaction: Mock,
) -> None:
    fake_cat_gateway.with_id = AsyncMock(return_value=None)
    dto = UpdateCatDescriptionCommand(cat_id=1, description="new desc")
    interactor = UpdateCatDescriptionCommandHandler(
        fake_cat_gateway,
        fake_cat_service,
        fake_transaction,
    )
    with pytest.raises(CatNotFoundError):
        await interactor.run(dto)
    fake_cat_service.change_description.assert_not_called()
    fake_transaction.commit.assert_not_called()
