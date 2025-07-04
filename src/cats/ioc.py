from dishka import Provider, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from cats.application.commands.cat.add_cat import NewCatCommandHandler
from cats.application.commands.cat.cat_update import (
    CatUpdateHandler,
)
from cats.application.commands.cat.delete_cat_by_id import (
    DeleteCatCommandHandler,
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
    provider = Provider()
    provider.from_context(provides=ASGIConfig, scope=Scope.APP)
    provider.from_context(provides=PostgresConfig, scope=Scope.APP)
    return provider


def db_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide(get_engine, scope=Scope.APP)
    provider.provide(get_sessionmaker, scope=Scope.APP)
    provider.provide(get_session, provides=AsyncSession)
    return provider


def gateways_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide(CatMapperAlchemy, provides=CatGateway)
    provider.provide(CatReaderAlchemy, provides=CatReader)
    provider.provide(BreedMapperAlchemy, provides=BreedGateway)
    provider.provide(TransactionAlchemy, provides=Transaction)
    provider.provide(EntitySaverAlchemy, provides=EntitySaver)
    return provider


def interactors_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide_all(
        GetBreedsQueryHandler,
        GetCatsQueryHandler,
        GetCatWithIDQueryHandler,
        NewCatCommandHandler,
        DeleteCatCommandHandler,
        CatUpdateHandler,
    )
    return provider


def setup_providers() -> tuple[Provider, ...]:
    return (
        configs_provider(),
        db_provider(),
        gateways_provider(),
        interactors_provider(),
    )
