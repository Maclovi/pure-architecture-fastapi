from dataclasses import dataclass
from typing import final

from cats.application.common.persistence.cat import CatReader
from cats.application.common.persistence.view_models import CatView
from cats.application.common.validators import validate_empty
from cats.entities.cat.models import CatID


@dataclass(slots=True, frozen=True)
class GetCatWithIDQuery:
    """Query object for retrieving a single cat by its identifier.

    Encapsulates the parameters needed to fetch a specific cat record.
    This immutable object ensures consistent parameter passing throughout
    the application layer.

    Attributes:
        id: The unique numeric identifier of the cat to retrieve.
    """

    id: int


@dataclass(slots=True, frozen=True)
class CatOutput:
    """Data transfer object for single cat API responses.

    Wraps a CatView instance to provide consistent output formatting
    for single-cat retrieval operations.

    Attributes:
        cat: The complete view model of the retrieved cat.
    """

    cat: CatView


@final
class GetCatWithIDQueryHandler:
    """Handler for executing single-cat retrieval queries.

    Implements the CQRS pattern by processing GetCatWithIDQuery objects
    to fetch individual cat records from persistence.

    Args:
        cat_reader: CatReader implementation for data access.
    """

    def __init__(self, cat_reader: CatReader) -> None:
        """Initializes the handler with required dependencies.

        Args:
            cat_reader: Data access component for reading cat records.
        """
        self._cat_reader = cat_reader

    async def run(self, data: GetCatWithIDQuery) -> CatOutput:
        """Executes the single-cat retrieval query.

        Args:
            data: GetCatWithIDQuery containing the cat identifier.

        Returns:
            CatOutput: Wrapped cat view model.

        Raises:
            EntityNotFoundError: If no cat exists with the specified ID.
            ValidationError: If the ID format is invalid.

        Note:
            Performs validation to ensure the cat exists before returning.
        """
        cat = await self._cat_reader.with_id(CatID(data.id))
        cat = validate_empty(cat, data.id)
        return CatOutput(cat)
