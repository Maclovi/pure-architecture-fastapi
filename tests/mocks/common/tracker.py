from collections.abc import Iterable
from contextlib import suppress
from typing import Any

from cats.entities.common.base_entity import BaseEntity, OIDType
from cats.entities.common.tracker import Tracker


class FakeTracker(Tracker):
    def __init__(self) -> None:
        self.entities: list[Any] = []

    def add_one(self, entity: BaseEntity[OIDType]) -> None:
        self.entities.append(entity)

    def add_many(self, entities: Iterable[BaseEntity[OIDType]]) -> None:
        self.entities.extend(entities)

    async def delete(self, entity: BaseEntity[OIDType]) -> None:
        with suppress(ValueError):
            self.entities.remove(entity)
