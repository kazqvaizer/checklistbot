import pytest

from bot import get_callback
from handlers import StartHandler
from models import Chat, Message

pytestmark = [
    pytest.mark.usefixtures("use_db"),
]


@pytest.fixture
def raw_message(read_fixture):
    return read_fixture("message")


@pytest.fixture
def execute(telegram_update, telegram_context):
    def _execute(method: callable, data: dict):
        return method(telegram_update(data), telegram_context)

    return _execute


@pytest.fixture
def chat(factory):
    return factory.chat(chat_id=200500, username="deadinside")


def test_no_chats_by_default():
    assert Chat.select().count() == 0


def test_no_messages_by_default():
    assert Message.select().count() == 0


def test_chat_created_after_event(execute, raw_message):
    execute(get_callback(StartHandler), raw_message)

    chat = Chat.select().first()
    assert chat.chat_id == 200500
    assert chat.username == "boi"
    assert chat.first_name == "John"
    assert chat.last_name == "Doe"
    assert chat.chat_type == "private"


def test_message_created_after_event(chat, execute, raw_message):
    execute(get_callback(StartHandler), raw_message)

    message = Message.select().first()
    assert message.message_id == 48
    assert message.text == "/start"
    assert message.chat == chat
    assert message.date == "2017-07-14 02:40:00+00:00"  # fuken sqlite dates


def test_auto_reply(chat, execute, raw_message, mock_reply):
    execute(get_callback(StartHandler), raw_message)

    assert mock_reply.call_count == 1


def test_existed_chat_updates(chat, execute, raw_message):
    execute(get_callback(StartHandler), raw_message)

    assert Chat.select().count() == 1
    assert chat.refresh().username == "boi"


def test_leave_other_chats_intact_after_update(factory, chat, execute, raw_message):
    ya_chat = factory.chat(username="jenkins")

    execute(get_callback(StartHandler), raw_message)

    chat = chat.refresh()
    ya_chat = ya_chat.refresh()
    assert chat.refresh().username == "boi"
    assert ya_chat.refresh().username == "jenkins"


def test_add_new_chat_by_id(chat, execute, raw_message):
    raw_message["message"]["chat"]["id"] = 300500

    execute(get_callback(StartHandler), raw_message)

    assert Chat.select().count() == 2


def test_add_new_messages_to_new_chat(chat, execute, raw_message):
    raw_message["message"]["chat"]["id"] = 300500

    execute(get_callback(StartHandler), raw_message)

    new_chat = Chat.select()[1]
    assert chat.messages.count() == 0
    assert new_chat.messages.count() == 1
