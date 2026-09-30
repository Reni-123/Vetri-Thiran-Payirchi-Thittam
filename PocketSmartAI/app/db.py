import sqlite3
from contextlib import contextmanager
from pathlib import Path

from app.config import BASE_DIR


DB_PATH = BASE_DIR / "data" / "pocketsmart.db"

DB_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    planner TEXT NOT NULL,
    request_json TEXT NOT NULL,
    response_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);
"""


@contextmanager
def get_db():
    connection = sqlite3.connect(DB_PATH)

    connection.row_factory = sqlite3.Row

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    try:
        yield connection

        connection.commit()

    finally:
        connection.close()


def init_db():
    with get_db() as db:
        db.executescript(SCHEMA)