from dataclasses import dataclass
from typing import final

from cats.application.common.persistence.cat import CatGateway
from cats.application.common.persistence.transaction import Transaction
from cats.application.common.validators import validate_empty
from cats.entities.cat.models import CatID
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription


@dataclass(slots=True, frozen=True)
class CatUpdate:
    """Command object for updating cat attributes.

    Encapsulates all data required to modify a cat's properties in the system.
    This immutable object ensures consistent parameter passing throughout the
    application layer.

    Attributes:
        cat_id: The unique numeric identifier of the cat to update.
        age: Optional new age value for the cat.
        color: Optional new color description for the cat.
        description: Optional new descriptive text about the cat.

    Notes:
        - Frozen to prevent modification after creation
        - Uses slots for memory efficiency
        - All fields will be validated and converted
            to value objects by the handler.
        - None values indicate the field should not be updated
    """

    cat_id: int
    age: int | None = None
    color: str | None = None
    description: str | None = None


@final
class CatUpdateHandler:
    """Handler for executing cat attribute updates.

    Coordinates the update of cat properties, including validation,
    entity modification, and transaction management.

    Args:
        cat_gateway: Data access component for cat persistence operations.
        transaction: Transaction manager ensuring atomic updates.
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

    async def run(self, data: CatUpdate) -> None:
        """Executes the cat attribute update command.

        Args:
            data: Contains update parameters including:
                - cat_id: Required identifier of cat to update
                - age: Optional new age value (if provided)
                - color: Optional new color description (if provided)
                - description: Optional new text (if provided)

        Raises:
            EntityNotFoundError: If no cat exists with the specified ID.
            ValidationError: If any provided value fails validation.

        Note:
            Performs atomically:
            1. Cat existence verification
            2. Value validation for all provided fields
            3. Entity updates for all valid fields
            4. Transaction commit
        """
        cat = await self._cat_gateway.with_id(CatID(data.cat_id))
        cat = validate_empty(cat, data.cat_id)

        if data.age:
            cat.change_age(CatAge(data.age))
        if data.color:
            cat.change_color(CatColor(data.color))
        if data.description:
            cat.change_description(CatDescription(data.description))

        await self._transaction.commit()
