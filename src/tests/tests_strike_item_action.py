import pytest

from actions import StrikeItemAction
from models import TodoItem

pytestmark = [
    pytest.mark.usefixtures("use_db"),
]


@pytest.fixture
def chat(factory):
    return factory.chat(enabled=True)


@pytest.fixture
def exist_items(factory, chat):
    items = []
    for fruit in ["oranges", "apples", "fucwits"]:
        items.append(factory.item(chat=chat, text=f"Buy 10 {fruit}!", is_checked=False))

    return items


@pytest.fixture
def action(chat, factory, telegram_bot):
    return lambda index="2", message_id=None: StrikeItemAction(
        factory.message(chat=chat, text=index, message_id=message_id), telegram_bot
    )


def test_all_non_checked_by_default(exist_items, chat):
    assert chat.items.where(TodoItem.is_checked == False).count() == 3
    assert chat.items.where(TodoItem.is_checked == True).count() == 0


def test_change_checked_flag_by_text_from_message(exist_items, chat, action):
    action(index="2").do()

    item = chat.items.where(TodoItem.is_checked == True).first()
    assert item == exist_items[1]  # Correct second item
    assert item.is_checked is True


def test_strike_only_one_item_by_index_from_message(exist_items, chat, action):
    action(index="2").do()

    assert chat.items.where(TodoItem.is_checked == False).count() == 2
    assert chat.items.where(TodoItem.is_checked == True).count() == 1


def test_toggle_item_by_second_strike_with_same_text(exist_items, chat, action):
    action(index="2").do()
    action(index="2").do()

    assert chat.items.where(TodoItem.is_checked == False).count() == 3
    assert chat.items.where(TodoItem.is_checked == True).count() == 0


def test_no_strikes_if_bad_index(exist_items, chat, action):
    action(index="100500").do()

    assert chat.items.where(TodoItem.is_checked == False).count() == 3


def test_if_all_messages_struck_delete_them(exist_items, chat, action):
    action(index="1").do()
    action(index="2").do()
    action(index="3").do()

    assert chat.items.count() == 0


def test_positions_are_actually_struck(exist_items, chat, action, mock_reply):
    action = action(index="2")

    action.do()

    reply = mock_reply.call_args[0][0]
    assert "1. Buy 10 oranges!" in reply
    assert "<s>2. Buy 10 apples!</s>" in reply
    assert "3. Buy 10 fucwits!" in reply


def test_struck_back(exist_items, chat, action, mock_reply):
    action(index="2").do()  # Stand-alone to not mess with replies

    action = action(index="2")
    action.do()

    reply = mock_reply.call_args[0][0]
    assert "1. Buy 10 oranges!" in reply
    assert "2. Buy 10 apples!" in reply
    assert "3. Buy 10 fucwits!" in reply


def test_ignore_action_if_chat_is_disabled(exist_items, chat, action, mock_reply):
    chat.enabled = False
    chat.save()

    action(index="2").do()

    assert mock_reply.called is False


def test_delete_incoming_message_with_index(exist_items, action, mock_delete):
    action(message_id=10300500).do()

    mock_delete.assert_called_once_with(10300500)
