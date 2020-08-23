import pytest

from handlers import StartHandler

pytestmark = [
    pytest.mark.usefixtures("use_db"),
]


@pytest.fixture
def chat(factory):
    return factory.chat(username="JohnyBoi")


@pytest.fixture
def handler(chat, factory):
    return StartHandler(chat, factory.message())


def test_no_replies_before_default(handler):
    assert len(handler.replier.get_replies()) == 0


def test_replies(handler):
    handler.work()

    replies = handler.replier.get_replies()
    assert len(replies) == 2


def test_reply_content(chat, handler):
    handler.work()

    reply = handler.replier.get_replies()[0]
    assert reply.chat == chat
    assert "JohnyBoi" in reply.text
