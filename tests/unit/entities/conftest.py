from unittest.mock import AsyncMock, Mock

import pytest

from cats.entities.common.tracker import Tracker


@pytest.fixture
def fake_tracker() -> Tracker:
    fake = Mock()
    fake.add_one = Mock(return_value=None)
    fake.add_many = Mock(return_value=None)
    fake.delete = AsyncMock(return_value=None)
    return fake
