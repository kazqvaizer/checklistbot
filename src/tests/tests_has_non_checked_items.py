import pytest

pytestmark = [
    pytest.mark.usefixtures("use_db"),
]


@pytest.fixture
def chat(factory):
    return factory.chat()


@pytest.fixture
def item(factory, chat):
    return factory.item(chat=chat, is_checked=False)


def test_has_non_checked_items(item, chat):
    assert chat.has_not_checked_items is True


def test_has_no_non_checked_items(item, chat):
    item.is_checked = True
    item.save()

    assert chat.has_not_checked_items is False


def test_no_items_no_non_checked(chat):

    assert chat.has_not_checked_items is False
