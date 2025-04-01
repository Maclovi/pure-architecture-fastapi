from dataclasses import dataclass
from typing import NewType, cast

from typing_extensions import Self

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

    def change_age(self, new_age: CatAge) -> None:
        """Updates the cat's age with a new validated age value.

        Args:
            new_age: Valid CatAge value object containing the new age value.
        """
        self.age = new_age

    def change_color(self, new_color: CatColor) -> None:
        """Updates the cat's color with a new validated color value.

        Args:
            new_color: Valid CatColor value object containing
                the new color value.
        """
        self.color = new_color

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

    @classmethod
    def create_cat(
        cls,
        breed_id: BreedID | None,
        age: CatAge,
        color: CatColor,
        description: CatDescription,
    ) -> Self:
        """Factory method for creating new Cat
            instances with validated attributes.

        Constructs a new Cat entity with temporary None ID, which should be
        replaced with a proper ID during persistence.

        Args:
            breed_id: Optional breed reference (None for mixed/unknown breeds)
            age: Validated age value object
            color: Validated color value object
            description: Validated description value object

        Returns:
            A new Cat instance with all provided attributes
                and temporary None ID.

        Note:
            - All parameters must be pre-validated value objects
            - The actual ID will be assigned during persistence
            - Uses type casting for the temporary None ID
                to satisfy type checking.
            - Caller is responsible for proper persistence handling

        Example:
            >>> new_cat = Cat.create_cat(
            ...     breed_id=BreedID(1),
            ...     age=CatAge(2),
            ...     color=CatColor("tabby"),
            ...     description=CatDescription("Very vocal"),
            ... )
            >>> repository.save(new_cat)  # Persistence assigns real ID
        """
        return cls(
            oid=cast("CatID", cast("object", None)),
            breed_id=breed_id,
            age=age,
            color=color,
            description=description,
        )
