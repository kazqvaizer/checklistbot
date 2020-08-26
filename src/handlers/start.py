from messages import registry

from .base import EventHandler


class StartHandler(EventHandler):
    def work(self):
        self.replier.add_reply(registry["to_start_help"])
