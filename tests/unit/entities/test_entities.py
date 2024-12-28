from cats.entities.breed.models import Breed
from cats.entities.cat.models import Cat


def test_cat(new_cat: Cat) -> None:
    age = 15
    assert new_cat.age.value == age
    assert new_cat.color.value == "pink"
    assert new_cat.description.value == "biba with pink hair"
    assert isinstance(new_cat, Cat)


def test_breed(new_breed: Breed) -> None:
    assert new_breed.name.value == "boba with cute face"
    assert isinstance(new_breed, Breed)
