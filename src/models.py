from datetime import datetime, timedelta
from typing import Optional

import peewee as pw
from envparse import env

env.read_envfile()

db = pw.SqliteDatabase(env("DATABASE_URL"))


def _utcnow():
    return datetime.utcnow()


def _get_recent_threshold():
    return _utcnow() - timedelta(hours=2)


def _format_item(index: int, item: "TodoItem",) -> str:
    line = f"{index}. {item.text}"
    return f"<s>{line}</s>" if item.is_checked else line


class BaseModel(pw.Model):
    created = pw.DateTimeField(default=_utcnow)
    modified = pw.DateTimeField(null=True)

    class Meta:
        database = db

    def save(self, *args, **kwargs):
        if self.id is not None:
            self.modified = _utcnow()

        return super().save(*args, **kwargs)


class Chat(BaseModel):
    chat_id = pw.IntegerField(unique=True)
    chat_type = pw.CharField(null=True)
    username = pw.CharField(null=True)
    first_name = pw.CharField(null=True)
    last_name = pw.CharField(null=True)

    @property
    def items(self) -> pw.Select:
        return self.todo_items.select().order_by(TodoItem.id.asc())

    @property
    def has_not_checked_items(self) -> bool:
        return self.items.where(TodoItem.is_checked == False).exists()

    @property
    def has_no_items_at_all(self) -> bool:
        return not self.items.exists()

    @property
    def has_recently_modified_items(self) -> bool:
        return self.items.where(TodoItem.modified > _get_recent_threshold()).exists()

    @property
    def has_recently_created_items(self) -> bool:
        return self.items.where(TodoItem.created > _get_recent_threshold()).exists()

    @property
    def has_no_recent_activity(self) -> bool:
        return not (self.has_recently_modified_items or self.has_recently_created_items)

    def get_item_by_index(self, index: int) -> Optional["TodoItem"]:
        return self.items.offset(index - 1).first() if index > 0 else None

    def get_formatted_items(self) -> str:
        return "\n".join([_format_item(*args) for args in enumerate(self.items, 1)])


class Message(BaseModel):
    message_id = pw.IntegerField(null=True)
    chat = pw.ForeignKeyField(Chat, backref="messages")
    date = pw.DateTimeField(null=True)
    text = pw.CharField(null=True)


class TodoItem(BaseModel):
    chat = pw.ForeignKeyField(Chat, backref="todo_items")
    is_checked = pw.BooleanField(default=False)
    text = pw.CharField()


app_models = BaseModel.__subclasses__()
