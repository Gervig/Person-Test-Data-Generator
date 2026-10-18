import mariadb

from app.database import get_connection
from app.exceptions import DatabaseError, PostalCodeUnavailableError
from app.models.postal_code import PostalCode


def get_all() -> list[PostalCode]:
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT cPostalCode, cTownName FROM postal_code ORDER BY cPostalCode"
        )
        return [
            PostalCode(postal_code=postal_code.strip(), town_name=town_name)
            for postal_code, town_name in cursor.fetchall()
        ]
    except mariadb.Error as exc:
        raise DatabaseError("Could not retrieve postal codes from the database.") from exc
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def get_random() -> PostalCode:
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT cPostalCode, cTownName "
            "FROM postal_code ORDER BY RAND() LIMIT 1"
        )
        row = cursor.fetchone()
        if row is None:
            raise PostalCodeUnavailableError("No postal codes are available.")
        postal_code, town_name = row
        return PostalCode(postal_code=postal_code.strip(), town_name=town_name)
    except mariadb.Error as exc:
        raise DatabaseError("Could not retrieve postal codes from the database.") from exc
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
