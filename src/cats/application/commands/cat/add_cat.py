from dataclasses import dataclass
from typing import final

from cats.application.common.persistence.breed import BreedGateway
from cats.application.common.persistence.transaction import (
    EntitySaver,
    Transaction,
)
from cats.entities.breed.models import BreedID
from cats.entities.breed.services import BreedService
from cats.entities.breed.value_objects import BreedName
from cats.entities.cat.models import CatID
from cats.entities.cat.services import CatService
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription


@dataclass(frozen=True, slots=True)
class NewCatCommand:
    """Command object for creating a new cat record.

    Encapsulates all data required to create a new cat in the system.
    This immutable object ensures consistent parameter passing throughout
    the application layer.

    Attributes:
        age: The cat's age in years.
        color: The primary color of the cat's coat.
        description: Descriptive text about the cat's
            appearance or personality.
        breed_name: Optional name of the cat's breed.
            None indicates a mixed-breed cat.

    Notes:
        - Frozen to prevent modification after creation
        - Uses slots for memory efficiency
        - Values will be validated and converted
            to value objects by the handler
    """

    age: int
    color: str
    description: str
    breed_name: str | None


@final
class NewCatCommandHandler:
    """Handler for executing new cat creation commands.

    Coordinates the creation of new cat records, including:
    - Breed resolution (creating new breeds if necessary)
    - Cat entity creation
    - Transaction management
    - Persistence operations

    Args:
        transaction: Transaction manager for atomic operations.
        entity_saver: Persistence interface for saving entities.
        breed_gateway: Data access component for breed operations.
        cat_service: Domain service for cat-related business logic.
        breed_service: Domain service for breed-related business logic.
    """

    def __init__(
        self,
        transaction: Transaction,
        entity_saver: EntitySaver,
        breed_gateway: BreedGateway,
        cat_service: CatService,
        breed_service: BreedService,
    ) -> None:
        """Initializes the handler with required dependencies.

        Args:
            transaction: Handles database transaction boundaries.
            entity_saver: Manages persistence of new entities.
            breed_gateway: Provides access to breed data.
            cat_service: Contains cat creation business rules.
            breed_service: Contains breed creation business rules.
        """
        self._transaction = transaction
        self._entity_saver = entity_saver
        self._breed_gateway = breed_gateway
        self._cat_service = cat_service
        self._breed_service = breed_service

    async def run(self, data: NewCatCommand) -> CatID:
        """Executes the new cat creation command.

        Args:
            data: NewCatCommand containing all required cat attributes.

        Returns:
            CatID: The unique identifier of the newly created cat.

        Note:
            Performs the following operations atomically:
            1. Resolves or creates the breed (if specified)
            2. Creates a new cat entity
            3. Persists all changes
            4. Returns the new cat's ID
        """
        if data.breed_name:
            breed_id = await self._get_breed_id(BreedName(data.breed_name))
        else:
            breed_id = None
        new_cat = self._cat_service.create_cat(
            breed_id,
            CatAge(data.age),
            CatColor(data.color),
            CatDescription(data.description),
        )
        self._entity_saver.add_one(new_cat)
        await self._transaction.commit()
        return new_cat.oid

    async def _get_breed_id(self, breed_name: BreedName) -> BreedID:
        """Resolves a breed ID by name, creating the breed if necessary.

        Args:
            breed_name: Name of the breed to resolve.

        Returns:
            BreedID: The existing or newly created breed's identifier.

        Note:
            If the breed doesn't exist, creates and persists a new breed
            before returning its ID.
        """
        breed = await self._breed_gateway.with_name(breed_name)
        if breed is None:
            breed = self._breed_service.create_breed(breed_name)
            self._entity_saver.add_one(breed)
            await self._transaction.flush()
        return breed.oid
