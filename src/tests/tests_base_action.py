import pytest
from telegram import ParseMode

from actions.base import Action
from models import Chat, Message

pytestmark = [
    pytest.mark.usefixtures("use_db"),
]


class TeztAction(Action):
    dummy_field = False

    def do(self):
        self.dummy_field = True


@pytest.fixture
def raw_message(read_fixture):
    return read_fixture("message")


@pytest.fixture
def execute(telegram_update, telegram_context):
    def _execute(data: dict):
        return TeztAction.run_as_callback(telegram_update(data), telegram_context)

    return _execute


@pytest.fixture
def action(telegram_bot, factory, chat):
    def _action(code: str = "en"):
        chat.language_code = code
        chat.save()

        return TeztAction(factory.message(chat=chat), telegram_bot)

    return _action


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


def test_action_has_correct_message_and_bot(execute, raw_message, telegram_bot):
    action = execute(raw_message)

    message = Message.select().first()
    assert action.message == message
    assert action.chat == message.chat
    assert action.bot == telegram_bot


def test_action_do_was_called(execute, raw_message):
    action = execute(raw_message)

    execute(raw_message)

    assert action.dummy_field is True


def test_reply_triggers_send_message(action, chat, mock_send_message):
    action().reply("Word!")

    assert mock_send_message.call_count == 1
    assert mock_send_message.call_args[1]["chat_id"] == 200500
    assert mock_send_message.call_args[1]["text"] == "Word!"
    assert mock_send_message.call_args[1]["parse_mode"] == ParseMode.HTML


@pytest.mark.parametrize(
    "code, result",
    (
        ("en", "Congratulations! You have been finished you to-do list!"),
        ("ru", "Поздравляю! Вы завершили свой список дел!"),
        ("fr", "Congratulations! You have been finished you to-do list!"),
    ),
)
def test_common_reply_works_with_languages(action, mock_send_message, code, result):
    action = action(code)

    action.common_reply("congrats")

    assert mock_send_message.call_args[1]["text"] == result
