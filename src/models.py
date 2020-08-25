from datetime import datetime, timedelta
from typing import Optional

import peewee as pw
from envparse import env

env.read_envfile()

db = pw.SqliteDatabase(env("DATABASE_URL"))


def _utcnow():
    return datetime.utcnow()


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

    def get_formatted_items(self) -> str:
        lines = []

        for index, item in enumerate(self.items, 1):
            line = f"{index}. {item.text}"

            if item.is_checked:
                line = f"<s>{line}</s>"

            lines.append(line)

        return "\n".join(lines)

    def get_item_by_index(self, index: int) -> Optional["TodoItem"]:
        if index <= 0:  # Yeap. This index starts from 1.
            return

        try:
            return self.items[index - 1]
        except IndexError:
            pass

    def get_name(self) -> str:
        return self.first_name or self.username or ""

    def has_not_checked_items(self) -> bool:
        return self.items.where(TodoItem.is_checked == False).exists()

    def has_no_items_at_all(self) -> bool:
        return not self.items.exists()

    def has_no_recent_activity(self) -> bool:
        threshold_time = _utcnow() - timedelta(hours=2)
        query = self.items

        recently_modified = query.where(TodoItem.modified > threshold_time).exists()
        if recently_modified:
            return False

        recently_created = query.where(TodoItem.created > threshold_time).exists()
        if recently_created:
            return False

        return True


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
