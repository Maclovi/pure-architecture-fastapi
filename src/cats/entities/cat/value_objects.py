from dataclasses import dataclass

from cats.entities.cat.errors import (
    CatAgeMaxError,
    CatAgeMinError,
    CatColorMaxLengthError,
    CatColorMinLengthError,
    CatDescriptionLengthError,
)


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class CatAge:
    value: int

    def __post_init__(self) -> None:
        min_age = 0
        max_age = 99
        if self.value < min_age:
            raise CatAgeMinError(min_age)
        if self.value > max_age:
            raise CatAgeMaxError(max_age)


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class CatColor:
    value: str

    def __post_init__(self) -> None:
        color_min_length = 3
        color_max_length = 50
        if len(self.value) < color_min_length:
            raise CatColorMinLengthError(color_min_length)
        if len(self.value) > color_max_length:
            raise CatColorMaxLengthError(color_max_length)


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class CatDescription:
    value: str

    def __post_init__(self) -> None:
        description_max_length = 1000
        if len(self.value) > description_max_length:
            raise CatDescriptionLengthError(description_max_length)
