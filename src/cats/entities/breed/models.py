from dataclasses import dataclass
from typing import NewType

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
