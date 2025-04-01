from dataclasses import dataclass
from typing import NewType, cast

from typing_extensions import Self

from cats.entities.breed.value_objects import BreedName
from cats.entities.common.base_entity import BaseEntity

BreedID = NewType("BreedID", int)
"""Strongly-typed identifier for Breed entities.

This type alias creates a distinct type for breed identifiers while maintaining
runtime compatibility with regular integers. Provides type safety when working
with breed IDs throughout the domain.

Note:
    - Prevents accidental mixing with other integer-based IDs
    - Runtime behavior identical to int
    - Used as the OIDType parameter for BaseEntity[BreedID]
"""


@dataclass
class Breed(BaseEntity[BreedID]):
    """Domain entity representing a cat breed.

    Models the core attributes and identity of a cat breed in the system.
    Inherits from BaseEntity to get common identity behavior.

    Attributes:
        oid: Unique breed identifier (inherited from BaseEntity)
        name: The breed's name, wrapped in BreedName value
            object for validation.

    Note:
        - Uses @dataclass for automatic boilerplate reduction
        - Identity is strongly typed via BreedID
        - Name is validated via BreedName value object
        - Represents an aggregate root in DDD terms

    Example:
        >>> siamese = Breed(oid=BreedID(1), name=BreedName("Siamese"))
    """

    name: BreedName

    @classmethod
    def create_breed(cls, breed_name: BreedName) -> Self:
        """Creates a new Breed entity with the given name.

        Args:
            breed_name: Validated breed name value object.

        Returns:
            Breed: A new Breed entity with:
                - A temporary None ID (to be assigned during persistence)
                - The provided breed name

        Note:
            - Uses cast for temporary None ID to satisfy type checker
            - The actual ID should be assigned during persistence
            - The breed_name is assumed to be already validated
            - Caller is responsible for proper persistence

        Example:
            >>> breed = Breed.create_breed(BreedName("Siamese"))
            >>> # Persist the breed to get a real ID
        """
        return cls(
            oid=cast("BreedID", cast("object", None)),
            name=breed_name,
        )
