from dataclasses import dataclass

from cats.entities.common.errors import FieldError


@dataclass(eq=False)
class CatAgeMinError(FieldError):
    limit: int

    @property
    def message(self) -> str:
        return (
            f"The minimum age of the cat should not be less than {self.limit}"
        )


@dataclass(eq=False)
class CatAgeMaxError(FieldError):
    age: int

    @property
    def message(self) -> str:
        return f"The maximum age of a cat should not exceed {self.age!r}"


@dataclass(eq=False)
class CatColorMinLengthError(FieldError):
    length: int

    @property
    def message(self) -> str:
        return f"The color length should not be less than {self.length}"


@dataclass(eq=False)
class CatColorMaxLengthError(FieldError):
    length: int

    @property
    def message(self) -> str:
        return f"The color length should not exceed {self.length}"


@dataclass(eq=False)
class CatDescriptionLengthError(FieldError):
    length: int

    @property
    def message(self) -> str:
        return f"The description length should not exceed {self.length!r}"
