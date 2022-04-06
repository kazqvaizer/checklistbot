from playhouse.migrate import BigIntegerField, SqliteMigrator, migrate

from models import db


def modify():
    migrator = SqliteMigrator(db)
    migrate(migrator.add_column("chat", "todo_message_id", BigIntegerField(null=True)))


if __name__ == "__main__":
    modify()
