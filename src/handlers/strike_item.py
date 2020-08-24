from handlers.base import EventHandler
from models import TodoItem


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

        parts = []
        for index, item in enumerate(self.chat.items, 1):
            if item.is_checked:
                parts.append(f"{index}. <s>{item.text}</s>")
            else:
                parts.append(f"{index}. {item.text}")

        self.replier.add_reply(self.chat, text="\n".join(parts))
