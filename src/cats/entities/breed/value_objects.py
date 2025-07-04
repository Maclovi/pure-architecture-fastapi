from dataclasses import dataclass

from cats.entities.breed.errors import (
    BreedNameMaxlengthError,
    BreedNameMinlengthError,
)


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class BreedName:
    value: str

    def __post_init__(self) -> None:
        breed_min_length = 2
        breed_max_length = 50
        if len(self.value) < breed_min_length:
            raise BreedNameMinlengthError(breed_min_length)
        if len(self.value) > breed_max_length:
            raise BreedNameMaxlengthError(breed_max_length)
