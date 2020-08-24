from handlers.base import EventHandler
from messages import registry
from models import TodoItem


class NewItemHandler(EventHandler):
    def work(self):
        if self.chat.has_no_recent_activity():
            self.replier.add_reply(self.chat, text=registry["help_1"])
            self.replier.add_reply(self.chat, text=registry["help_2"])

        TodoItem.create(chat=self.chat, text=self.message.text)

        parts = []
        for index, item in enumerate(self.chat.todo_items.select(), 1):
            parts.append(f"{index}. {item.text}")

        self.replier.add_reply(self.chat, text="\n".join(parts))