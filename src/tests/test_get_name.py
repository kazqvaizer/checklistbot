import pytest

pytestmark = [
    pytest.mark.usefixtures("use_db"),
]


def test_first_name(factory):
    chat = factory.chat(username="boi", first_name="John")

    assert chat.get_name() == "John"


def test_username(factory):
    chat = factory.chat(username="boi")

    assert chat.get_name() == "boi"


def test_empty(factory):
    chat = factory.chat()

    assert chat.get_name() == ""
