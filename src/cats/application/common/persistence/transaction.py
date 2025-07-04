from typing import Protocol

from cats.entities.common.base_entity import BaseEntity, OIDType


class Transaction(Protocol):
    async def commit(self) -> None: ...

    async def flush(self) -> None: ...


class EntitySaver(Protocol):
    def add_one(self, entity: BaseEntity[OIDType]) -> None: ...

    async def delete(self, entity: BaseEntity[OIDType]) -> None: ...
