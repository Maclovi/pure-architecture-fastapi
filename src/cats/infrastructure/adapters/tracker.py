from typing import Final

from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from cats.entities.common.base_entity import BaseEntity, OIDType
from cats.entities.common.tracker import Tracker


class TrackerAlchemy(Tracker):
    def __init__(self, session: AsyncSession) -> None:
        self._session: Final = session

    @override
    def add_one(self, entity: BaseEntity[OIDType]) -> None:
        self._session.add(entity)

    @override
    async def delete(self, entity: BaseEntity[OIDType]) -> None:
        await self._session.delete(entity)
