from logging import getLogger
from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Path, Query, status

from cats.application.commands.cat.add_cat import (
    NewCatCommand,
    NewCatCommandHandler,
)
from cats.application.commands.cat.delete_cat_by_id import (
    DeleteCatCommand,
    DeleteCatCommandHandler,
)
from cats.application.commands.cat.update_cat import (
    UpdateCatDescriptionCommand,
    UpdateCatDescriptionCommandHandler,
)
from cats.application.common.ports.cat import CatFilters
from cats.application.common.ports.filters import Pagination
from cats.application.queries.cat.get_cat_by_id import (
    CatOutput,
    GetCatWithIDQuery,
    GetCatWithIDQueryHandler,
)
from cats.application.queries.cat.get_cats import (
    GetCatsQuery,
    GetCatsQueryHandler,
)
from cats.application.queries.cat.get_cats_by_breed import (
    GetCatsWithBreedQuery,
    GetCatsWithBreedQueryHandler,
)
from cats.application.queries.cat.output_shared import CatsOutput
from cats.presentation.http.common.schemes import (
    CatsAllSchema,
    CatsWithBreedSchema,
    ExceptionSchema,
)

logger = getLogger(__name__)
router = APIRouter(prefix="/cats", tags=["Cats"], route_class=DishkaRoute)


@router.get("/", summary="Get all cats", status_code=status.HTTP_200_OK)
async def get_all(
    query: Annotated[CatsAllSchema, Query()],
    interactor: FromDishka[GetCatsQueryHandler],
) -> CatsOutput:
    dto = GetCatsQuery(
        CatFilters(query.breed, query.color),
        Pagination(query.offset, query.limit, query.order),
    )
    return await interactor.run(dto)


@router.get(
    "/breed/{breed}",
    summary="Get cats by breed",
    status_code=status.HTTP_200_OK,
)
async def get_by_breed(
    query: Annotated[CatsWithBreedSchema, Path()],
    interactor: FromDishka[GetCatsWithBreedQueryHandler],
) -> CatsOutput:
    dto = GetCatsWithBreedQuery(
        query.breed,
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
    return await interactor.run(GetCatWithIDQuery(oid))


@router.post("/add", summary="Add cat", status_code=status.HTTP_201_CREATED)
async def add(
    command_data: NewCatCommand,
    interactor: FromDishka[NewCatCommandHandler],
) -> int:
    return await interactor.run(command_data)


@router.patch(
    "/update_description/",
    summary="Update cat",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema}},
)
async def update_description(
    command_data: UpdateCatDescriptionCommand,
    interactor: FromDishka[UpdateCatDescriptionCommandHandler],
) -> None:
    return await interactor.run(command_data)


@router.delete(
    "/delete/{id}",
    summary="Delete cat by id",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema}},
)
async def delete_by_id(
    oid: Annotated[int, Path(alias="id")],
    interactor: FromDishka[DeleteCatCommandHandler],
) -> None:
    dto = DeleteCatCommand(oid)
    await interactor.run(dto)
