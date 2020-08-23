from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from telegram import Bot

from models import Chat, Message


@dataclass
class Reply:
    """Single text reply to chat."""

    chat: Chat
    text: str


class Replier:

    _replies: List[Reply]

    def __init__(self, bot: Bot = None):
        self.bot = bot
        self._replies = []

    def add_reply(self, chat: Chat, text: str):
        self._replies.append(Reply(chat=chat, text=text))

    def get_replies(self):
        return self._replies

    def clean_all(self):
        self._replies = []

    def reply_to_all(self):
        if not self.bot:
            return

        for reply in self.get_replies():
            self.bot.send_message(chat_id=reply.chat.chat_id, text=reply.text)

        self.clean_all()


class EventHandler(ABC):
    def __init__(self, chat: Chat, message: Message, bot: Bot = None):
        self.chat = chat
        self.message = message

        self.replier = Replier(bot)

    @abstractmethod
    def work(self):
        """Do some work, add replies to replier..."""
