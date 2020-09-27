import pytest
from telegram import ParseMode

pytestmark = [
    pytest.mark.usefixtures("use_db", "mock_do"),
]


@pytest.fixture
def action(tezt_action, telegram_bot, factory):
    def _action(code: str = "en"):
        chat = factory.chat(chat_id=200500, language_code=code)

        return tezt_action(factory.message(chat=chat), telegram_bot)

    return _action


def test_reply_triggers_send_message(action, mock_send_message):
    action().reply("Word!")

    assert mock_send_message.call_count == 1
    assert mock_send_message.call_args[1]["chat_id"] == 200500
    assert mock_send_message.call_args[1]["text"] == "Word!"
    assert mock_send_message.call_args[1]["parse_mode"] == ParseMode.HTML


@pytest.mark.parametrize(
    "code, result",
    (
        ("en", "Congratulations! You have been finished you to-do list!"),
        ("ru", "Поздравляю! Вы завершили свой список дел!"),
        ("fr", "Congratulations! You have been finished you to-do list!"),
    ),
)
def test_common_reply_works_with_languages(action, mock_send_message, code, result):
    action = action(code)

    action.common_reply("congrats")

    assert mock_send_message.call_args[1]["text"] == result
