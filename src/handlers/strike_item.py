from models import TodoItem

from .base import EventHandler


class StrikeItemHandler(EventHandler):
    def work(self):
        index = int(self.message.text)

        if self.chat.has_no_items_at_all():
            return

        item = self.chat.get_item_by_index(index)
        if not item:
            return

        item.is_checked = not item.is_checked  # Toggle
        item.save()

        if not self.chat.has_not_checked_items():
            TodoItem.delete().where(TodoItem.chat == self.chat).execute()

        self.replier.add_reply(self.chat, text=self.chat.get_formatted_items())
