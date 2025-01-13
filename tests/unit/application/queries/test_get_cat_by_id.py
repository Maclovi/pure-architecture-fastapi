from unittest.mock import Mock

import pytest

from cats.application.common.errors.base import EntityNotFoundError
from cats.application.common.errors.cat import CatNotFoundError
from cats.application.common.ports.view_models import CatView
from cats.application.queries.cat.get_cat_by_id import (
    GetCatWithIDQuery,
    GetCatWithIDQueryHandler,
)
from cats.entities.cat.models import CatID


@pytest.mark.parametrize(
    ("dto", "exc_class"),
    [
        (GetCatWithIDQuery(1), None),
        (GetCatWithIDQuery(2), CatNotFoundError),
    ],
)
async def test_get_cat_with_id(
    dto: GetCatWithIDQuery,
    exc_class: type[EntityNotFoundError] | None,
    fake_cat_reader: Mock,
) -> None:
    interactor = GetCatWithIDQueryHandler(fake_cat_reader)
    if exc_class:
        fake_cat_reader.with_id.return_value = None
        with pytest.raises(CatNotFoundError) as exinfo:
            _ = await interactor.run(dto)
        assert exinfo.value.message == f"Cat with id={dto.id} not found"
    else:
        result = await interactor.run(dto)
        assert isinstance(result.cat, CatView)
    fake_cat_reader.with_id.assert_called_once_with(CatID(dto.id))
