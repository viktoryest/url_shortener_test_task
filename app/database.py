import sqlite3
from pathlib import Path
from typing import Generator

from app.logger import logger

DB_PATH: Path = Path("urls.db")


def init_db(db_path: Path | str = DB_PATH) -> None:
    logger.info("Initializing database at %s", db_path)

    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS urls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_url TEXT NOT NULL,
                    short_code TEXT UNIQUE NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        logger.info("Database initialized successfully")

    except sqlite3.Error:
        logger.exception("Database initialization failed")
        raise


def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn: sqlite3.Connection | None = None

    try:
        conn = sqlite3.connect(DB_PATH, timeout=5)
        conn.row_factory = sqlite3.Row
        yield conn

    except sqlite3.Error:
        logger.exception("Database connection error")
        raise

    finally:
        if conn is not None:
            conn.close()
