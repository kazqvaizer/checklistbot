import pytest
from telegram.error import NetworkError

pytestmark = [
    pytest.mark.usefixtures("use_db", "mock_do"),
]


@pytest.fixture
def action(tezt_action, telegram_bot, factory):
    def _action():
        chat = factory.chat(chat_id=200500)

        return tezt_action(factory.message(chat=chat), telegram_bot)

    return _action


def test_delete(action, mock_delete_message):
    action().delete(100500)

    assert mock_delete_message.call_count == 1
    assert mock_delete_message.call_args[1]["chat_id"] == 200500
    assert mock_delete_message.call_args[1]["message_id"] == 100500


def test_do_nothing_if_nothing_to_delete(action, mock_delete_message):
    action().delete(None)

    assert mock_delete_message.call_count == 0


def test_drop_errors(action, mock_delete_message):
    mock_delete_message.side_effect = NetworkError(message="123asd")

    action().delete(100324)  # Not failing

    assert mock_delete_message.call_count == 1
