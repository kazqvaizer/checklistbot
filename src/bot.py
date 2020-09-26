import logging

import sentry_sdk
from envparse import env
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from actions import HelpAction, NewItemAction, StartAction, StrikeItemAction

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


env.read_envfile()

sentry_sdk.init(env("SENTRY_DSN", default=None))


updater = Updater(token=env("TELEGRAM_BOT_TOKEN"), use_context=True)
dispatcher = updater.dispatcher

base_filter = Filters.text & (~Filters.command) & (~Filters.status_update)
text = base_filter & (~Filters.regex("^[0-9]+$"))
numbers = base_filter & Filters.regex("^[0-9]+$")


def define_routes():
    dispatcher.add_handler(CommandHandler("start", StartAction.run_as_callback))
    dispatcher.add_handler(CommandHandler("help", HelpAction.run_as_callback))
    dispatcher.add_handler(MessageHandler(text, NewItemAction.run_as_callback))
    dispatcher.add_handler(MessageHandler(numbers, StrikeItemAction.run_as_callback))


if __name__ == "__main__":
    define_routes()
    updater.start_polling()
