from dataclasses import dataclass

from . import Breed


@dataclass
class Cat:
    color: str
    age: int
    description: str
    breed: Breed | None
