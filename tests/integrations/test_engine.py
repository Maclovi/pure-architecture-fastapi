from unittest import mock

from cats.infrastructure.persistence.db_provider import get_engine


@mock.patch("cats.infrastructure.persistence.db_provider.create_async_engine")
async def test_engine(mock_create_async_engine: mock.Mock) -> None:
    mock_create_async_engine.return_value.dispose = mock.AsyncMock()

    mock_config = mock.Mock()
    e = get_engine(mock_config)
    async for _ in e:
        pass

    mock_create_async_engine.return_value.dispose.assert_called_once()
