from fastapi import APIRouter, status

from cats.domain.models import Breed, Cat

cats_router = APIRouter(prefix="/cats")


@cats_router.get("/all", response_model=list[Cat])
async def get_all() -> list[Cat]:
    return [
        Cat(color="red", age=5, description="cat1", breed=None),
        Cat(
            color="blue", age=10, description="cat2", breed=Breed(title="muy")
        ),
    ]


@cats_router.get("/breed/{breed}", response_model=list[Cat])
async def get_by_breed(breed: str) -> list[Cat]:
    return [
        Cat(color="red", age=5, description="cat1", breed=None),
        Cat(
            color="blue", age=10, description="cat2", breed=Breed(title="muy")
        ),
    ]


@cats_router.get("/id/{id}", response_model=Cat)
async def get_by_id(id: int) -> Cat:
    return Cat(color="red", age=5, description="cat1", breed=None)


@cats_router.post(
    "/add", response_model=Cat, status_code=status.HTTP_201_CREATED
)
async def add(cat: Cat) -> Cat:
    return cat


@cats_router.put("/update", response_model=Cat)
async def update(cat: Cat) -> Cat:
    return cat


@cats_router.delete(
    "/delete/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def delete_by_id(id: int) -> None:
    pass
