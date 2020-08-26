from messages import registry

from .base import Action


class StartAction(Action):
    def work(self):
        self.replier.add_reply(registry["to_start_help"])
