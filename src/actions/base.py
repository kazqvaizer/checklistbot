from abc import ABC, abstractmethod

from telegram import Bot, ParseMode
from telegram.ext.callbackcontext import CallbackContext
from telegram.update import Update

from models import Chat, Message


class Action(ABC):
    """
    Base action.

    Saves message and chat and implements `do` method for your logic.
    """

    def __init__(self, message: Message, bot: Bot):
        self.bot = bot
        self.chat = message.chat
        self.message = message

    @abstractmethod
    def do(self):
        """Do some work, add replies to replier..."""

    def reply(self, text: str):
        """
        Reply to message chat.

        Call it from your `do` method.
        """
        self.bot.send_message(
            chat_id=self.message.chat.chat_id, text=text, parse_mode=ParseMode.HTML,
        )

    @classmethod
    def store_message(self, update: Update) -> Message:
        """Store incoming message and chat."""
        chat_defaults = dict(
            chat_type=update.effective_chat.type,
            username=update.effective_chat.username,
            first_name=update.effective_chat.first_name,
            last_name=update.effective_chat.last_name,
        )

        chat = Chat.get_or_create(
            chat_id=update.effective_chat.id, defaults=chat_defaults
        )[0]

        message = Message.create(
            message_id=update.effective_message.message_id,
            date=update.effective_message.date,
            text=update.effective_message.text,
            chat=chat,
        )

        return message

    @classmethod
    def run_as_callback(cls, update: Update, context: CallbackContext) -> "Action":
        """Assign this class method as telegram dispatcher callback."""

        message = cls.store_message(update)

        action = cls(message=message, bot=context.bot)
        action.do()

        return action
