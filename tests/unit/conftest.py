import pytest

from cats.entities.common.tracker import Tracker
from tests.mocks.common.tracker import FakeTracker


@pytest.fixture
def fake_tracker() -> Tracker:
    return FakeTracker()
