from typing import cast

from cats.entities.breed.models import BreedID
from cats.entities.cat.models import Cat, CatID
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription


class CatService:
    """Domain service for cat-related business logic and entity creation.

    Provides operations that don't naturally fit within the Cat entity itself,
    particularly around the creation and validation of cat objects.

    Note:
        - Contains stateless operations
        - Follows domain-driven design principles
        - Works with Cat entities and value objects (CatAge, CatColor, etc.)
        - Handles the creation of properly initialized Cat entities
    """

    @staticmethod
    def create_cat(
        breed_id: BreedID | None,
        age: CatAge,
        color: CatColor,
        description: CatDescription,
    ) -> Cat:
        """Creates a new Cat entity with validated attributes.

        Args:
            breed_id: Optional breed identifier (None for mixed breeds).
            age: Validated cat age value object.
            color: Validated cat color value object.
            description: Validated cat description value object.

        Returns:
            Cat: A new Cat entity with:
                - A temporary None ID (to be assigned during persistence)
                - The provided validated attributes

        Note:
            - Uses cast for temporary None ID to satisfy type checker
            - All parameters must be pre-validated value objects
            - The actual ID should be assigned during persistence
            - Caller is responsible for proper persistence
            - Maintains immutability of value objects

        Example:
            >>> cat = CatService.create_cat(
            ...     breed_id=BreedID(1),
            ...     age=CatAge(3),
            ...     color=CatColor("black"),
            ...     description=CatDescription("Playful"),
            ... )
            >>> # Persist the cat to get a real ID
        """
        return Cat(
            oid=cast("CatID", cast("object", None)),
            breed_id=breed_id,
            age=age,
            color=color,
            description=description,
        )
