from pydantic import BaseModel

from cats.application.common.ports.filters import SortOrder


class ExceptionSchema(BaseModel):
    detail: str


class BreedSchema(BaseModel):
    breed: str


class PaginationSchema(BaseModel):
    offset: int | None = None
    limit: int | None = None
    order: SortOrder = SortOrder.ASC


class CatFiltersSchema(BaseModel):
    breed: str | None = None
    color: str | None = None


class CatsAllSchema(PaginationSchema, CatFiltersSchema):
    pass


class CatsWithBreedSchema(BreedSchema, PaginationSchema):
    pass
