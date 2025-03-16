import os
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine

from cats.infrastructure.persistence.models.base import metadata
from cats.web import create_app

if TYPE_CHECKING:
    from dishka import AsyncContainer


def _load_env() -> None:
    os.environ["POSTGRES_USER"] = "postgres"
    os.environ["POSTGRES_PASSWORD"] = "postgres"  # noqa: S105
    os.environ["POSTGRES_HOST"] = "localhost"
    os.environ["POSTGRES_PORT"] = "5432"
    os.environ["POSTGRES_DB"] = "test"
    os.environ["POSTGRES_DEBUG"] = "true"
    os.environ["UVICORN_HOST"] = "127.0.0.1"
    os.environ["UVICORN_PORT"] = "8888"


@pytest.fixture(scope="session")
async def app() -> AsyncIterator[FastAPI]:
    _load_env()
    app = create_app()
    container: AsyncContainer = app.state.dishka_container

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
