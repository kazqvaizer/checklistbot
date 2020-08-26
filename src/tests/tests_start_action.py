import pytest

from actions import StartAction
from models import TodoItem

pytestmark = [
    pytest.mark.usefixtures("use_db"),
]


@pytest.fixture
def message(factory):
    return factory.message()


@pytest.fixture
def action(message, telegram_bot):
    return StartAction(message, telegram_bot)


def test_replies_with_help(action, mock_reply):
    action.do()

    assert mock_reply.call_count == 1
    assert "start a new" in mock_reply.call_args[0][0]


def test_drop_items_after_start(action, factory, message):
    factory.item(chat=message.chat)

    action.do()

    assert TodoItem.select().count() == 0


def test_info_that_previous_list_was_deleted(action, factory, message, mock_reply):
    factory.item(chat=message.chat)

    action.do()

    assert mock_reply.call_count == 2
    assert "has just been deleted!" in mock_reply.call_args_list[0][0][0]


def test_do_not_drop_other_chat_items_after_start(action, factory, message):
    factory.item()

    action.do()

    assert TodoItem.select().count() == 1
