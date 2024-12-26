from dataclasses import dataclass

from cats.entities.breed.errors import BreedNamelengthError


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class BreedName:
    value: str

    def __post_init__(self) -> None:
        breed_min_length = 2
        breed_max_length = 50
        if not (breed_min_length <= len(self.value) <= breed_max_length):
            raise BreedNamelengthError(breed_max_length)
