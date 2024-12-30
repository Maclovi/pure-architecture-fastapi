from unittest.mock import Mock

import pytest

from cats.application.commands.cat.update_cat import (
    UpdateCatDescriptionCommand,
    UpdateCatDescriptionCommandHandler,
)
from cats.application.common.errors.base import EntityNotFoundError
from cats.application.common.errors.cat import CatNotFoundError
from cats.entities.cat.models import Cat, CatID
from cats.entities.cat.value_objects import CatDescription


@pytest.mark.parametrize(
    ("dto", "exc_class"),
    [
        (UpdateCatDescriptionCommand(1, "new desc 1"), None),
        (UpdateCatDescriptionCommand(2, "new desc 2"), CatNotFoundError),
    ],
)
async def test_update_cat_description(  # noqa: PLR0913
    dto: UpdateCatDescriptionCommand,
    exc_class: type[EntityNotFoundError] | None,
    fake_cat_gateway: Mock,
    fake_cat_service: Mock,
    fake_transaction: Mock,
    new_cat: Cat,
) -> None:
    interactor = UpdateCatDescriptionCommandHandler(
        fake_cat_gateway,
        fake_cat_service,
        fake_transaction,
    )
    if exc_class:
        fake_cat_gateway.with_id.return_value = None
        with pytest.raises(CatNotFoundError) as excinfo:
            await interactor.run(dto)
        assert excinfo.value.message == f"Cat with id={dto.cat_id} not found"
        fake_cat_service.change_description.assert_not_called()
        fake_transaction.commit.assert_not_called()
    else:
        await interactor.run(dto)
        fake_cat_gateway.with_id.assert_called_once_with(CatID(dto.cat_id))
        fake_cat_service.change_description.assert_called_once_with(
            new_cat,
            CatDescription(dto.description),
        )
