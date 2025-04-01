from unittest.mock import Mock

import pytest

from cats.application.commands.cat.cat_update import (
    CatUpdate,
    CatUpdateHandler,
)
from cats.application.common.errors.base import EntityNotFoundError
from cats.entities.cat.models import Cat, CatID


@pytest.mark.parametrize(
    ("data", "exc_class"),
    [
        (
            CatUpdate(2, age=2, color="white", description="new desc 2"),
            EntityNotFoundError,
        ),
        (CatUpdate(1, age=1, color="blue", description="new desc 1"), None),
        (CatUpdate(1, age=None, color=None, description=None), None),
    ],
)
async def test_update_cat_description(
    data: CatUpdate,
    exc_class: type[EntityNotFoundError] | None,
    fake_cat_gateway: Mock,
    fake_transaction: Mock,
) -> None:
    cat: Cat = fake_cat_gateway.with_id.return_value
    assert cat.description.value == "biba with pink hair"

    interactor = CatUpdateHandler(fake_cat_gateway, fake_transaction)
    if exc_class:
        fake_cat_gateway.with_id.return_value = None
        with pytest.raises(EntityNotFoundError) as excinfo:
            await interactor.run(data)
        assert (
            excinfo.value.message == f"Entity with id={data.cat_id} not found"
        )
        fake_transaction.commit.assert_not_called()
    else:
        await interactor.run(data)

        fake_cat_gateway.with_id.assert_called_once_with(CatID(data.cat_id))

        if data.age is not None:
            assert cat.age.value == data.age
        if data.color is not None:
            assert cat.color.value == data.color
        if data.description is not None:
            assert cat.description.value == data.description

        fake_transaction.commit.assert_called_once_with()
