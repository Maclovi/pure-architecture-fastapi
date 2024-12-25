from typing import Any

from sqlalchemy import RowMapping, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from cats.application.common.persistence.cat import (
    CatFilters,
    CatGateway,
    CatReader,
)
from cats.application.common.persistence.filters import Pagination
from cats.application.common.persistence.view_models import CatView
from cats.entities.breed.value_objects import BreedName
from cats.entities.cat.models import Cat, CatID
from cats.infrastructure.persistence.models.breed import breeds_table
from cats.infrastructure.persistence.models.cat import cats_table


class CatMapperAlchemy(CatGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def with_id(self, cat_id: CatID) -> Cat | None:
        stmt = select(Cat).where(cats_table.c.cat_id == cat_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()


class CatReaderAlchemy(CatReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _make_join(self, *, isouter: bool = False) -> Select[tuple[Any, ...]]:
        return select(
            cats_table.c.cat_id,
            cats_table.c.cat_age,
            cats_table.c.cat_color,
            cats_table.c.cat_description,
            breeds_table.c.breed_name,
        ).join(
            breeds_table,
            cats_table.c.breed_id == breeds_table.c.breed_id,
            isouter=isouter,
        )

    def _load_catview(self, row: RowMapping) -> CatView:
        return CatView(
            row.cat_id,
            row.breed_name,
            row.cat_age,
            row.cat_color,
            row.cat_description,
        )

    async def all(
        self,
        filters: CatFilters,
        pagination: Pagination,
    ) -> list[CatView]:
        stmt = self._make_join(isouter=True)
        if filters.breed:
            stmt = stmt.where(breeds_table.c.breed_id == filters.breed)
        if filters.color:
            stmt = stmt.where(cats_table.c.color == filters.color)

        if pagination.offset:
            stmt = stmt.offset(pagination.offset)
        if pagination.limit:
            stmt = stmt.limit(pagination.limit)

        result = await self._session.execute(stmt)
        return [self._load_catview(row) for row in result.mappings()]

    async def with_breed_name(
        self,
        breed_name: BreedName,
        pagination: Pagination,
    ) -> list[CatView]:
        stmt = self._make_join(isouter=True)
        stmt = stmt.where(breeds_table.c.breed_name == breed_name.value)
        if pagination.offset:
            stmt = stmt.offset(pagination.offset)
        if pagination.limit:
            stmt = stmt.limit(pagination.limit)

        result = await self._session.execute(stmt)
        return [self._load_catview(row) for row in result.mappings()]
