import pytest

from actions import StartAction

pytestmark = [
    pytest.mark.usefixtures("use_db"),
]


@pytest.fixture
def message(factory):
    return factory.message()


@pytest.fixture
def action(message, telegram_bot):
    return StartAction(message, telegram_bot)


def test_replies_with_help(action, mock_reply):
    action.do()

    assert mock_reply.call_count == 1
    assert "start a new" in mock_reply.call_args[0][0]
