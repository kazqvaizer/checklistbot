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
def replier(telegram_bot, chat):
    return Replier(bot=telegram_bot, default_chat=chat)


def test_no_replies_by_default(replier):
    assert len(replier.get_replies()) == 0


def test_add_and_get_reply(chat, replier):
    replier.add_reply("Hello!")

    replies = replier.get_replies()
    assert len(replies) == 1


def test_reply_fields(chat, replier):
    replier.add_reply("Hello!")

    reply = replier.get_replies()[0]
    assert reply.chat == chat
    assert reply.text == "Hello!"


def test_send_replies_as_messages(replier, chat, mock_send_message):
    replier.add_reply("Hello!")

    replier.reply()

    assert mock_send_message.call_count == 1
    assert mock_send_message.call_args[1]["chat_id"] == chat.chat_id
    assert mock_send_message.call_args[1]["text"] == "Hello!"


def test_reply_to_not_default_chat(replier, chat, ya_chat, mock_send_message):
    replier.add_reply("Hello!")
    replier.add_reply("Cunt!", chat=ya_chat)

    replier.reply()

    assert mock_send_message.call_count == 2

    assert mock_send_message.call_args_list[0][1]["chat_id"] == chat.chat_id
    assert mock_send_message.call_args_list[0][1]["text"] == "Hello!"

    assert mock_send_message.call_args_list[1][1]["chat_id"] == ya_chat.chat_id
    assert mock_send_message.call_args_list[1][1]["text"] == "Cunt!"


def test_clean_messages_after_reply(replier):
    replier.add_reply("Hello!")

    replier.reply()

    assert len(replier.get_replies()) == 0


def test_no_replies_if_no_bot(chat, mock_send_message):
    replier = Replier(default_chat=chat)  # No bot here
    replier.add_reply("Hello!")

    with pytest.raises(ValueError):
        replier.reply()


def test_cannot_add_replies_if_no_chat(telegram_bot, chat, mock_send_message):
    replier = Replier(bot=telegram_bot)  # No chat here

    with pytest.raises(ValueError):
        replier.add_reply("Hello!", chat=None)  # And here
