from dataclasses import dataclass
from typing import final

from cats.application.common.persistence.cat import CatGateway
from cats.application.common.persistence.transaction import Transaction
from cats.application.common.validators import validate_empty
from cats.entities.cat.models import CatID
from cats.entities.cat.value_objects import CatDescription


@dataclass(slots=True, frozen=True)
class UpdateCatDescriptionCommand:
    """Command object for updating a cat's description.

    Encapsulates all data required to modify a cat's description in the system.
    This immutable object ensures consistent parameter passing throughout the
    application layer.

    Attributes:
        cat_id: The unique numeric identifier of the cat to update.
        description: New descriptive text about
            the cat's appearance or personality.

    Notes:
        - Frozen to prevent modification after creation
        - Uses slots for memory efficiency
        - The ID will be validated and converted to a CatID value object
        - The description will be validated and converted to a CatDescription
          value object by the handler
    """

    cat_id: int
    description: str


@final
class UpdateCatDescriptionCommandHandler:
    """Handler for executing cat description update commands.

    Coordinates the update of cat descriptions, including:
    - Validation of cat existence
    - Description validation
    - Entity modification
    - Transaction management

    Args:
        cat_gateway: Data access component for cat operations.
        transaction: Transaction manager for atomic operations.
    """

    def __init__(
        self,
        cat_gateway: CatGateway,
        transaction: Transaction,
    ) -> None:
        """Initializes the handler with required dependencies.

        Args:
            cat_gateway: Provides access
                to cat data and persistence operations.
            transaction: Handles database transaction boundaries.
        """
        self._cat_gateway = cat_gateway
        self._transaction = transaction

    async def run(self, data: UpdateCatDescriptionCommand) -> None:
        """Executes the cat description update command.

        Args:
            data: UpdateCatDescriptionCommand containing:
                - cat_id: Identifier of cat to update
                - description: New description text

        Raises:
            EntityNotFoundError: If no cat exists with the specified ID.
            ValidationError: If either the ID or description format is invalid.

        Note:
            Performs the following operations atomically:
            1. Validates the cat exists
            2. Validates the new description
            3. Updates the cat's description
            4. Commits the transaction
        """
        description = CatDescription(data.description)
        cat = await self._cat_gateway.with_id(CatID(data.cat_id))
        cat = validate_empty(cat, data.cat_id)
        cat.change_description(description)
        await self._transaction.commit()
