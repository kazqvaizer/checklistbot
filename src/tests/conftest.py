import json
from os import path

import pytest
from telegram.update import Update

from models import Chat, app_models, db


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


@pytest.fixture
def factory():
    class Factory:
        def chat(*args, **kwargs):
            return Chat.create(**kwargs)

    return Factory()


@pytest.fixture
def read_fixture():
    """JSON fixture reader"""

    def read_file(f):
        with open(path.join("tests/fixtures/", f) + ".json") as fp:
            return json.load(fp)

    return read_file


@pytest.fixture
def telegram_update():
    return lambda data: Update.de_json(data, None)
