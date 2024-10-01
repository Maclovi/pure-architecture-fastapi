from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CatView:
    cat_id: int
    breed: str
    age: int
    color: str
    description: str
