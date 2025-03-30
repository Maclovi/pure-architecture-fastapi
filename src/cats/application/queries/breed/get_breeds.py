from dataclasses import dataclass
from typing import final

from cats.application.common.persistence.breed import BreedGateway
from cats.application.common.persistence.filters import Pagination
from cats.entities.breed.models import Breed


@dataclass(slots=True, frozen=True)
class GetBreedsQuery:
    """Query object for retrieving paginated breed records.

    Encapsulates the pagination parameters needed to fetch
        a list of cat breeds.
    This immutable object ensures consistent parameter
        passing throughout the application layer.

    Attributes:
        pagination: Pagination configuration containing:
            - offset: Number of records to skip
            - limit: Maximum number of records to return
            - order: Sort direction (ASC/DESC)
    """

    pagination: Pagination


@dataclass(slots=True, frozen=True)
class BreedsOutput:
    """Data transfer object for paginated breed list responses.

    Represents a page of breed records along with total count information,
    following REST pagination best practices.

    Attributes:
        total: Total number of breeds available (ignoring pagination).
        breeds: List of Breed entities for the current page.
    """

    total: int
    breeds: list[Breed]


@final
class GetBreedsQueryHandler:
    """Handler for executing breed listing queries.

    Implements the CQRS pattern by processing
        GetBreedsQuery objects to retrieve
    paginated breed records from the persistence layer.

    Args:
        breed_gateway: Data access component for breed operations.
    """

    def __init__(self, breed_gateway: BreedGateway) -> None:
        """Initializes the handler with required dependencies.

        Args:
            breed_gateway: Implementation of BreedGateway interface for
                persistence operations.
        """
        self._breed_gateway = breed_gateway

    async def run(self, data: GetBreedsQuery) -> BreedsOutput:
        """Executes the breed listing query.

        Args:
            data: GetBreedsQuery containing pagination parameters.

        Returns:
            BreedsOutput: Contains:
                - total: Count of all available breeds
                - breeds: Paginated list of Breed entities

        Note:
            The total count represents all breeds in the system,
            while the breeds list contains only the current page.
        """
        breeds = await self._breed_gateway.all(data.pagination)
        return BreedsOutput(len(breeds), breeds)
