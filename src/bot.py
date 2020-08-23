import logging

from envparse import env
from telegram.ext import CommandHandler, Updater

from decorators import create_or_update_chat

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


env.read_envfile()


updater = Updater(token=env("TELEGRAM_BOT_TOKEN"), use_context=True)
dispatcher = updater.dispatcher


@create_or_update_chat
def start(update, context):
    pass


def define_routes():
    dispatcher.add_handler(CommandHandler("start", start))


if __name__ == "__main__":
    define_routes()
    updater.start_polling()
