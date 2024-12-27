import pytest

from cats.entities.breed.errors import BreedNamelengthError
from cats.entities.breed.value_objects import BreedName
from cats.entities.cat.errors import (
    CatAgeMaxError,
    CatAgeMinError,
    CatColorMaxLengthError,
    CatColorMinLengthError,
    CatDescriptionLengthError,
)
from cats.entities.cat.value_objects import CatAge, CatColor, CatDescription
from cats.entities.common.errors import FieldError


@pytest.mark.value_objects
@pytest.mark.parametrize(
    ("value", "exc_class"),
    [
        ("a", BreedNamelengthError),
        ("a" * 13, None),
        ("a" * 50, None),
        ("a" * 51, BreedNamelengthError),
    ],
)
def test_breed_name(value: str, exc_class: type[FieldError] | None) -> None:
    if exc_class:
        with pytest.raises(exc_class) as excinfo:
            BreedName(value)
        assert (
            excinfo.value.message
            == "Maximum length must be less than or equal to 50"
        )
    else:
        breed_name = BreedName(value)
        assert value == breed_name.value
        assert isinstance(breed_name, BreedName)


@pytest.mark.value_objects
@pytest.mark.parametrize(
    ("value", "exc_class"),
    [
        (-1, CatAgeMinError),
        (0, None),
        (99, None),
        (100, CatAgeMaxError),
    ],
)
def test_cat_age(value: int, exc_class: type[FieldError] | None) -> None:
    if exc_class:
        with pytest.raises(exc_class) as excinfo:
            CatAge(value)

        min_age = 0
        if value < min_age:
            msg = "The minimum age of the cat should not be less than 0"
        else:
            msg = "The maximum age of a cat should not exceed 99"
        assert excinfo.value.message == msg
    else:
        cat_age = CatAge(value)
        assert value == cat_age.value
        assert isinstance(cat_age, CatAge)


@pytest.mark.value_objects
@pytest.mark.parametrize(
    ("value", "exc_class"),
    [
        ("a" * 2, CatColorMinLengthError),
        ("a" * 3, None),
        ("a" * 50, None),
        ("a" * 100, CatColorMaxLengthError),
    ],
)
def test_cat_color(
    value: str,
    exc_class: type[FieldError] | None,
) -> None:
    if exc_class:
        with pytest.raises(exc_class) as excinfo:
            CatColor(value)

        color_min_length = 3
        if len(value) < color_min_length:
            msg = "The color length should not be less than 3"
        else:
            msg = "The color length should not exceed 50"
        assert excinfo.value.message == msg
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
def test_cat_description(
    value: str,
    exc_class: type[FieldError] | None,
) -> None:
    if exc_class:
        with pytest.raises(exc_class) as excinfo:
            CatDescription(value)
        assert (
            excinfo.value.message
            == "The description length should not exceed 1000"
        )
    else:
        cat_description = CatDescription(value)
        assert value == cat_description.value
        assert isinstance(cat_description, CatDescription)
