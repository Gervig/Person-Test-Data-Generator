import os

import mariadb
from dotenv import load_dotenv

from app.exceptions import DatabaseError

load_dotenv()

_db_password = os.getenv("DB_PASSWORD")
_connection_pool: mariadb.ConnectionPool | None = None


def _get_connection_pool() -> mariadb.ConnectionPool:
    global _connection_pool

    if _connection_pool is None:
        if not _db_password:
            raise DatabaseError("DB_PASSWORD must be configured before using the database.")

        _connection_pool = mariadb.ConnectionPool(
            pool_name="person_test_data_generator",
            pool_size=5,
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=_db_password,
            database=os.getenv("DB_NAME", "addresses"),
        )
    return _connection_pool


def get_connection() -> mariadb.Connection:
    return _get_connection_pool().get_connection()
