from functools import wraps

from telegram.update import Update

from models import Chat, Message


def save_chat_and_message(fn):
    def handle_chat(update: Update) -> Chat:
        data = update.effective_chat.to_dict()
        data["chat_type"] = data.pop("type", None)

        return Chat.get_or_create(chat_id=data.pop("id", None), defaults=data)[0]

    def handle_message(update: Update, chat: Chat) -> Message:
        data = {
            "message_id": update.effective_message.message_id,
            "date": update.effective_message.date,
            "text": update.effective_message.text,
            "chat": chat,
        }

        return Message.create(**data)

    @wraps(fn)
    def wrapped(update, context):
        chat = handle_chat(update)
        message = handle_message(update, chat)

        return fn(update, context, chat=chat, message=message)

    return wrapped
