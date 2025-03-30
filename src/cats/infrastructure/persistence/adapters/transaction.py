from typing import Final

from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from cats.application.common.persistence.transaction import (
    EntitySaver,
    Transaction,
)
from cats.entities.common.base_entity import BaseEntity, OIDType


class TransactionAlchemy(Transaction):
    """SQLAlchemy implementation of the Transaction interface.

    Provides asynchronous transaction management using SQLAlchemy's session,
    handling commit and flush operations for atomic changes.

    Args:
        session: Async SQLAlchemy session to manage transactions for.

    Note:
        - Implements unit of work pattern
        - Wraps SQLAlchemy's async transaction methods
        - Should be used as a context manager in most cases
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initializes the transaction manager with a database session.

        Args:
            session: Async SQLAlchemy session for transaction operations.
        """
        self._session: Final[AsyncSession] = session

    @override
    async def commit(self) -> None:
        """Commits all pending changes to the database.

        Note:
            - Makes all staged changes permanent
            - Ends the current transaction
            - Raises if any conflicts or violations occur
            - Starts a new transaction automatically
        """
        await self._session.commit()

    @override
    async def flush(self) -> None:
        """Flushes pending changes without committing.

        Note:
            - Writes changes to database but doesn't commit
            - Useful for getting generated IDs before commit
            - Maintains transaction isolation
        """
        await self._session.flush()


class EntitySaverAlchemy(EntitySaver):
    """SQLAlchemy implementation of the EntitySaver interface.

    Provides asynchronous entity persistence
        operations using SQLAlchemy's session,
    handling both additions and deletions of domain entities.

    Args:
        session: Async SQLAlchemy session for persistence operations.

    Note:
        - Implements repository pattern for entity persistence
        - Works with any BaseEntity subclass
        - Changes are transactional (require commit to persist)
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initializes the saver with a database session.

        Args:
            session: Async SQLAlchemy session for entity operations.
        """
        self._session: Final[AsyncSession] = session

    @override
    def add_one(self, entity: BaseEntity[OIDType]) -> None:
        """Stages a new entity for persistence.

        Args:
            entity: Domain entity to persist. Must inherit from BaseEntity.

        Note:
            - Entity is added to session but not written to DB immediately
            - Requires subsequent commit to make permanent
            - Works with any entity type via BaseEntity[OIDType]
        """
        self._session.add(entity)

    @override
    async def delete(self, entity: BaseEntity[OIDType]) -> None:
        """Marks an entity for deletion.

        Args:
            entity: Domain entity to remove. Must inherit from BaseEntity.

        Note:
            - Deletion is staged but not executed immediately
            - Requires subsequent commit to make permanent
            - Works with any entity type via BaseEntity[OIDType]
        """
        await self._session.delete(entity)
