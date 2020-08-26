import pytest

from actions import StrikeItemAction
from models import TodoItem

pytestmark = [
    pytest.mark.usefixtures("use_db"),
]


@pytest.fixture
def chat(factory):
    return factory.chat()


@pytest.fixture
def exist_items(factory, chat):
    items = []
    for fruit in ["oranges", "apples", "fucwits"]:
        items.append(factory.item(chat=chat, text=f"Buy 10 {fruit}!", is_checked=False))

    return items


@pytest.fixture
def handler(chat, factory):
    return lambda index: StrikeItemAction(chat, factory.message(chat=chat, text=index))


def test_all_non_checked_by_default(exist_items, chat):
    assert chat.items.where(TodoItem.is_checked == False).count() == 3
    assert chat.items.where(TodoItem.is_checked == True).count() == 0


def test_change_checked_flag_by_text_from_message(exist_items, chat, handler):
    handler(index="2").work()

    item = chat.items.where(TodoItem.is_checked == True).first()
    assert item == exist_items[1]  # Correct second item
    assert item.is_checked is True


def test_strike_only_one_item_by_index_from_message(exist_items, chat, handler):
    handler(index="2").work()

    assert chat.items.where(TodoItem.is_checked == False).count() == 2
    assert chat.items.where(TodoItem.is_checked == True).count() == 1


def test_toggle_item_by_second_strike_with_same_text(exist_items, chat, handler):
    handler(index="2").work()
    handler(index="2").work()

    assert chat.items.where(TodoItem.is_checked == False).count() == 3
    assert chat.items.where(TodoItem.is_checked == True).count() == 0


def test_no_strikes_if_bad_index(exist_items, chat, handler):
    handler(index="100500").work()

    assert chat.items.where(TodoItem.is_checked == False).count() == 3


def test_if_all_messages_struck_delete_them(exist_items, chat, handler):
    handler(index="1").work()
    handler(index="2").work()
    handler(index="3").work()

    assert chat.items.count() == 0


def test_positions_are_actually_struck(exist_items, chat, handler):
    handler = handler(index="2")

    handler.work()

    reply = handler.replier.get_replies()[0]
    assert "1. Buy 10 oranges!" in reply.text
    assert "<s>2. Buy 10 apples!</s>" in reply.text
    assert "3. Buy 10 fucwits!" in reply.text


def test_struck_back(exist_items, chat, handler):
    handler(index="2").work()  # Stand-alone to not mess with replies

    handler = handler(index="2")
    handler.work()

    reply = handler.replier.get_replies()[0]
    assert "1. Buy 10 oranges!" in reply.text
    assert "2. Buy 10 apples!" in reply.text
    assert "3. Buy 10 fucwits!" in reply.text
