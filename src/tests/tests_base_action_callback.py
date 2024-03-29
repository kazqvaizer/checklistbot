import pytest

from models import Chat, Message

pytestmark = [
    pytest.mark.usefixtures("use_db", "mock_do"),
]


@pytest.fixture
def raw_message(read_fixture):
    return read_fixture("message")


@pytest.fixture
def execute(tezt_action, telegram_update, telegram_context):
    def _execute(data: dict):
        return tezt_action.run_as_callback(telegram_update(data), telegram_context)

    return _execute


@pytest.fixture
def chat(factory):
    return factory.chat(chat_id=200500)


def test_no_chats_by_default():
    assert Chat.select().count() == 0


def test_no_messages_by_default():
    assert Message.select().count() == 0


def test_no_calls_by_default(mock_send_message):
    assert mock_send_message.call_count == 0


def test_chat_created(execute, raw_message):
    execute(raw_message)

    chat = Chat.select().first()
    assert chat.chat_id == 200500
    assert chat.username == "boi"
    assert chat.first_name == "John"
    assert chat.last_name == "Doe"
    assert chat.chat_type == "private"
    assert chat.language_code == "ru"


def test_message_added_to_new_chat(execute, raw_message):
    execute(raw_message)

    chat = Chat.select().first()
    message = Message.select().first()
    assert message.message_id == 48
    assert message.text == "/start"
    assert message.chat == chat
    assert message.date == "2017-07-14 02:40:00+00:00"


def test_message_added_to_existing_chat(chat, execute, raw_message):
    execute(raw_message)

    message = Message.select().first()
    assert message.chat == chat


def test_add_new_chat_by_id(chat, execute, raw_message):
    raw_message["message"]["chat"]["id"] = 300500

    execute(raw_message)

    assert Chat.select().count() == 2


def test_previous_chat_messages_stood_intact(chat, execute, raw_message):
    raw_message["message"]["chat"]["id"] = 300500

    execute(raw_message)

    new_chat = Chat.select()[1]
    assert chat.messages.count() == 0
    assert new_chat.messages.count() == 1


def test_default_language_code(execute, raw_message):
    del raw_message["message"]["from"]["language_code"]

    execute(raw_message)

    chat = Chat.select().first()
    assert chat.language_code == "en"


def test_default_language_code_if_no_user(execute, raw_message):
    del raw_message["message"]["from"]

    execute(raw_message)

    chat = Chat.select().first()
    assert chat.language_code == "en"


def test_action_has_correct_message_and_bot(execute, raw_message, telegram_bot, mocker):
    mock = mocker.patch("actions.base.Action.__init__", return_value=None)

    execute(raw_message)

    message = Message.select().first()
    assert mock.call_args[1]["message"] == message
    assert mock.call_args[1]["bot"].token == telegram_bot.token


def test_action_do_was_called(mock_do, execute, raw_message):
    execute(raw_message)

    assert mock_do.called
