from dataclasses import dataclass

from cats.entities.common.errors import FieldError


@dataclass(eq=False)
class BreedNamelengthError(FieldError):
    length: int

    @property
    def message(self) -> str:
        return f"Maximum length must be less than or equal to {self.length!r}"
