from datetime import datetime

from envparse import env
from peewee import CharField, DateTimeField, IntegerField, Model, SqliteDatabase

env.read_envfile()

db = SqliteDatabase(env("DATABASE_URL"))


def _utcnow():
    return datetime.utcnow()


class BaseModel(Model):
    created = DateTimeField(default=_utcnow)
    modified = DateTimeField(null=True)

    class Meta:
        database = db

    def save(self, *args, **kwargs):
        if self.id is not None:
            self.modified = _utcnow()

        return super().save(*args, **kwargs)


class Chat(BaseModel):
    chat_id = IntegerField(unique=True)
    chat_type = CharField(null=True)
    username = CharField(null=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)


app_models = BaseModel.__subclasses__()
