from .base import Action


class HelpAction(Action):
    def do(self):
        self.common_reply("general_help")
