import pytest

from actions import NewItemAction

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
def action(message, telegram_bot):
    return NewItemAction(message, telegram_bot)


def test_no_items_by_default(chat, action):
    assert len(chat.items) == 0


def test_add_new_item(chat, action):
    action.do()

    assert len(chat.items) == 1


def test_new_item_text_from_messages(chat, action):
    action.do()

    item = chat.items.first()
    assert item.text == "Eat 8.5 oranges!"


def test_multiline_message_cause_multiple_items(chat, action, message):
    message.text = "First item!\nSecond one!"
    message.save()

    action.do()

    assert len(chat.items) == 2
    assert chat.items[0].text == "First item!"
    assert chat.items[1].text == "Second one!"


def test_clean_empty_lines(chat, action, message):
    message.text = "\n Only item! \n  \n\t\n\r\n"
    message.save()

    action.do()

    assert len(chat.items) == 1
    assert chat.items.first().text == "Only item!"


def test_escape_html(chat, action, message):
    message.text = "<s><html></asd> wow"
    message.save()

    action.do()

    item = chat.items.first()
    assert "<s><html></asd>" not in item.text


def test_list_all_items_after_item_addition(factory, chat, action, mock_reply):
    factory.item(chat=chat, text="Buy 10 oranges!")  # Exist item

    action.do()

    reply = mock_reply.call_args[0][0]
    assert "1. Buy 10 oranges!" in reply
    assert "2. Eat 8.5 oranges!" in reply


def test_also_add_help_messages_if_no_recent_activity(chat, action, mock_reply):
    action.do()

    replies = mock_reply.call_args_list
    assert "index" in replies[0][0][0]  # The help
    assert "oranges!" in replies[1][0][0]  # The list
