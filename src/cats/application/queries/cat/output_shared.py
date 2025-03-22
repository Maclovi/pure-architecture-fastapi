from dataclasses import dataclass

from cats.application.common.persistence.view_models import CatView


@dataclass(slots=True, frozen=True)
class CatsOutput:
    total: int
    cats: list[CatView]
