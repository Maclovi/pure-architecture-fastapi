from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from cats.infrastructure.configs import PostgresConfig


async def get_engine(config: PostgresConfig) -> AsyncIterator[AsyncEngine]:
    """Creates and manages the lifecycle of an async SQLAlchemy engine.

    Args:
        config: PostgreSQL configuration containing:
            - uri: Database connection string
            - debug: Flag to enable SQL echo output

    Yields:
        AsyncEngine: Configured SQLAlchemy async engine instance

    Note:
        - Uses connection pooling (size=15, overflow=15)
        - Sets 5-second connection timeout
        - Enables connection health checks (pool_pre_ping)
        - Automatically disposes the engine when done

    Example:
        async for engine in get_engine(config):
            # Use engine...
    """
    engine = create_async_engine(
        config.uri,
        echo=config.debug,
        pool_size=15,
        max_overflow=15,
        connect_args={"connect_timeout": 5},
        pool_pre_ping=True,
    )
    yield engine
    await engine.dispose()


async def get_sessionmaker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    """Creates an async session factory bound to an engine.

    Args:
        engine: AsyncEngine instance to bind to the session factory

    Returns:
        async_sessionmaker: Configured session factory with:
            - autoflush disabled
            - expire_on_commit disabled

    Note:
        - The returned factory should be reused throughout the application
        - Disabling autoflush and expire_on_commit improves performance
        - Sessions should be short-lived (created per request)
    """
    return async_sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )


async def get_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    """Provides an async database session context manager.

    Args:
        session_factory: Session factory to create new sessions from

    Yields:
        AsyncSession: A new async database session

    Note:
        - Automatically handles session cleanup
        - Sessions should be used within a single logical operation
        - Transactions should be explicitly committed or rolled back

    Example:
        async for session in get_session(session_factory):
            await session.execute(...)
    """
    async with session_factory() as session:
        yield session
