from abc import ABC, abstractmethod
from typing import Optional

from telegram import Bot
from telegram import Message as TelegramMessage
from telegram import ParseMode
from telegram.error import NetworkError
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from messages import CommonMessages
from models import Message


class Action(ABC):
    """
    Base action.

    Saves message and chat and implements `do` method for your logic.
    """

    def __init__(self, message: Message, bot: Bot):
        self.bot = bot
        self.chat = message.chat
        self.message = message
        self.common_messages = CommonMessages(self.chat.language_code)

    @abstractmethod
    def do(self):
        """Do some work, add replies to replier..."""

    def reply(self, text: str) -> TelegramMessage:
        """
        Reply to message chat.

        Call it from your `do` method.
        """
        return self.bot.send_message(
            chat_id=self.message.chat.chat_id,
            text=text,
            parse_mode=ParseMode.HTML,
        )

    def delete(self, message_id: Optional[int]):
        """
        Delete chat message.

        Call it from your `do` method.
        """
        if not message_id:
            return

        try:
            self.bot.delete_message(
                chat_id=self.message.chat.chat_id,
                message_id=message_id,
            )
        except NetworkError:
            pass

    def common_reply(self, message_slug: str):
        """Reply with common message."""
        self.reply(self.common_messages.get_message(message_slug))

    @classmethod
    def run_as_callback(action_cls, update: Update, context: CallbackContext):
        """Assign this class method as telegram dispatcher callback."""
        message = Message.create_from_update(update)

        action_cls(message=message, bot=context.bot).do()
