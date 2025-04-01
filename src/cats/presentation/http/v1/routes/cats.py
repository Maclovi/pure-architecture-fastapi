from logging import getLogger
from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path, Query, status

from cats.application.commands.cat.add_cat import (
    NewCatCommand,
    NewCatCommandHandler,
)
from cats.application.commands.cat.cat_update import (
    CatUpdate,
    CatUpdateHandler,
)
from cats.application.commands.cat.delete_cat_by_id import (
    DeleteCatCommand,
    DeleteCatCommandHandler,
)
from cats.application.common.persistence.cat import CatFilters
from cats.application.common.persistence.filters import Pagination
from cats.application.queries.cat.get_cat_by_id import (
    CatOutput,
    GetCatWithIDQuery,
    GetCatWithIDQueryHandler,
)
from cats.application.queries.cat.get_cats import (
    GetCatsQuery,
    GetCatsQueryHandler,
)
from cats.application.queries.cat.output_shared import CatsOutput
from cats.presentation.http.v1.common.schemes import (
    CatsAllSchema,
    CatUpdateSchema,
    ExceptionSchema,
)

logger = getLogger(__name__)
router = APIRouter(prefix="/cats", tags=["Cats"], route_class=DishkaRoute)


@router.get("/", summary="Get all cats", status_code=status.HTTP_200_OK)
async def get_all(
    query: Annotated[CatsAllSchema, Query()],
    interactor: FromDishka[GetCatsQueryHandler],
) -> CatsOutput:
    """Retrieve paginated and filtered list of cats.

    Args:
        query: Combined filter and pagination parameters containing:
            - breed: Optional breed name filter (case-insensitive)
            - color: Optional color filter (case-insensitive)
            - offset: Number of items to skip (default: 0)
            - limit: Maximum items per page (default: 10)
            - order: Sort direction (ASC or DESC, default: ASC)
        interactor: Injected GetCatsQueryHandler instance

    Returns:
        CatsOutput: Paginated result containing:
            - items: List of cat records with full details
            - total: Total count of matching records
            - offset: Actual offset used
            - limit: Actual limit used

    Raises:
        HTTPException:
            400: If invalid pagination or filter parameters provided

    Example:
        GET /cats?breed=siamese&color=white&offset=0&limit=10
    """
    dto = GetCatsQuery(
        CatFilters(query.breed, query.color),
        Pagination(query.offset, query.limit, query.order),
    )
    return await interactor.run(dto)


@router.get(
    "/{id}",
    summary="Get cat by id",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema}},
)
async def get_by_id(
    oid: Annotated[int, Path(alias="id")],
    interactor: FromDishka[GetCatWithIDQueryHandler],
) -> CatOutput:
    """Retrieve detailed information about a specific cat.

    Args:
        oid: Unique numeric identifier of the cat (from URL path)
        interactor: Injected GetCatWithIDQueryHandler instance

    Returns:
        CatOutput: Complete cat details including:
            - Identification information
            - Physical attributes
            - Breed details (if applicable)
            - Description

    Raises:
        HTTPException:
            404: If no cat exists with the specified ID
            400: If invalid ID format provided

    Example:
        GET /cats/123
    """
    return await interactor.run(GetCatWithIDQuery(oid))


@router.post("/", summary="Add cat", status_code=status.HTTP_201_CREATED)
async def add(
    command_data: NewCatCommand,
    interactor: FromDishka[NewCatCommandHandler],
) -> int:
    """Create a new cat record in the system.

    Args:
        command_data: New cat creation data containing:
            - name: Cat's name (2-50 characters)
            - breed: Optional breed name (if purebred)
            - color: Primary coat color (3-50 characters)
            - age: Age in years (0-99)
            - description: Optional description (max 1000 chars)
        interactor: Injected NewCatCommandHandler instance

    Returns:
        int: The unique numeric ID assigned to the new cat

    Raises:
        HTTPException:
            400: If any validation rules are violated
            422: If invalid request body format

    Example:
        POST /cats
        {
            "name": "Whiskers",
            "breed": "Siamese",
            "color": "White",
            "age": 3,
            "description": "Very vocal"
        }
    """
    return await interactor.run(command_data)


@router.patch(
    "/{id}",
    summary="Update cat",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema}},
)
async def update_cat(
    oid: Annotated[int, Path(alias="id")],
    data: CatUpdateSchema,
    interactor: FromDishka[CatUpdateHandler],
) -> None:
    """Updates attributes of an existing cat record.

    Args:
        oid: Path parameter containing the cat's unique identifier.
        command_data: Update payload containing:
            - age: Optional new age value (if provided)
            - color: Optional new color description (if provided)
            - description: Optional new text (if provided)
        interactor: Injected CatUpdateHandler for processing the command.

    Raises:
        HTTPException:
            404: If no cat exists with the specified ID
            422: If request format is invalid and any field fails validation

    Example:
        PATCH /cats/123
        {
            "age": 5,
            "color": "tabby",
            "description": "Very playful"
        }
    """
    return await interactor.run(
        CatUpdate(
            cat_id=oid,
            age=data.age,
            color=data.color,
            description=data.description,
        ),
    )


@router.delete(
    "/{id}",
    summary="Delete cat by id",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema}},
)
async def delete_by_id(
    oid: Annotated[int, Path(alias="id")],
    interactor: FromDishka[DeleteCatCommandHandler],
) -> None:
    """Permanently delete a cat record from the system.

    Args:
        oid: Unique numeric identifier of the cat to delete
        interactor: Injected DeleteCatCommandHandler instance

    Raises:
        HTTPException:
            404: If no cat exists with the specified ID
            400: If invalid ID format provided

    Note:
        This operation is irreversible. The cat record and all associated
        data will be permanently removed.

    Example:
        DELETE /cats/123
    """
    dto = DeleteCatCommand(oid)
    await interactor.run(dto)
