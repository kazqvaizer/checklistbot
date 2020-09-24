import pytest

from actions import HelpAction

pytestmark = [
    pytest.mark.usefixtures("use_db"),
]


@pytest.fixture
def action(factory, telegram_bot):
    return HelpAction(factory.message(), telegram_bot)


def test_replies_with_general_help(action, mock_reply):
    action.do()

    assert mock_reply.call_count == 1
    assert "Strike out items" in mock_reply.call_args[0][0]
