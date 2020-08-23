import pytest

pytestmark = [
    pytest.mark.usefixtures("use_db"),
    pytest.mark.freeze_time("2049-02-01 10:02"),
]


@pytest.fixture
def chat(factory):
    return factory.chat()


def test_created_date(chat):
    assert chat.created.isoformat() == "2049-02-01T10:02:00"


def test_modified_date_is_non_by_default(chat):
    assert chat.modified is None


def test_modified_date_updates(chat):
    chat.username = "asd"
    chat.save()

    assert chat.modified.isoformat() == "2049-02-01T10:02:00"
