from unittest.mock import Mock

import pytest

from cats.application.commands.cat.delete_cat_by_id import (
    DeleteCatCommand,
    DeleteCatCommandHandler,
)
from cats.application.common.errors.base import EntityNotFoundError
from cats.application.common.errors.cat import CatNotFoundError
from cats.entities.cat.models import Cat, CatID


@pytest.mark.parametrize(
    ("dto", "exc_class"),
    [
        (DeleteCatCommand(1), None),
        (DeleteCatCommand(2), CatNotFoundError),
    ],
)
async def test_delete_cat_with_id(  # noqa: PLR0913
    dto: DeleteCatCommand,
    exc_class: type[EntityNotFoundError] | None,
    fake_transaction: Mock,
    fake_entity_saver: Mock,
    fake_cat_gateway: Mock,
    new_cat: Cat,
) -> None:
    interactor = DeleteCatCommandHandler(
        fake_transaction,
        fake_entity_saver,
        fake_cat_gateway,
    )
    if exc_class:
        fake_cat_gateway.with_id.return_value = None
        with pytest.raises(CatNotFoundError) as excinfo:
            await interactor.run(dto)
        assert excinfo.value.message == f"Cat with id={dto.cat_id} not found"
        fake_entity_saver.remove.assert_not_called()
        fake_transaction.commit.assert_not_called()
    else:
        await interactor.run(dto)
        fake_cat_gateway.with_id.assert_called_once_with(CatID(1))
        fake_entity_saver.delete.assert_called_once_with(new_cat)
        fake_transaction.commit.assert_called_once()
