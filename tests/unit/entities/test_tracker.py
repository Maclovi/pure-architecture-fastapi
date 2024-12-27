from cats.entities.breed.models import Breed
from cats.entities.cat.models import Cat
from tests.mocks.common.tracker import FakeTracker


async def test_tracker(
    new_cat: Cat,
    new_breed: Breed,
    fake_tracker: FakeTracker,
) -> None:
    fake_tracker.add_one(new_cat)
    assert fake_tracker.entities[0] == new_cat

    expected_entities = 3
    fake_tracker.add_many([new_breed, new_breed])
    assert len(fake_tracker.entities) == expected_entities

    await fake_tracker.delete(new_breed)
    assert fake_tracker.entities[0] == new_cat
    assert fake_tracker.entities[1] == new_breed

    await fake_tracker.delete(new_breed)
    assert new_breed not in fake_tracker.entities
