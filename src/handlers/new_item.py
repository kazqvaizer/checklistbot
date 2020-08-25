from html import escape

from messages import registry
from models import TodoItem

from .base import EventHandler


class NewItemHandler(EventHandler):
    def work(self):
        if self.chat.has_no_recent_activity():
            self.replier.add_reply(registry["help_2"])

        TodoItem.create(chat=self.chat, text=escape(self.message.text))

        self.replier.add_reply(self.chat.get_formatted_items())
