import pytest

from cats.entities.breed.errors import BreedNamelengthError
from cats.entities.breed.value_objects import BreedName
from cats.entities.cat.errors import (
    CatAgeMaxError,
    CatColorLengthError,
    CatDescriptionLengthError,
)
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription
from cats.entities.common.errors import FieldError


@pytest.mark.value_objects
@pytest.mark.parametrize(
    ("value", "exc_class"),
    [
        ("determinateness", None),
        ("a" * 50, None),
        ("c" * 51, BreedNamelengthError),
        ("b", BreedNamelengthError),
    ],
)
def test_breed_name(value: str, exc_class: type[FieldError] | None) -> None:
    if exc_class:
        with pytest.raises(exc_class):
            BreedName(value)
    else:
        breed_name = BreedName(value)
        assert value == breed_name.value
        assert isinstance(breed_name, BreedName)


@pytest.mark.value_objects
@pytest.mark.parametrize(
    ("value", "exc_class"),
    [
        (-1, CatAgeMaxError),
        (0, None),
        (99, None),
        (100, CatAgeMaxError),
    ],
)
def test_cat_age(value: int, exc_class: type[FieldError] | None) -> None:
    if exc_class:
        with pytest.raises(exc_class):
            CatAge(value)
    else:
        cat_age = CatAge(value)
        assert value == cat_age.value
        assert isinstance(cat_age, CatAge)


@pytest.mark.value_objects
@pytest.mark.parametrize(
    ("value", "exc_class"),
    [
        ("aa", CatColorLengthError),
        ("aaa", None),
        ("a" * 50, None),
        ("a" * 100, CatColorLengthError),
    ],
)
def test_cat_description(
    value: str,
    exc_class: type[FieldError] | None,
) -> None:
    if exc_class:
        with pytest.raises(exc_class):
            CatColor(value)
    else:
        cat_color = CatColor(value)
        assert value == cat_color.value
        assert isinstance(cat_color, CatColor)


@pytest.mark.value_objects
@pytest.mark.parametrize(
    ("value", "exc_class"),
    [
        ("", None),
        ("a" * 1000, None),
        ("a" * 1001, CatDescriptionLengthError),
        ("a" * 2002, CatDescriptionLengthError),
    ],
)
def test_cat_color(value: str, exc_class: type[FieldError] | None) -> None:
    if exc_class:
        with pytest.raises(exc_class):
            CatDescription(value)
    else:
        cat_description = CatDescription(value)
        assert value == cat_description.value
        assert isinstance(cat_description, CatDescription)
