import pytest

pytestmark = [
    pytest.mark.usefixtures("use_db"),
]


@pytest.fixture
def chat(factory):
    return factory.chat()


@pytest.fixture
def item(factory, chat):
    return factory.item(chat=chat)


def test_has_no_items_at_all(item, chat):
    assert chat.has_no_items_at_all is False


def test_has_items(chat):
    assert chat.has_no_items_at_all is True
