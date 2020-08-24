import pytest

from handlers.base import Replier

pytestmark = [
    pytest.mark.usefixtures("use_db"),
]


@pytest.fixture
def chat(factory):
    return factory.chat()


@pytest.fixture
def ya_chat(factory):
    return factory.chat()


@pytest.fixture
def replier(telegram_bot):
    return Replier(bot=telegram_bot)


def test_no_replies_by_default(replier):
    assert len(replier.get_replies()) == 0


def test_add_and_get_reply(chat, replier):
    replier.add_reply(chat, "Hello!")

    replies = replier.get_replies()
    assert len(replies) == 1


def test_reply_fields(chat, replier):
    replier.add_reply(chat, "Hello!")

    reply = replier.get_replies()[0]
    assert reply.chat == chat
    assert reply.text == "Hello!"


def test_send_replies_as_messages(replier, chat, mock_send_message):
    replier.add_reply(chat, "Hello!")

    replier.reply()

    assert mock_send_message.call_count == 1
    assert mock_send_message.call_args[1]["chat_id"] == chat.chat_id
    assert mock_send_message.call_args[1]["text"] == "Hello!"


def test_reply_messages(replier, chat, ya_chat, mock_send_message):
    replier.add_reply(chat, "Hello!")
    replier.add_reply(ya_chat, "Cunt!")

    replier.reply()

    assert mock_send_message.call_count == 2

    assert mock_send_message.call_args_list[0][1]["chat_id"] == chat.chat_id
    assert mock_send_message.call_args_list[0][1]["text"] == "Hello!"

    assert mock_send_message.call_args_list[1][1]["chat_id"] == ya_chat.chat_id
    assert mock_send_message.call_args_list[1][1]["text"] == "Cunt!"


def test_clean_messages_after_reply(replier, chat):
    replier.add_reply(chat, "Hello!")

    replier.reply()

    assert len(replier.get_replies()) == 0


def test_no_replies_if_no_bot(chat, mock_send_message):
    replier = Replier()  # No bot here
    replier.add_reply(chat, "Hello!")

    replier.reply()

    assert mock_send_message.call_count == 0
