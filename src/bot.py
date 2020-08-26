import logging

from envparse import env
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from actions import NewItemAction, StartAction, StrikeItemAction
from decorators import save_chat_and_message
from models import Chat, Message

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


env.read_envfile()


updater = Updater(token=env("TELEGRAM_BOT_TOKEN"), use_context=True)
dispatcher = updater.dispatcher


def get_callback(Action):
    @save_chat_and_message
    def callback(update, context, chat: Chat, message: Message):
        handler = Action(chat=chat, message=message, bot=context.bot)
        handler.work()
        handler.reply()

    return callback


def define_routes():
    dispatcher.add_handler(CommandHandler("start", get_callback(StartAction)))
    dispatcher.add_handler(
        MessageHandler(
            Filters.text and ~Filters.regex("^[0-9]+$"), get_callback(NewItemAction)
        )
    )
    dispatcher.add_handler(
        MessageHandler(
            Filters.text and Filters.regex("^[0-9]+$"), get_callback(StrikeItemAction)
        )
    )


if __name__ == "__main__":
    define_routes()
    updater.start_polling()
