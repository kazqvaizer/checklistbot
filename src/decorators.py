from functools import wraps

from models import Chat


def create_or_update_chat(fn):
    @wraps(fn)
    def wrapped(update, context):

        data = update.effective_chat.to_dict()

        data["chat_id"] = data.pop("id", None)
        data["chat_type"] = data.pop("type", None)

        Chat.replace(**data).execute()

        return fn(update, context)

    return wrapped
