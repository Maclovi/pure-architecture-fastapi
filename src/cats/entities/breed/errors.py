from dataclasses import dataclass

from typing_extensions import override

from cats.entities.common.errors import FieldError


@dataclass(eq=False)
class BreedNameMinlengthError(FieldError):
    length: int

    @property
    @override
    def message(self) -> str:
        return f"The minimum length must not be less than {self.length!r}"


@dataclass(eq=False)
class BreedNameMaxlengthError(FieldError):
    length: int

    @property
    @override
    def message(self) -> str:
        return f"Maximum length must be less than or equal to {self.length!r}"
