from dataclasses import dataclass

from cats.application.common.ports.view_models import CatView


@dataclass(frozen=True, slots=True)
class CatsOutput:
    total: int
    cats: list[CatView]
