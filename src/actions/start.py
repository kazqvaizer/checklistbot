from .base import Action


class StartAction(Action):
    def do(self):
        self.common_reply("to_start_help")
