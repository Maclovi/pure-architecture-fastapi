from dataclasses import dataclass
from typing import final

from cats.application.common.persistence.breed import BreedGateway
from cats.application.common.persistence.transaction import (
    EntitySaver,
    Transaction,
)
from cats.entities.breed.models import Breed, BreedID
from cats.entities.breed.value_objects import BreedName
from cats.entities.cat.models import Cat, CatID
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription


@dataclass(frozen=True, slots=True)
class NewCatCommand:
    """Command object for creating a new cat record.

    Encapsulates all data required to initialize a new cat entity.
    This immutable object ensures consistent parameter passing throughout
    the application layer.

    Attributes:
        age: The cat's age in years (positive integer).
        color: The primary color description of the cat's coat.
        description: Text describing the cat's characteristics.
        breed_name: Optional breed specification. None indicates
            a mixed-breed or unknown breed.

    Notes:
        - Frozen to enforce immutability after creation
        - Uses slots for memory optimization
        - All values undergo validation when converted to value objects
    """

    age: int
    color: str
    description: str
    breed_name: str | None


@final
class NewCatCommandHandler:
    """Handler for creating new cat records with breed resolution.

    Orchestrates the complete cat creation workflow including:
    - Breed lookup/creation when specified
    - Cat entity instantiation
    - Transactional persistence
    - ID generation

    Args:
        transaction: Coordinates atomic database operations.
        entity_saver: Handles entity persistence.
        breed_gateway: Provides breed data access.
    """

    def __init__(
        self,
        transaction: Transaction,
        entity_saver: EntitySaver,
        breed_gateway: BreedGateway,
    ) -> None:
        """Initializes handler with persistence dependencies.

        Args:
            transaction: Manages transaction boundaries.
            entity_saver: Handles entity storage operations.
            breed_gateway: Provides breed data access.
        """
        self._transaction = transaction
        self._entity_saver = entity_saver
        self._breed_gateway = breed_gateway

    async def run(self, data: NewCatCommand) -> CatID:
        """Creates and persists a new cat record.

        Args:
            data: Contains validated cat attributes for creation.

        Returns:
            The persistent identifier of the newly created cat.

        Note:
            Atomic operation sequence:
            1. Breed resolution (if specified)
            2. Cat entity instantiation
            3. Database persistence
            4. ID return
        """
        if data.breed_name:
            breed_id = await self._get_breed_id(BreedName(data.breed_name))
        else:
            breed_id = None
        new_cat = Cat.create_cat(
            breed_id,
            CatAge(data.age),
            CatColor(data.color),
            CatDescription(data.description),
        )
        self._entity_saver.add_one(new_cat)
        await self._transaction.commit()
        return new_cat.oid

    async def _get_breed_id(self, breed_name: BreedName) -> BreedID:
        """Resolves breed reference, creating new breed if necessary.

        Args:
            breed_name: Validated breed name specification.

        Returns:
            Persistent identifier for existing or new breed.

        Note:
            Auto-creates new breed records for unrecognized names,
            persisting them before reference.
        """
        breed = await self._breed_gateway.with_name(breed_name)
        if breed is None:
            breed = Breed.create_breed(breed_name)
            self._entity_saver.add_one(breed)
            await self._transaction.flush()
        return breed.oid
