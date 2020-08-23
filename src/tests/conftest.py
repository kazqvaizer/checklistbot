import pytest

from ..models import Chat, app_models, db


@pytest.fixture(scope="function")
def use_db():

    db.connect()

    db.drop_tables(app_models)
    db.create_tables(app_models)

    yield db

    db.close()


@pytest.fixture
def factory():
    class Factory:
        def chat(*args, **kwargs):
            return Chat.create(**kwargs)

    return Factory()
