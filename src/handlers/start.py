from messages import registry

from .base import EventHandler


class StartHandler(EventHandler):
    def work(self):
        text = registry["greetings"].format(name=self.chat.get_name())

        self.replier.add_reply(text)
        self.replier.add_reply(registry["good_luck"])
