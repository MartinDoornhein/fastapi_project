import os
import time
from contextlib import contextmanager
from typing import Generator

import psycopg
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://app_user:app_password@127.0.0.1:5432/app_db",
)


@contextmanager
def get_connection() -> Generator[psycopg.Connection]:
    with psycopg.connect(DATABASE_URL) as connection:
        yield connection


def initialize_database() -> None:
    for attempt in range(1, 11):
        try:
            with get_connection() as connection:
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS items (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        description TEXT,
                        price DOUBLE PRECISION NOT NULL CHECK (price > 0)
                    )
                    """
                )
            return
        except psycopg.OperationalError:
            if attempt == 10:
                raise
            time.sleep(1)
