from dataclasses import dataclass
from typing import Generic, TypeVar

OIDType = TypeVar("OIDType")


@dataclass
class BaseEntity(Generic[OIDType]):
    """Abstract base class for all domain entities.

    Provides the fundamental structure for domain entities with generic
    identifier support. All concrete domain entities should inherit from
    this class.

    Attributes:
        oid: The unique identifier of the entity. Type is parameterized
            to support different identifier types (int, UUID, etc.) for
            different entities.

    Type Variables:
        OIDType: The type parameter for the entity's identifier.

    Note:
        - Uses @dataclass for automatic boilerplate reduction
        - Designed to be inherited by concrete entity classes
        - Supports any identifier type through generics
        - Forms the foundation of the domain model hierarchy

    Example:
        class CatEntity(BaseEntity[CatID]):
            name: str
            breed: BreedID
            ...
    """

    oid: OIDType
