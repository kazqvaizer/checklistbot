from datetime import datetime

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

    def get_name(self):
        return self.first_name or self.username or ""


class Message(BaseModel):
    message_id = pw.IntegerField(null=True)
    chat = pw.ForeignKeyField(Chat, backref="messages")
    date = pw.DateTimeField(null=True)
    text = pw.CharField(null=True)


app_models = BaseModel.__subclasses__()
