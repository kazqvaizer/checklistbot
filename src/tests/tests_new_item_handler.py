import pytest

from handlers import NewItemHandler

pytestmark = [
    pytest.mark.usefixtures("use_db"),
    pytest.mark.freeze_time("2049-02-01 10:02"),
]


@pytest.fixture
def chat(factory):
    return factory.chat()


@pytest.fixture
def message(factory, chat):
    return factory.chat(chat=chat, text="Eat 8.5 oranges!")


@pytest.fixture
def exist_item(factory, chat):
    return factory.item(chat=chat, text="Buy 10 oranges!", is_checked=False)


@pytest.fixture
def handler(chat, message):
    return NewItemHandler(chat, message)


def test_add_new_item(exist_item, chat, handler):
    handler.work()

    items = chat.items
    assert len(items) == 2


def test_new_and_already_exist_items(exist_item, chat, handler):
    handler.work()

    items = chat.items
    assert items[0] == exist_item
    assert items[1].text == "Eat 8.5 oranges!"  # New item


def test_list_all_items_after_item_addition(exist_item, chat, handler):
    handler.work()

    reply = handler.replier.get_replies()[0]
    assert "1. Buy 10 oranges!" in reply.text
    assert "2. Eat 8.5 oranges!" in reply.text


def test_also_add_help_messages_if_no_recent_activity(chat, handler):
    handler.work()

    replies = handler.replier.get_replies()
    assert "Let me remind" in replies[0].text
    assert "index" in replies[1].text
    assert "oranges!" in replies[2].text  # The list
