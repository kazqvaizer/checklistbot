import pytest
from freezegun import freeze_time

pytestmark = [
    pytest.mark.usefixtures("use_db"),
    pytest.mark.freeze_time("2049-02-01 10:02"),
]


@pytest.fixture
def chat(factory):
    return factory.chat()


@pytest.fixture
def item(factory, chat):
    with freeze_time("2049-02-01 07:02"):
        item = factory.item(chat=chat)
    return item


def test_has_no_recent_activity(item, chat):
    assert chat.has_no_recent_activity is True


def test_has_recent_modified_activity(item, chat):
    item.is_checked = True
    item.save()

    assert chat.has_no_recent_activity is False


def test_has_recent_create_activity(factory, chat):
    factory.item(chat=chat)

    assert chat.has_no_recent_activity is False


def test_no_items_no_activity(chat):
    assert chat.has_no_recent_activity is True
