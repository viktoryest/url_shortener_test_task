import sqlite3

from app.logger import logger
from app.utils import generate_short_code

MAX_ATTEMPTS = 5


def create_short_code(conn: sqlite3.Connection, full_url: str) -> str:
    """
    Generate and persist a unique short code.
    Returns the created code.
    """
    for _ in range(MAX_ATTEMPTS):
        code = generate_short_code()

        try:
            conn.execute(
                "INSERT INTO urls (full_url, short_code) VALUES (?, ?)",
                (full_url, code),
            )
            conn.commit()

            logger.info("Short code created: %s", code)
            return code

        except sqlite3.IntegrityError:
            continue

    logger.error("Failed to create unique short code after %s attempts", MAX_ATTEMPTS)
    raise RuntimeError("Failed to generate unique short code")


def get_full_url(conn: sqlite3.Connection, code: str) -> str | None:
    """
    Retrieve the original URL associated with the given short code.
    Returns the full URL if found, otherwise None.
    """
    row = conn.execute(
        "SELECT full_url FROM urls WHERE short_code = ?",
        (code,),
    ).fetchone()

    if row is None:
        logger.info("Short code not found: %s", code)
        return None

    logger.debug("URL retrieved for code: %s", code)
    return row["full_url"]
