from httpx import AsyncClient
from starlette import status


async def test_get_cats(client: AsyncClient) -> None:
    response = await client.get("/cats/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"total": 0, "cats": []}


async def test_get_cats_by_breed(client: AsyncClient) -> None:
    response = await client.get("/cats/?breed=plain")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"total": 0, "cats": []}


async def test_get_cat_by_id_noncat(client: AsyncClient) -> None:
    response = await client.get("/cats/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Cat with id=1 not found"


async def test_scenarios_cat(client: AsyncClient) -> None:
    payload = {
        "age": 1,
        "color": "red",
        "description": "biba blyt",
        "breed_name": "plain",
    }
    response = await client.post("/cats/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.read() == b"1"

    response = await client.get("/cats/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["cat"] == {
        "cat_id": 1,
        "breed": "plain",
        "age": 1,
        "color": "red",
        "description": "biba blyt",
    }

    json = {"cat_id": 1, "description": "nixya ne biba"}
    response = await client.patch("/cats/", json=json)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await client.get("/cats/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["cat"]["description"] == "nixya ne biba"

    response = await client.delete("/cats/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
