import os
from collections.abc import AsyncIterator

import pytest
from dishka import AsyncContainer, Provider, Scope, make_async_container
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from cats.infrastructure.bootstrap.ioc import setup_providers
from cats.infrastructure.persistence.models.base import metadata
from cats.web import create_app


def _load_env() -> None:
    os.environ["POSTGRES_USER"] = ""
    os.environ["POSTGRES_PASSWORD"] = ""
    os.environ["POSTGRES_HOST"] = ""
    os.environ["POSTGRES_PORT"] = ""
    os.environ["POSTGRES_DB"] = ""
    os.environ["POSTGRES_DEBUG"] = ""
    os.environ["UVICORN_HOST"] = "127.0.0.1"
    os.environ["UVICORN_PORT"] = "8000"


def _get_engine() -> AsyncEngine:
    return create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)


@pytest.fixture(scope="session")
def container() -> AsyncContainer:
    overriden_provider = Provider()
    overriden_provider.provide(_get_engine, scope=Scope.APP)
    return make_async_container(*setup_providers(), overriden_provider)


@pytest.fixture(scope="session")
async def app(container: AsyncContainer) -> AsyncIterator[FastAPI]:
    _load_env()
    app = create_app()
    app.state.dishka_container = container

    engine = await container.get(AsyncEngine)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield app
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope="session")
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    t = ASGITransport(app)
    async with AsyncClient(transport=t, base_url="http://test") as ac:
        yield ac