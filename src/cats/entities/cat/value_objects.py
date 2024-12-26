from dataclasses import dataclass

from cats.entities.cat.errors import (
    CatAgeMaxError,
    CatColorLengthError,
    CatDescriptionLengthError,
)


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class CatAge:
    value: int

    def __post_init__(self) -> None:
        min_age = 0
        max_age = 99
        if not (min_age <= self.value <= max_age):
            raise CatAgeMaxError(self.value)


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class CatColor:
    value: str

    def __post_init__(self) -> None:
        color_min_length = 3
        color_max_length = 50
        if not (color_min_length <= len(self.value) <= color_max_length):
            raise CatColorLengthError(color_min_length)


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class CatDescription:
    value: str

    def __post_init__(self) -> None:
        description_max_length = 1000
        if len(self.value) > description_max_length:
            raise CatDescriptionLengthError(description_max_length)
