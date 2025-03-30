from dataclasses import dataclass
from typing import final

from cats.application.common.persistence.cat import CatGateway
from cats.application.common.persistence.transaction import (
    EntitySaver,
    Transaction,
)
from cats.application.common.validators import validate_empty
from cats.entities.cat.models import CatID


@dataclass(slots=True, frozen=True)
class DeleteCatCommand:
    """Command object for deleting a cat record.

    Encapsulates the identifier needed
        to delete a specific cat from the system.
    This immutable object ensures consistent parameter passing throughout the
    application layer.

    Attributes:
        cat_id: The unique numeric identifier of the cat to delete.

    Notes:
        - Frozen to prevent modification after creation
        - Uses slots for memory efficiency
        - The ID will be validated and converted to a CatID value object
          by the handler
    """

    cat_id: int


@final
class DeleteCatCommandHandler:
    """Handler for executing cat deletion commands.

    Coordinates the deletion of cat records, including:
    - Validation of cat existence
    - Deletion operation
    - Transaction management

    Args:
        transaction: Transaction manager for atomic operations.
        entity_saver: Persistence interface for delete operations.
        cat_gateway: Data access component for cat operations.
    """

    def __init__(
        self,
        transaction: Transaction,
        entity_saver: EntitySaver,
        cat_gateway: CatGateway,
    ) -> None:
        """Initializes the handler with required dependencies.

        Args:
            transaction: Handles database transaction boundaries.
            entity_saver: Manages persistence operations for deletions.
            cat_gateway: Provides access to cat data.
        """
        self._transaction = transaction
        self._entity_saver = entity_saver
        self._cat_gateway = cat_gateway

    async def run(self, data: DeleteCatCommand) -> None:
        """Executes the cat deletion command.

        Args:
            data: DeleteCatCommand containing the cat identifier.

        Raises:
            EntityNotFoundError: If no cat exists with the specified ID.
            ValidationError: If the ID format is invalid.

        Note:
            Performs the following operations atomically:
            1. Validates the cat exists
            2. Marks the cat for deletion
            3. Commits the transaction
        """
        cat = await self._cat_gateway.with_id(CatID(data.cat_id))
        cat = validate_empty(cat, data.cat_id)

        await self._entity_saver.delete(cat)
        await self._transaction.commit()
