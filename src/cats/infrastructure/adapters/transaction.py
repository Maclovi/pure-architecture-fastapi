from typing import Final

from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from cats.application.common.ports.transaction import EntitySaver, Transaction
from cats.entities.common.base_entity import BaseEntity, OIDType


class TransactionAlchemy(Transaction):
    def __init__(self, session: AsyncSession) -> None:
        self._session: Final[AsyncSession] = session

    @override
    async def commit(self) -> None:
        await self._session.commit()

    @override
    async def flush(self) -> None:
        await self._session.flush()


class EntitySaverAlchemy(EntitySaver):
    def __init__(self, session: AsyncSession) -> None:
        self._session: Final[AsyncSession] = session

    @override
    def add_one(self, entity: BaseEntity[OIDType]) -> None:
        self._session.add(entity)

    @override
    async def delete(self, entity: BaseEntity[OIDType]) -> None:
        await self._session.delete(entity)
