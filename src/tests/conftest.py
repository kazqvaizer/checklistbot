import json
from os import path
from random import randint

import pytest
from telegram.bot import Bot
from telegram.update import Update

from actions.base import Action
from models import Chat, Message, TodoItem, app_models, db


@pytest.fixture(scope="function")
def use_db():

    db.connect()

    db.drop_tables(app_models)
    db.create_tables(app_models)

    yield db

    db.close()


@pytest.fixture(autouse=True)
def mock_send_message(mocker):
    return mocker.patch("telegram.bot.Bot.send_message")


@pytest.fixture(autouse=True)
def mock_delete_message(mocker):
    return mocker.patch("telegram.bot.Bot.delete_message")


@pytest.fixture
def mock_reply(mocker):
    return mocker.patch("actions.base.Action.reply")


@pytest.fixture
def mock_delete(mocker):
    return mocker.patch("actions.base.Action.delete")


@pytest.fixture
def mock_do(mocker):
    return mocker.patch("actions.base.Action.do")


@pytest.fixture
def tezt_action():
    class TeztAction(Action):
        def do(self):
            super().do()  # You should mock it with `mock_do` fixture

    return TeztAction


@pytest.fixture
def factory():
    class Factory:
        def chat(self, **kwargs):
            chat_id = kwargs.pop("chat_id", None) or randint(100000, 200000)
            return Chat.create(chat_id=chat_id, **kwargs)

        def message(self, **kwargs):
            chat = kwargs.pop("chat", None) or self.chat()
            return Message.create(chat=chat, **kwargs)

        def item(self, **kwargs):
            chat = kwargs.pop("chat", None) or self.chat()
            text = kwargs.pop("text", "some")
            return TodoItem.create(chat=chat, text=text, **kwargs)

    return Factory()


@pytest.fixture
def read_fixture():
    """JSON fixture reader"""

    def read_file(f):
        with open(path.join("tests/fixtures/", f) + ".json") as fp:
            return json.load(fp)

    return read_file


@pytest.fixture
def raw_message(read_fixture):
    return read_fixture("message")


@pytest.fixture
def telegram_update():
    return lambda data: Update.de_json(data, None)


@pytest.fixture
def telegram_bot():
    return Bot("123:123")


@pytest.fixture
def telegram_context(telegram_bot):
    class Context:
        bot = telegram_bot

    return Context()
