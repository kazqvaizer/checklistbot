import logging

from envparse import env
from telegram.ext import CommandHandler, Updater

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


env.read_envfile()


updater = Updater(token=env("TELEGRAM_BOT_TOKEN"), use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

if __name__ == "__main__":
    updater.start_polling()
