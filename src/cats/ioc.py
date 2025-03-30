from dishka import Provider, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from cats.application.commands.cat.add_cat import NewCatCommandHandler
from cats.application.commands.cat.delete_cat_by_id import (
    DeleteCatCommandHandler,
)
from cats.application.commands.cat.update_cat import (
    UpdateCatDescriptionCommandHandler,
)
from cats.application.common.persistence.breed import BreedGateway
from cats.application.common.persistence.cat import CatGateway, CatReader
from cats.application.common.persistence.transaction import (
    EntitySaver,
    Transaction,
)
from cats.application.queries.breed.get_breeds import GetBreedsQueryHandler
from cats.application.queries.cat.get_cat_by_id import GetCatWithIDQueryHandler
from cats.application.queries.cat.get_cats import GetCatsQueryHandler
from cats.entities.breed.services import BreedService
from cats.entities.cat.services import CatService
from cats.infrastructure.configs import ASGIConfig, PostgresConfig
from cats.infrastructure.persistence.adapters.breed import BreedMapperAlchemy
from cats.infrastructure.persistence.adapters.cat import (
    CatMapperAlchemy,
    CatReaderAlchemy,
)
from cats.infrastructure.persistence.adapters.transaction import (
    EntitySaverAlchemy,
    TransactionAlchemy,
)
from cats.infrastructure.persistence.db_provider import (
    get_engine,
    get_session,
    get_sessionmaker,
)


def configs_provider() -> Provider:
    """Creates a Provider for application configuration dependencies.

    Provides:
        - ASGIConfig (app-scoped)
        - PostgresConfig (app-scoped)

    Returns:
        Provider: Configured provider instance with application-level configs.
    """
    provider = Provider()
    provider.from_context(provides=ASGIConfig, scope=Scope.APP)
    provider.from_context(provides=PostgresConfig, scope=Scope.APP)
    return provider


def db_provider() -> Provider:
    """Creates a Provider for database-related dependencies.

    Provides:
        - get_engine (app-scoped)
        - get_sessionmaker (app-scoped)
        - AsyncSession (request-scoped)

    Returns:
        Provider: Configured provider instance with database connections.
    """
    provider = Provider(scope=Scope.REQUEST)
    provider.provide(get_engine, scope=Scope.APP)
    provider.provide(get_sessionmaker, scope=Scope.APP)
    provider.provide(get_session, provides=AsyncSession)
    return provider


def gateways_provider() -> Provider:
    """Creates a Provider for persistence gateway implementations.

    Provides request-scoped:
        - CatGateway (via CatMapperAlchemy)
        - CatReader (via CatReaderAlchemy)
        - BreedGateway (via BreedMapperAlchemy)
        - Transaction (via TransactionAlchemy)
        - EntitySaver (via EntitySaverAlchemy)

    Returns:
        Provider: Configured provider instance with persistence adapters.
    """
    provider = Provider(scope=Scope.REQUEST)
    provider.provide(CatMapperAlchemy, provides=CatGateway)
    provider.provide(CatReaderAlchemy, provides=CatReader)
    provider.provide(BreedMapperAlchemy, provides=BreedGateway)
    provider.provide(TransactionAlchemy, provides=Transaction)
    provider.provide(EntitySaverAlchemy, provides=EntitySaver)
    return provider


def services_provider() -> Provider:
    """Creates a Provider for domain services.

    Provides request-scoped:
        - CatService
        - BreedService

    Returns:
        Provider: Configured provider instance with domain services.
    """
    provider = Provider(scope=Scope.REQUEST)
    provider.provide_all(CatService, BreedService)
    return provider


def interactors_provider() -> Provider:
    """Creates a Provider for application interactors (CQRS handlers).

    Provides request-scoped handlers for:
        - GetBreedsQuery
        - GetCatsQuery
        - GetCatWithIDQuery
        - NewCatCommand
        - DeleteCatCommand
        - UpdateCatDescriptionCommand

    Returns:
        Provider: Configured provider instance with CQRS handlers.
    """
    provider = Provider(scope=Scope.REQUEST)
    provider.provide_all(
        GetBreedsQueryHandler,
        GetCatsQueryHandler,
        GetCatWithIDQueryHandler,
        NewCatCommandHandler,
        DeleteCatCommandHandler,
        UpdateCatDescriptionCommandHandler,
    )
    return provider


def setup_providers() -> tuple[Provider, ...]:
    """Assembles all dependency providers for the application.

    Combines providers for:
        - Configuration
        - Database
        - Persistence gateways
        - Domain services
        - CQRS interactors

    Returns:
        tuple[Provider, ...]: Tuple of all configured providers.
    """
    return (
        configs_provider(),
        db_provider(),
        gateways_provider(),
        services_provider(),
        interactors_provider(),
    )
