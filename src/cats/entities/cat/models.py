from dataclasses import dataclass
from typing import NewType

from cats.entities.breed.models import BreedID
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription
from cats.entities.common.base_entity import BaseEntity

CatID = NewType("CatID", int)
"""Strongly-typed identifier for Cat entities.

This type alias creates a distinct type for cat identifiers while maintaining
runtime compatibility with regular integers. Provides type safety when working
with cat IDs throughout the domain.

Note:
    - Prevents accidental mixing with other integer-based IDs
    - Runtime behavior identical to int
    - Used as the OIDType parameter for BaseEntity[CatID]
    - Enforces type safety across domain boundaries
"""


@dataclass
class Cat(BaseEntity[CatID]):
    """Domain entity representing a cat.

    Models the core attributes and behavior of a cat in the system,
    including breed association and descriptive attributes.

    Attributes:
        oid: Unique cat identifier (inherited from BaseEntity)
        breed_id: Optional reference to the cat's breed (None for mixed breeds)
        age: Validated cat age value object
        color: Validated cat color value object
        description: Validated cat description value object

    Note:
        - Uses @dataclass for automatic boilerplate reduction
        - Identity is strongly typed via CatID
        - Attributes are validated via value objects
        - Breed association is optional (None indicates mixed breed)
        - Mutable only through controlled methods

    Example:
        >>> cat = Cat(
        ...     oid=CatID(1),
        ...     breed_id=BreedID(2),
        ...     age=CatAge(3),
        ...     color=CatColor("black"),
        ...     description=CatDescription("Very playful"),
        ... )
    """

    breed_id: BreedID | None
    age: CatAge
    color: CatColor
    description: CatDescription

    def change_description(self, new: CatDescription) -> None:
        """Updates the cat's description with a new validated value.

        Args:
            new: Valid CatDescription value object
                containing the new description.

        Note:
            - Maintains encapsulation by only allowing description changes
              through this method
            - The new description must be a validated CatDescription
            - Preserves object consistency by only modifying one attribute
        """
        self.description = new
