from httpx import AsyncClient
from starlette import status


async def test_get_cats(client: AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello there! Welcome to cats API"}
