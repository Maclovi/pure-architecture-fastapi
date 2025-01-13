from unittest.mock import Mock

import pytest

from cats.application.commands.cat.update_cat import (
    UpdateCatDescriptionCommand,
    UpdateCatDescriptionCommandHandler,
)
from cats.application.common.errors.base import EntityNotFoundError
from cats.application.common.errors.cat import CatNotFoundError
from cats.entities.cat.models import CatID


@pytest.mark.parametrize(
    ("dto", "exc_class"),
    [
        (UpdateCatDescriptionCommand(1, "new desc 1"), None),
        (UpdateCatDescriptionCommand(2, "new desc 2"), CatNotFoundError),
    ],
)
async def test_update_cat_description(
    dto: UpdateCatDescriptionCommand,
    exc_class: type[EntityNotFoundError] | None,
    fake_cat_gateway: Mock,
    fake_transaction: Mock,
) -> None:
    assert (
        fake_cat_gateway.with_id.return_value.description.value
        == "biba with pink hair"
    )
    interactor = UpdateCatDescriptionCommandHandler(
        fake_cat_gateway,
        fake_transaction,
    )
    if exc_class:
        fake_cat_gateway.with_id.return_value = None
        with pytest.raises(CatNotFoundError) as excinfo:
            await interactor.run(dto)
        assert excinfo.value.message == f"Cat with id={dto.cat_id} not found"
        fake_transaction.commit.assert_not_called()
    else:
        await interactor.run(dto)
        fake_cat_gateway.with_id.assert_called_once_with(CatID(dto.cat_id))
        assert (
            fake_cat_gateway.with_id.return_value.description.value
            == dto.description
        )
        fake_transaction.commit.assert_called_once_with()
