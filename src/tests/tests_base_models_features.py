import pytest

from ..models import Chat

pytestmark = [
    pytest.mark.usefixtures("use_db"),
    pytest.mark.freeze_time("2049-02-01 10:02"),
]


def test_created_date():
    chat = Chat.create(chat_id="100500")

    assert chat.created.isoformat() == "2049-02-01T10:02:00"


def test_modified_date_is_non_by_default():
    chat = Chat.create(chat_id="100500")

    assert chat.modified is None


def test_modified_date_updates():
    chat = Chat.create(chat_id="100500")

    chat.username = "asd"
    chat.save()

    assert chat.modified.isoformat() == "2049-02-01T10:02:00"
