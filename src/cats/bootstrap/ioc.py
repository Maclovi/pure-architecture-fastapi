from dishka import Provider, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from cats.application.commands.cat.add_cat import NewCatCommandHandler
from cats.application.commands.cat.delete_cat_by_id import (
    DeleteCatCommandHandler,
)
from cats.application.commands.cat.update_cat import (
    UpdateCatDescriptionCommandHandler,
)
from cats.application.common.ports.breed import BreedGateway
from cats.application.common.ports.cat import CatGateway, CatReader
from cats.application.common.ports.transaction import EntitySaver, Transaction
from cats.application.queries.breed.get_breeds import GetBreedsQueryHandler
from cats.application.queries.cat.get_cat_by_id import GetCatWithIDQueryHandler
from cats.application.queries.cat.get_cats import GetCatsQueryHandler
from cats.application.queries.cat.get_cats_by_breed import (
    GetCatsWithBreedQueryHandler,
)
from cats.entities.breed.services import BreedService
from cats.entities.cat.services import CatService
from cats.infrastructure.adapters.breed import BreedMapperAlchemy
from cats.infrastructure.adapters.cat import CatMapperAlchemy, CatReaderAlchemy
from cats.infrastructure.adapters.transaction import (
    EntitySaverAlchemy,
    TransactionAlchemy,
)
from cats.infrastructure.configs import APIConfig, PostgresConfig
from cats.infrastructure.persistence.db_provider import (
    get_engine,
    get_session,
    get_sessionmaker,
)


def configs_provider() -> Provider:
    provider = Provider()
    _ = provider.from_context(provides=APIConfig, scope=Scope.APP)
    _ = provider.from_context(provides=PostgresConfig, scope=Scope.APP)
    return provider


def db_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    _ = provider.provide(get_engine, scope=Scope.APP)
    _ = provider.provide(get_sessionmaker, scope=Scope.APP)
    _ = provider.provide(get_session, provides=AsyncSession)
    return provider


def gateways_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    _ = provider.provide(CatMapperAlchemy, provides=CatGateway)
    _ = provider.provide(CatReaderAlchemy, provides=CatReader)
    _ = provider.provide(BreedMapperAlchemy, provides=BreedGateway)
    _ = provider.provide(TransactionAlchemy, provides=Transaction)
    _ = provider.provide(EntitySaverAlchemy, provides=EntitySaver)
    return provider


def services_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    _ = provider.provide_all(CatService, BreedService)
    return provider


def interactors_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    _ = provider.provide_all(
        GetBreedsQueryHandler,
        GetCatsQueryHandler,
        GetCatWithIDQueryHandler,
        GetCatsWithBreedQueryHandler,
        NewCatCommandHandler,
        DeleteCatCommandHandler,
        UpdateCatDescriptionCommandHandler,
    )
    return provider


def setup_providers() -> tuple[Provider, ...]:
    return (
        configs_provider(),
        db_provider(),
        gateways_provider(),
        services_provider(),
        interactors_provider(),
    )
