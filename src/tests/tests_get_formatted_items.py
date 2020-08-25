import pytest

from models import TodoItem

pytestmark = [
    pytest.mark.usefixtures("use_db"),
]


@pytest.fixture
def chat(factory):
    return factory.chat()


@pytest.fixture
def items(factory, chat):
    return [
        factory.item(chat=chat, text="Hello"),
        factory.item(chat=chat, text="Nice!"),
    ]


def test_format_without_strike(items, chat):
    lines = chat.get_formatted_items().split("\n")

    assert len(lines) == 2
    assert "1. Hello" == lines[0]
    assert "2. Nice!" == lines[1]


def test_format_with_strike(items, chat):
    items[0].is_checked = True
    items[0].save()

    lines = chat.get_formatted_items().split("\n")

    assert len(lines) == 2
    assert "<s>1. Hello</s>" == lines[0]
    assert "2. Nice!" == lines[1]


def test_respect_order_by_id(items, chat):
    TodoItem.update(id=100500).where(TodoItem.id == items[0].id).execute()

    lines = chat.get_formatted_items().split("\n")

    assert len(lines) == 2
    assert "1. Nice!" == lines[0]
    assert "2. Hello" == lines[1]


def test_no_items_is_okay(chat):
    assert chat.get_formatted_items() == ""
