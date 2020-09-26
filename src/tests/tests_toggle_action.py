import pytest

from actions import ToggleAction

pytestmark = [
    pytest.mark.usefixtures("use_db"),
]


@pytest.fixture
def chat(factory):
    return factory.chat()


@pytest.fixture
def action(factory, chat, telegram_bot):
    return ToggleAction(factory.message(chat=chat), telegram_bot)


@pytest.mark.parametrize("enabled, result", ((True, False), (False, True)))
def test_toggled(chat, action, enabled, result):
    chat.enabled = enabled
    chat.save()

    action.do()

    assert chat.enabled is result


@pytest.mark.parametrize("enabled, message", ((True, "Disabled!"), (False, "Enabled!")))
def test_toggled_message(chat, action, enabled, message, mock_reply):
    chat.enabled = enabled
    chat.save()

    action.do()

    assert mock_reply.call_count == 1
    assert message in mock_reply.call_args[0][0]
