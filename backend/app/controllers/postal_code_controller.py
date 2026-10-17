from fastapi import HTTPException

from app.database import get_connection
from app.views.postal_code_view import PostalCodeView


def list_postal_codes() -> list[PostalCodeView]:
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT cPostalCode, cTownName FROM postal_code ORDER BY cPostalCode"
        )
        return [
            PostalCodeView(postal_code=postal_code.strip(), town=town)
            for postal_code, town in cursor.fetchall()
        ]
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve postal codes from the database.",
        ) from exc
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
