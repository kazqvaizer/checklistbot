from messages import registry
from models import TodoItem

from .base import EventHandler


class StrikeItemHandler(EventHandler):
    def work(self):
        if self.chat.has_no_items_at_all():
            self.replier.add_reply(registry["no_items_to_check_off"])
            self.replier.add_reply(registry["to_start_help"])

            return

        item = self.chat.get_item_by_index(int(self.message.text))
        if item is None:
            self.replier.add_reply(registry["no_index"])

            return

        item.is_checked = not item.is_checked  # Toggle
        item.save()

        if not self.chat.has_not_checked_items():

            # Show all struck items to get more dopamine
            self.replier.add_reply(self.chat.get_formatted_items())

            TodoItem.delete().where(TodoItem.chat == self.chat).execute()

            self.replier.add_reply(registry["congrats"])
            self.replier.add_reply(registry["to_start_help"])

            return

        self.replier.add_reply(self.chat.get_formatted_items())
