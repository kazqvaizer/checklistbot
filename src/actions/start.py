from .base import Action


class StartAction(Action):
    def do(self):
        if not self.chat.has_no_items_at_all:
            self.chat.delete_items()
            self.common_reply("deleted")

        self.common_reply("to_start_help")
