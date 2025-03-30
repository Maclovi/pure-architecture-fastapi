from typing import Any, Final, cast

from sqlalchemy import RowMapping, Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

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
    """SQLAlchemy implementation of the CatGateway interface.

    Provides asynchronous database access for
        Cat entities using SQLAlchemy Core,
    handling write operations and full entity retrieval.

    Args:
        session: Async database session for executing queries.

    Note:
        - Implements all required CatGateway operations
        - Works with full Cat domain entities
        - Uses SQLAlchemy Core for maximum performance
        - Follows repository pattern for write operations
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initializes the mapper with an async database session.

        Args:
            session: Async SQLAlchemy session for database operations.
        """
        self._session: Final = session

    @override
    async def with_id(self, cat_id: CatID) -> Cat | None:
        """Retrieves a full Cat entity by its unique identifier.

        Args:
            cat_id: CatID to search for.

        Returns:
            Cat | None: The matching Cat entity if found, None otherwise.

        Note:
            - Returns the complete aggregate root with all relationships
            - Suitable for write operations and business logic
            - Uses SQLAlchemy Core select operation
        """
        stmt = select(Cat).where(cats_table.c.cat_id == cat_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()


class CatReaderAlchemy(CatReader):
    """SQLAlchemy implementation of the CatReader interface.

    Provides optimized read-only access for
        Cat view models using SQLAlchemy Core,
        with support for joins, filtering and pagination.

    Args:
        session: Async database session for executing queries.

    Note:
        - Implements all required CatReader operations
        - Returns lightweight CatView objects
        - Supports complex queries with joins and filtering
        - Optimized for read performance
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initializes the reader with an async database session.

        Args:
            session: Async SQLAlchemy session for database operations.
        """
        self._session: Final = session

    def _make_join(self, *, isouter: bool = False) -> Select[tuple[Any, ...]]:  # pyright: ignore[reportExplicitAny]
        """Constructs a base JOIN query between cats and breeds tables.

        Args:
            isouter: If True, performs a LEFT OUTER JOIN instead of INNER JOIN.

        Returns:
            Select: Configured SQLAlchemy select statement with joined tables.

        Note:
            - Selects all required fields for CatView construction
            - Allows control over join type for optional breed relationship
        """
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
        """Converts a database row into a CatView object.

        Args:
            row: Raw database row from joined cats/breeds query.

        Returns:
            CatView: Populated view model with all required fields.

        Note:
            - Handles type casting of raw database values
            - Manages optional breed_name field
            - Creates lightweight view objects
        """
        return CatView(
            cast("int", row.cat_id),
            cast("str | None", row.breed_name),
            cast("int", row.cat_age),
            cast("str", row.cat_color),
            cast("str", row.cat_description),
        )

    @override
    async def with_id(self, cat_id: CatID) -> CatView | None:
        """Retrieves a CatView by its unique identifier.

        Args:
            cat_id: CatID to search for.

        Returns:
            CatView | None: The matching view model if found, None otherwise.

        Note:
            - Uses LEFT OUTER JOIN to handle cats without breeds
            - Returns lightweight view object
            - Optimized for read operations
        """
        stmt = self._make_join(isouter=True).where(
            cats_table.c.cat_id == cat_id,
        )
        result = await self._session.execute(stmt)
        row = result.mappings().one_or_none()
        return self._load_catview(row) if row else None

    @override
    async def all(
        self,
        filters: CatFilters,
        pagination: Pagination,
    ) -> list[CatView]:
        """Retrieves paginated and filtered list of CatView objects.

        Args:
            filters: CatFilters containing breed and color criteria.
            pagination: Pagination parameters for offset/limit.

        Returns:
            list[CatView]: List of view models matching the criteria.

        Note:
            - Applies both filtering and pagination
            - Uses LEFT OUTER JOIN for optional breed relationship
            - Returns empty list if no matches found
            - Efficiently loads only required fields
        """
        stmt = self._make_join(isouter=True)
        if filters.breed:
            stmt = stmt.where(breeds_table.c.breed_name == filters.breed)
        if filters.color:
            stmt = stmt.where(cats_table.c.color == filters.color)

        if pagination.offset:
            stmt = stmt.offset(pagination.offset)
        if pagination.limit:
            stmt = stmt.limit(pagination.limit)

        result = await self._session.execute(stmt)
        return [self._load_catview(row) for row in result.mappings()]

    @override
    async def with_breed_name(
        self,
        breed_name: BreedName,
        pagination: Pagination,
    ) -> list[CatView]:
        """Retrieves cats belonging to a specific breed with pagination.

        Args:
            breed_name: BreedName to filter by.
            pagination: Pagination parameters for offset/limit.

        Returns:
            list[CatView]: List of view models for cats of the specified breed.

        Note:
            - Uses INNER JOIN since breed is required
            - Applies pagination
            - Returns empty list if no matches found
            - More efficient than generic all() when filtering by breed
        """
        stmt = self._make_join(isouter=True)
        stmt = stmt.where(breeds_table.c.breed_name == breed_name.value)
        if pagination.offset:
            stmt = stmt.offset(pagination.offset)
        if pagination.limit:
            stmt = stmt.limit(pagination.limit)

        result = await self._session.execute(stmt)
        return [self._load_catview(row) for row in result.mappings()]
