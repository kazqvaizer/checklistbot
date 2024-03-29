from .base import Action


class StrikeItemAction(Action):
    def do(self):
        if not self.chat.enabled:
            return

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

        new_todo_message = self.reply(self.chat.get_formatted_items())

        self.delete(self.message.message_id)  # Drop message with index
        self.delete(self.chat.todo_message_id)  # Drop previous todo list

        self.chat.todo_message_id = new_todo_message.message_id
        self.chat.save()

        if not self.chat.has_not_checked_items:

            self.common_reply("congrats")
            self.common_reply("to_start_help")

            self.chat.delete_items()
