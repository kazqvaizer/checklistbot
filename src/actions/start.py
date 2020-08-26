from messages import registry

from .base import Action


class StartAction(Action):
    def do(self):
        self.reply(registry["to_start_help"])
