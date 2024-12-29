from unittest.mock import Mock

from cats.application.common.persistence.cat import CatFilters
from cats.application.common.persistence.filters import Pagination
from cats.application.common.persistence.view_models import CatView
from cats.application.queries.cat.get_cats import (
    GetCatsQuery,
    GetCatsQueryHandler,
)


async def test_get_cats(fake_cat_reader: Mock) -> None:
    dto = GetCatsQuery(CatFilters(), Pagination())
    interactor = GetCatsQueryHandler(fake_cat_reader)
    results = await interactor.run(dto)

    assert results.total == 1
    assert len(results.cats) > 0
    assert all(isinstance(cat, CatView) for cat in results.cats)
    fake_cat_reader.all.assert_called_once_with(dto.filters, dto.pagination)
