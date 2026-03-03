from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import MetaData

# Naming convention helps with SQLite and future migrations
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)


def init_db(app: Flask) -> None:
    db.init_app(app)
    with app.app_context():
        db.create_all()

