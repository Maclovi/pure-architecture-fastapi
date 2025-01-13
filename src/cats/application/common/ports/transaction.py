from abc import abstractmethod
from typing import Protocol

from cats.entities.common.base_entity import BaseEntity, OIDType


class Transaction(Protocol):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def flush(self) -> None: ...


class EntitySaver:
    @abstractmethod
    def add_one(self, entity: BaseEntity[OIDType]) -> None: ...

    @abstractmethod
    async def delete(self, entity: BaseEntity[OIDType]) -> None: ...
