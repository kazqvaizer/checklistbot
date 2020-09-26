from playhouse.migrate import BooleanField, SqliteMigrator, migrate

from models import db


def add_enabled():
    migrator = SqliteMigrator(db)
    migrate(migrator.add_column("chat", "enabled", BooleanField(default=True)))


if __name__ == "__main__":
    add_enabled()
