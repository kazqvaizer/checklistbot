from .base import Action


class StrikeItemAction(Action):
    def do(self):
        if self.chat.has_no_items_at_all:
            self.common_reply("no_items_to_check_off")
            self.common_reply("to_start_help")

            return

        item = self.chat.get_item_by_index(int(self.message.text))
        if item is None:
            self.common_reply("no_index")

            return

        item.is_checked = not item.is_checked  # Toggle
        item.save()

        if not self.chat.has_not_checked_items:

            # Show all struck items to get more dopamine
            self.reply(self.chat.get_formatted_items())

            self.common_reply("congrats")
            self.common_reply("to_start_help")

            self.chat.delete_items()

            return

        self.reply(self.chat.get_formatted_items())
