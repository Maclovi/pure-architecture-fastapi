from httpx import AsyncClient
from starlette import status


async def test_get_cats(client: AsyncClient) -> None:
    response = await client.get("/cats/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 0
    assert data["cats"] == []
