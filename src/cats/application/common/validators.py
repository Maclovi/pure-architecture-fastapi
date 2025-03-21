from typing import TypeVar

from cats.application.common.errors.cat import CatNotFoundError
from cats.application.common.ports.view_models import CatView
from cats.entities.cat.models import Cat

CatT = TypeVar("CatT", Cat, CatView)


def validate_cat(cat: CatT | None, oid: int) -> CatT:
    if cat is None:
        raise CatNotFoundError(oid)
    return cat
