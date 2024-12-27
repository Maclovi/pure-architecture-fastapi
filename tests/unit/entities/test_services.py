from cats.entities.cat.models import Cat
from cats.entities.cat.services import CatService
from cats.entities.cat.value_objects import CatDescription
from tests.mocks.common.tracker import FakeTracker


async def test_cat_service(fake_tracker: FakeTracker) -> None:
    cat_service = CatService(fake_tracker)

    created_cat = cat_service.create_cat(None, 3, "blue", "biba and boba")
    assert isinstance(created_cat, Cat)

    cat_service.add_cat(created_cat)
    assert fake_tracker.entities[0] == created_cat

    cat_service.change_description(created_cat, CatDescription("new descr"))
    assert created_cat.description.value == "new descr"

    await cat_service.remove_cat(created_cat)
    assert created_cat not in fake_tracker.entities
