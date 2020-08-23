import pytest

from bot import start
from models import Chat, Message

pytestmark = [
    pytest.mark.usefixtures("use_db"),
]


@pytest.fixture
def raw_message(read_fixture):
    return read_fixture("message")


@pytest.fixture
def execute(telegram_update):
    def _execute(method: callable, data: dict):
        return method(telegram_update(data), {})

    return _execute


@pytest.fixture
def chat(factory):
    return factory.chat(chat_id=200500, username="deadinside")


def test_no_chats_by_default():
    assert Chat.select().count() == 0


def test_no_messages_by_default():
    assert Message.select().count() == 0


@pytest.mark.parametrize("method", (start,))
def test_chat_created_after_event(execute, raw_message, method):
    execute(method, raw_message)

    chat = Chat.select().first()
    assert chat.chat_id == 200500
    assert chat.username == "boi"
    assert chat.first_name == "John"
    assert chat.last_name == "Doe"
    assert chat.chat_type == "private"


@pytest.mark.parametrize("method", (start,))
def test_message_created_after_event(chat, execute, raw_message, method):
    execute(method, raw_message)

    message = Message.select().first()
    assert message.message_id == 48
    assert message.text == "/start"
    assert message.chat == chat
    assert message.date == "2017-07-14 02:40:00+00:00"  # fuken sqlite dates


def test_existed_chat_updates(chat, execute, raw_message):
    execute(start, raw_message)

    chat = chat.get()
    assert Chat.select().count() == 1
    assert chat.username == "boi"


def test_add_new_chat_by_id(chat, execute, raw_message):
    raw_message["message"]["chat"]["id"] = 300500

    execute(start, raw_message)

    assert Chat.select().count() == 2
