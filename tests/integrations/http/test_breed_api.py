from httpx import AsyncClient
from starlette import status


async def test_get_breeds(client: AsyncClient) -> None:
    response = await client.get("/breeds/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"total": 0, "breeds": []}
