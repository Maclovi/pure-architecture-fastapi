from logging import getLogger
from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Query, status

from cats.application.common.ports.filters import Pagination
from cats.application.queries.breed.get_breeds import (
    BreedsOutput,
    GetBreedsQuery,
    GetBreedsQueryHandler,
)
from cats.presentation.http.common.schemes import PaginationSchema

logger = getLogger(__name__)
router = APIRouter(prefix="/breeds", tags=["Breeds"], route_class=DishkaRoute)


@router.get("/", summary="Get all of breeds", status_code=status.HTTP_200_OK)
async def get_all_breeds(
    query: Annotated[PaginationSchema, Query()],
    interactor: FromDishka[GetBreedsQueryHandler],
) -> BreedsOutput:
    dto = GetBreedsQuery(Pagination(query.offset, query.limit))
    return await interactor.run(dto)
