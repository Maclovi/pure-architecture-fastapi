from fastapi import APIRouter

from cats.domain.models import Breed

breeds_router = APIRouter(prefix="/breeds")


@breeds_router.get("/breeds", response_model=list[Breed])
async def get_all_breeds() -> list[Breed]:
    return [
        Breed(name="breed1", results=["cat1", "cat2"]),
        Breed(name="breed2", results=["cat3", "cat4"]),
    ]
