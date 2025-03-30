from logging import getLogger
from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Query, status

from cats.application.common.persistence.filters import Pagination
from cats.application.queries.breed.get_breeds import (
    BreedsOutput,
    GetBreedsQuery,
    GetBreedsQueryHandler,
)
from cats.presentation.http.v1.common.schemes import PaginationSchema

logger = getLogger(__name__)
router = APIRouter(prefix="/breeds", tags=["Breeds"], route_class=DishkaRoute)


@router.get("/", summary="Get all of breeds", status_code=status.HTTP_200_OK)
async def get_all_breeds(
    query: Annotated[PaginationSchema, Query()],
    interactor: FromDishka[GetBreedsQueryHandler],
) -> BreedsOutput:
    """Retrieve paginated list of all available cat breeds.

    Args:
        query: Pagination parameters containing:
            - offset: Number of items to skip
            - limit: Maximum number of items to return
        interactor: Injected GetBreedsQueryHandler instance
            for processing the request

    Returns:
        BreedsOutput: Paginated result containing:
            - items: List of breed details
            - total: Total number of breeds available
            - offset: Current pagination offset
            - limit: Current pagination limit

    Raises:
        HTTPException:
            - 400: If pagination parameters are invalid
            - 500: If internal server error occurs

    Notes:
        - Requires valid pagination parameters
        - Uses CQRS pattern with GetBreedsQuery
        - Results are always ordered consistently
        - Part of 'Breeds' tag group in OpenAPI docs

    Example request:
        GET /breeds?offset=0&limit=10
    """
    dto = GetBreedsQuery(Pagination(query.offset, query.limit))
    return await interactor.run(dto)
