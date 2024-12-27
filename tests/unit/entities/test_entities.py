from cats.entities.breed.models import Breed
from cats.entities.cat.models import Cat


def test_cat(new_cat: Cat) -> None:
    age = 3
    assert new_cat.age.value == age
    assert new_cat.color.value == "red"
    assert new_cat.description.value == "biba"
    assert isinstance(new_cat, Cat)


def test_breed(new_breed: Breed) -> None:
    breed_name = "boba"
    assert new_breed.name.value == breed_name
    assert isinstance(new_breed, Breed)
