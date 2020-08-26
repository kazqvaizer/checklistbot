from html import escape
from typing import List

from messages import registry
from models import TodoItem

from .base import Action


class NewItemAction(Action):
    def cleaned_lines(self) -> List[str]:
        text = escape(self.message.text)
        return [line.strip() for line in text.split("\n") if line.strip()]

    def do(self):
        if self.chat.has_no_recent_activity():
            self.reply(registry["to_check_off_help"])

        for text in self.cleaned_lines():
            TodoItem.create(chat=self.chat, text=text)

        self.reply(self.chat.get_formatted_items())
