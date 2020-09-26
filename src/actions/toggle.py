from .base import Action


class ToggleAction(Action):
    def do(self):
        self.chat.enabled = not self.chat.enabled
        self.chat.save()

        self.common_reply("enabled" if self.chat.enabled else "disabled")
