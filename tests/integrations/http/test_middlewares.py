from unittest import mock

from httpx import AsyncClient
from starlette import status


@mock.patch("cats.presentation.http.middlewares.tracing.logger.info")
async def test_log_requests_middleware(
    mock_logger: mock.Mock,
    client: AsyncClient,
) -> None:
    response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK
    mock_logger.assert_called()
