from fastapi import FastAPI

from cats.api import breeds, cats


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(cats.cats_router)
    app.include_router(breeds.breeds_router)
    return app
