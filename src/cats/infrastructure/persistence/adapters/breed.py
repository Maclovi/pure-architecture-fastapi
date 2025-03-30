from typing import Final

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from cats.application.common.persistence.breed import BreedGateway
from cats.application.common.persistence.filters import Pagination
from cats.entities.breed.models import Breed, BreedID
from cats.entities.breed.value_objects import BreedName
from cats.infrastructure.persistence.models.breed import breeds_table


class BreedMapperAlchemy(BreedGateway):
    """SQLAlchemy implementation of the BreedGateway interface.

    Provides asynchronous database access for
    forBreed entities using SQLAlchemy Core.

    Args:
        session: Async database session for executing queries.

    Note:
        - Implements all required BreedGateway operations
        - Uses raw SQLAlchemy Core for maximum performance
        - Maintains compatibility with domain models
        - Follows repository pattern
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initializes the mapper with an async database session.

        Args:
            session: Async SQLAlchemy session for database operations.
        """
        self._session: Final = session

    @override
    async def with_id(self, breed_id: BreedID) -> Breed | None:
        """Retrieves a breed by its unique identifier.

        Args:
            breed_id: BreedID to search for.

        Returns:
            Breed | None: The matching Breed entity if found, None otherwise.

        Note:
            - Uses SQLAlchemy Core select operation
            - Returns None if no matching breed exists
            - Maintains type safety with BreedID
        """
        stmt = select(Breed).where(breeds_table.c.breed_id == breed_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    @override
    async def with_name(self, name: BreedName) -> Breed | None:
        """Retrieves a breed by its exact name.

        Args:
            name: BreedName value object containing the name to search for.

        Returns:
            Breed | None: The matching Breed entity if found, None otherwise.

        Note:
            - Performs exact match comparison
            - Case-sensitive search
            - Uses validated BreedName value object
        """
        stmt = select(Breed).where(breeds_table.c.breed_name == name.value)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    @override
    async def all(self, pagination: Pagination) -> list[Breed]:
        """Retrieves all breeds with pagination support.

        Args:
            pagination: Pagination parameters containing:
                - offset: Number of records to skip
                - limit: Maximum number of records to return

        Returns:
            list[Breed]: List of Breed entities matching
                the pagination criteria.

        Note:
            - Applies both offset and limit if specified
            - Returns empty list if no breeds exist
            - Maintains order from database unless sorted
            - Uses efficient scalars() execution
        """
        stmt = select(Breed)
        if pagination.offset:
            stmt = stmt.offset(pagination.offset)
        if pagination.limit:
            stmt = stmt.limit(pagination.limit)
        result = await self._session.scalars(stmt)
        return [*result.all()]
