from unittest.mock import Mock

from cats.application.common.persistence.filters import Pagination
from cats.application.common.persistence.view_models import CatView
from cats.application.queries.cat.get_cats_by_breed import (
    GetCatsWithBreedQuery,
    GetCatsWithBreedQueryHandler,
)
from cats.entities.breed.value_objects import BreedName


async def test_get_cats_by_breed(fake_cat_reader: Mock) -> None:
    dto = GetCatsWithBreedQuery("some breed", Pagination())
    interactor = GetCatsWithBreedQueryHandler(fake_cat_reader)
    results = await interactor.run(dto)

    assert results.total == 1
    assert len(results.cats) > 0
    assert all(isinstance(cat, CatView) for cat in results.cats)
    fake_cat_reader.with_breed_name.assert_called_once_with(
        BreedName(dto.breed_name),
        dto.pagination,
    )
