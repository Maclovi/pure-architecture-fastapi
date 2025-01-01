from abc import abstractmethod
from typing import Protocol

from cats.entities.common.base_entity import BaseEntity, OIDType


class Tracker(Protocol):
    @abstractmethod
    def add_one(self, entity: BaseEntity[OIDType]) -> None: ...

    @abstractmethod
    async def delete(self, entity: BaseEntity[OIDType]) -> None: ...
