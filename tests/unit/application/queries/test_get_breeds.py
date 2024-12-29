from unittest.mock import Mock

from cats.application.common.persistence.filters import Pagination
from cats.application.queries.breed.get_breeds import (
    GetBreedsQuery,
    GetBreedsQueryHandler,
)
from cats.entities.breed.models import Breed


async def test_get_breeds(fake_breed_gateway: Mock, new_breed: Breed) -> None:
    dto = GetBreedsQuery(Pagination())
    interactor = GetBreedsQueryHandler(fake_breed_gateway)
    results = await interactor.run(dto)

    assert results.total == 1
    assert len(results.breeds) > 0
    assert results.breeds[0] == new_breed
    fake_breed_gateway.all.assert_called_once_with(dto.pagination)
