from dataclasses import dataclass
from typing import Generic, TypeVar

OIDType = TypeVar("OIDType")


@dataclass
class BaseEntity(Generic[OIDType]):
    oid: OIDType
