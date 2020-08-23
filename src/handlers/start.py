from handlers.base import EventHandler
from messages import registry


class StartHandler(EventHandler):
    def work(self):
        text = registry["greetings"].format(name=self.chat.get_name())

        self.replier.add_reply(self.chat, text=text)
        self.replier.add_reply(self.chat, text=registry["good_luck"])
