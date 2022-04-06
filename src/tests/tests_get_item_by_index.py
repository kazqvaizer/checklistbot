import pytest

pytestmark = [
    pytest.mark.usefixtures("use_db"),
]


@pytest.fixture
def chat(factory):
    return factory.chat()


@pytest.fixture
def items(factory, chat):
    return [factory.item(chat=chat), factory.item(chat=chat), None]


@pytest.mark.parametrize(
    "index, item",
    (
        (1, 0),
        (2, 1),
        (100, 2),
        (-1, 2),
        (0, 2),
    ),
)
def test_get_by_index(items, chat, index, item):
    assert chat.get_item_by_index(index) == items[item]


def test_no_items_is_okay(chat):
    assert chat.get_item_by_index(10500) is None
