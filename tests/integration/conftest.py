import sqlite3
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from main import app

# Tables mirroring the MySQL schema in agents/db/schema.sql
SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    role TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS consultations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    model_name TEXT,
    original_image_path TEXT,
    xai_image_path TEXT,
    prediction_label TEXT,
    confidence_score REAL,
    patient_name TEXT,
    pdf_path TEXT,
    timestamp TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS training_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    dataset_path TEXT,
    model_name TEXT,
    status TEXT DEFAULT 'In Progress',
    progress REAL DEFAULT 0.0,
    metrics_json TEXT,
    started_at TEXT DEFAULT (datetime('now')),
    finished_at TEXT
);
"""


class SQLiteConn:
    """Wraps a sqlite3 connection to mimic mysql.connector's interface."""
    def __init__(self, db_path=":memory:"):
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")

    def cursor(self, dictionary=False):
        return SQLiteCursor(self._conn, dictionary)

    def commit(self):
        self._conn.commit()

    def close(self):
        # No-op: fixture owns the lifecycle
        pass


class SQLiteCursor:
    """Wraps sqlite3 cursor. Returns dicts when dictionary=True."""
    def __init__(self, conn, dictionary=False):
        self._cursor = conn.cursor()
        self._dictionary = dictionary
        self.lastrowid = None

    def execute(self, sql, params=None):
        # Translate MySQL %s placeholders to SQLite ?
        sql_sqlite = sql.replace("%s", "?")
        if params is None:
            self._cursor.execute(sql_sqlite)
        else:
            self._cursor.execute(sql_sqlite, params)
        self.lastrowid = self._cursor.lastrowid
        return self

    def fetchone(self):
        row = self._cursor.fetchone()
        if row is None:
            return None
        if self._dictionary:
            return dict(row)
        return row

    def fetchall(self):
        rows = self._cursor.fetchall()
        if self._dictionary:
            return [dict(r) for r in rows]
        return rows

    def __iter__(self):
        return iter(self.fetchall())


@pytest.fixture
def sqlite_db():
    """Creates an in-memory SQLite DB with the full schema and patches get_db_connection."""
    conn = SQLiteConn()
    conn.cursor().execute("PRAGMA foreign_keys = ON")
    for statement in SCHEMA.split(";"):
        stmt = statement.strip()
        if stmt:
            conn.cursor().execute(stmt)
    conn.commit()

    # Patch ALL modules that import get_db_connection
    patchers = [
        patch("database.get_db_connection", return_value=conn),
        patch("routers.auth.get_db_connection", return_value=conn),
        patch("routers.history.get_db_connection", return_value=conn),
        patch("routers.inference.get_db_connection", return_value=conn),
        patch("services.trainer_engine.get_db_connection", return_value=conn),
    ]
    for p in patchers:
        p.start()
    yield conn
    for p in patchers:
        p.stop()
    conn.close()


@pytest.fixture
def client():
    return TestClient(app)
