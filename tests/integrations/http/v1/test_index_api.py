from httpx import AsyncClient
from starlette import status


async def test_get_index(client: AsyncClient) -> None:
    response = await client.get("/v1/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello there! Welcome to cats API"}
