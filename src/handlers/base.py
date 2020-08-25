from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from telegram import Bot, ParseMode

from models import Chat, Message


@dataclass
class Reply:
    """Single text reply to chat."""

    chat: Chat
    text: str


class Replier:
    """Collects all replies."""

    _replies: List[Reply]

    def __init__(self, bot: Bot = None, default_chat: Chat = None):
        self.bot = bot
        self.default_chat = default_chat
        self._replies = []

    def add_reply(self, text: str, chat: Chat = None):
        if not chat:
            chat = self.default_chat

        if not chat:
            raise ValueError("You should define chat in reply!")

        self._replies.append(Reply(chat=chat, text=text))

    def get_replies(self):
        return self._replies

    def clean_all(self):
        self._replies = []

    def reply(self):
        if not self.bot:
            raise ValueError("You should define bot for reply!")

        for single_reply in self.get_replies():
            self.bot.send_message(
                chat_id=single_reply.chat.chat_id,
                text=single_reply.text,
                parse_mode=ParseMode.HTML,
            )

        self.clean_all()


class EventHandler(ABC):
    """Base event handler."""

    def __init__(self, chat: Chat, message: Message, bot: Bot = None):
        self.chat = chat
        self.message = message

        self.replier = Replier(bot, default_chat=self.chat)

    @abstractmethod
    def work(self):
        """Do some work, add replies to replier..."""

    def reply(self):
        """Reply to all generated messages."""
        self.replier.reply()
