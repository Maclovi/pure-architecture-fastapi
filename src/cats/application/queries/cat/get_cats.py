from dataclasses import dataclass
from typing import final

from cats.application.common.persistence.cat import (
    CatFilters,
    CatReader,
)
from cats.application.common.persistence.filters import Pagination
from cats.application.queries.cat.output_shared import CatsOutput


@dataclass(slots=True, frozen=True)
class GetCatsQuery:
    """Query object for retrieving paginated and filtered cat records.

    Encapsulates all parameters needed to execute a cat listing operation,
    including filters and pagination settings. This immutable object ensures
    consistent parameter passing throughout the application layer.

    Attributes:
        filters: CatFilters object containing breed and color
            filtering criteria.
        pagination: Pagination object with offset, limit
            and sort order parameters.

    Notes:
        - Immutable to prevent parameter modification during processing
        - Uses slots for memory efficiency
        - Serves as input for GetCatsQueryHandler
    """

    filters: CatFilters
    pagination: Pagination


@final
class GetCatsQueryHandler:
    """Handler for executing cat listing queries.

    Implements the CQRS pattern by processing GetCatsQuery objects to retrieve
    filtered and paginated cat records from persistence.

    Args:
        cat_reader: CatReader implementation for data access.

    Methods:
        run: Executes the query and returns formatted results.
    """

    def __init__(self, cat_reader: CatReader) -> None:
        """Initializes the handler with required dependencies.

        Args:
            cat_reader: Data access component for reading cat records.
        """
        self._cat_reader = cat_reader

    async def run(self, data: GetCatsQuery) -> CatsOutput:
        """Executes the cat listing query.

        Args:
            data: GetCatsQuery containing filters and pagination parameters.

        Returns:
            CatsOutput: Paginated result containing cat
                records and total count.

        Note:
            The total count in the output represents all matching records
            before pagination is applied.
        """
        cats = await self._cat_reader.all(data.filters, data.pagination)
        return CatsOutput(len(cats), cats)
