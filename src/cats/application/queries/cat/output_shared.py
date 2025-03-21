from typing import NamedTuple

from cats.application.common.ports.view_models import CatView


class CatsOutput(NamedTuple):
    total: int
    cats: list[CatView]
