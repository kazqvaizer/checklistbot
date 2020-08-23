import logging

from envparse import env
from telegram.ext import CommandHandler, Updater

from decorators import save_chat_and_message
from handlers import StartHandler
from models import Chat, Message

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


env.read_envfile()


updater = Updater(token=env("TELEGRAM_BOT_TOKEN"), use_context=True)
dispatcher = updater.dispatcher


@save_chat_and_message
def start(update, context, chat: Chat, message: Message):
    handler = StartHandler(chat=chat, message=message, bot=context.bot)
    handler.work()
    handler.reply_to_all()


def define_routes():
    dispatcher.add_handler(CommandHandler("start", start))


if __name__ == "__main__":
    define_routes()
    updater.start_polling()
